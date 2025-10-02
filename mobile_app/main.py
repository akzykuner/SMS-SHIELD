import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import mainthread

from mobile_app.api_client import classify_text, send_feedback

class ShieldSMSUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=8, padding=8, **kwargs)
        self.last_text = ""
        self.last_pred = None
        self.last_proba = None

        self.title = Label(text="[b]Shield-SMS[/b]", markup=True, font_size="20sp", size_hint_y=None, height=40)
        self.add_widget(self.title)

        self.input = TextInput(hint_text="Pega aquí el SMS...", multiline=True, size_hint_y=None, height=140)
        self.add_widget(self.input)

        self.analyze_btn = Button(text="Analizar", size_hint_y=None, height=48)
        self.analyze_btn.bind(on_release=lambda _: self._analyze_async())
        self.add_widget(self.analyze_btn)

        self.result = Label(text="Resultado: —", size_hint_y=None, height=30)
        self.add_widget(self.result)

        self.urls_label = Label(text="URLs detectadas:", size_hint_y=None, height=24)
        self.add_widget(self.urls_label)

        self.urls_container = GridLayout(cols=1, size_hint_y=None)
        self.urls_container.bind(minimum_height=self.urls_container.setter('height'))
        self.scroll = ScrollView(size_hint=(1, 1))
        self.scroll.add_widget(self.urls_container)
        self.add_widget(self.scroll)

        # Feedback
        self.fb_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=48, spacing=8)
        self.safe_btn = Button(text="Marcar como SEGURO")
        self.smish_btn = Button(text="Reportar SMISHING")
        self.safe_btn.bind(on_release=lambda _: self._send_feedback("ham"))
        self.smish_btn.bind(on_release=lambda _: self._send_feedback("smishing"))
        self.fb_box.add_widget(self.safe_btn)
        self.fb_box.add_widget(self.smish_btn)
        self.add_widget(self.fb_box)

        self.status = Label(text="", size_hint_y=None, height=24)
        self.add_widget(self.status)

    def _analyze_async(self):
        self._update_status("Analizando...")
        t = threading.Thread(target=self._analyze, daemon=True)
        t.start()

    def _analyze(self):
        text = self.input.text.strip()
        if not text:
            self._update_status("Ingresa un texto.")
            return
        try:
            data = classify_text(text)
            if data.get("verification_status") == "pending":
                self._update_status("La verificación está pendiente...")
                return
            label = data.get("label", "—")
            proba = float(data.get("probability", 0.0))
            self.last_text = text
            self.last_pred = label
            self.last_proba = proba
            self._update_result(label, proba)
            self._update_urls(data.get("urls") or [])
            self._update_status("Listo.")
        except Exception as e:
            self._update_status(f"Error: {e}")

    def _send_feedback(self, user_label: str):
        if not self.last_text:
            self._update_status("Nada que enviar. Primero analiza un SMS.")
            return
        self._update_status("Enviando feedback...")
        t = threading.Thread(target=self._send_feedback_thread, args=(user_label,), daemon=True)
        t.start()

    def _send_feedback_thread(self, user_label: str):
        try:
            send_feedback(
                text=self.last_text,
                user_label=user_label,
                predicted_label=self.last_pred,
                probability=self.last_proba,
            )
            self._update_status("¡Gracias por tu feedback!")
        except Exception as e:
            self._update_status(f"Error al enviar feedback: {e}")

    @mainthread
    def _update_status(self, text: str):
        self.status.text = text

    @mainthread
    def _update_result(self, label: str, proba: float):
        pct = int(round(proba * 100))
        self.result.text = f"Resultado: {label} ({pct}%)"

    @mainthread
    def _update_urls(self, urls):
        self.urls_container.clear_widgets()
        if not urls:
            self.urls_container.add_widget(Label(text="(Ninguna)", size_hint_y=None, height=24))
            return
        for u in urls:
            if isinstance(u, dict):
                text = f"{u.get('url','')}  [{u.get('domain','')}]"
            else:
                text = str(u)
            self.urls_container.add_widget(Label(text=text, size_hint_y=None, height=24))

class ShieldSMSApp(App):
    def build(self):
        return ShieldSMSUI()

if __name__ == "__main__":
    ShieldSMSApp().run()