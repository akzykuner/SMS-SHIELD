package com.shieldsms

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.provider.Telephony
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import android.util.Log
import androidx.core.app.NotificationCompat
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

class SmsReceiver : BroadcastReceiver() {

    private val client by lazy { OkHttpClient() }

    // REEMPLAZA con la IP de tu PC y puerto de tu API
    private val API_BASE = "http://192.168.18.8:8000"
    private val TAG = "ShieldSMS"
    private val CHANNEL_ID = "shield_sms_alerts"

    override fun onReceive(context: Context, intent: Intent) {
        if (Telephony.Sms.Intents.SMS_RECEIVED_ACTION != intent.action) return

        val messages = Telephony.Sms.Intents.getMessagesFromIntent(intent)
        val smsBody = messages.joinToString("") { it.displayMessageBody }
        Log.d(TAG, "SMS recibido: $smsBody")

        val pending = goAsync()
        Thread {
            try {
                val payload = JSONObject().put("text", smsBody).toString()
                val reqBody = payload.toRequestBody("application/json; charset=utf-8".toMediaType())
                val req = Request.Builder()
                    .url("$API_BASE/classify")
                    .post(reqBody)
                    .build()
                client.newCall(req).execute().use { resp ->
                    val body = resp.body?.string().orEmpty()
                    Log.d(TAG, "Respuesta API: $body")
                    val (label, prob) = parseResult(body)
                    notify(context, label, prob)
                }
            } catch (e: Exception) {
                Log.e(TAG, "Error clasificando", e)
                notify(context, "error", 0.0)
            } finally {
                pending.finish()
            }
        }.start()
    }

    private fun parseResult(body: String): Pair<String, Double> = try {
        val o = JSONObject(body)
        Pair(o.optString("label", "unknown"), o.optDouble("probability", 0.0))
    } catch (_: Exception) { Pair("unknown", 0.0) }

    private fun notify(context: Context, label: String, prob: Double) {
        val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            nm.createNotificationChannel(
                NotificationChannel(CHANNEL_ID, "Shield-SMS Alerts", NotificationManager.IMPORTANCE_HIGH)
            )
        }
        val pct = (prob * 100).toInt()
        val title = if (label == "smishing") "SMISHING detectado" else "SMS seguro"
        val text = "$label ($pct%)"

        val notif = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_dialog_alert)
            .setContentTitle(title)
            .setContentText(text)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .build()

        nm.notify((System.currentTimeMillis() % Int.MAX_VALUE).toInt(), notif)
    }
}