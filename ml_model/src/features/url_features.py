import re
from urllib.parse import urlparse
import ipaddress

# Lista mínima de acortadores (puedes ampliarla en refactor)
SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd",
    "ow.ly",
    "cut.ly",
    "buff.ly",
}

# Caracteres de cierre a limpiar al final de la URL detectada
_TRAILING_PUNCT = '.,);]»”"'

def _strip_trailing_punct(s: str) -> str:
    while s and s[-1] in _TRAILING_PUNCT:
        s = s[:-1]
    return s

def _normalize_candidate(raw: str) -> str:
    raw = _strip_trailing_punct(raw.strip())
    # Agregar esquema si falta, para que urlparse funcione
    if not re.match(r'(?i)^[a-z][a-z0-9+.-]*://', raw):
        raw = 'http://' + raw
    return raw

def _extract_raw_candidates(text: str):
    if not text:
        return []
    # URLs de dominio (con o sin esquema)
    pat_domain = r'(?i)\b((?:https?://)?(?:www\.)?[a-z0-9.-]+\.[a-z]{2,}(?:/[\w\-./?%&=+#:]*)?)'
    # URLs con IP (con o sin esquema)
    pat_ip = r'(?i)\b((?:https?://)?(?:\d{1,3}\.){3}\d{1,3}(?:/[\w\-./?%&=+#:]*)?)'
    # URLs con IPv6 entre corchetes, ej: https://[2001:db8::1]/ruta o https://[2001:db8::1]:8443
    pat_ipv6 = r'(?i)\b((?:https?://)?\[[0-9a-f:]+\](?::\d+)?(?:/[\w\-./?%&=+#:]*)?)'

    candidates = []
    candidates += re.findall(pat_domain, text or '')
    candidates += re.findall(pat_ip, text or '')
    candidates += re.findall(pat_ipv6, text or '')

    # Desduplicar preservando orden
    seen = set()
    out = []
    for c in candidates:
        c = _strip_trailing_punct(c)
        if c not in seen:
            out.append(c)
            seen.add(c)
    return out

def _domain_and_type(netloc: str):
    """Devuelve (domain_sin_www, host_type: 'ip'|'domain')."""
    host = netloc.lower()
    if host.startswith('www.'):
        host = host[4:]

    # Separar puerto si existiera
    if ':' in host:
        host = host.split(':', 1)[0]
    # Determinar si es IP
    try:
        ipaddress.ip_address(host)
        return host, 'ip'
    except ValueError:
        return host, 'domain'

def extract_urls(text: str):
    """
    Extrae URLs y devuelve una lista de diccionarios con:
    { 'url': str, 'domain': str, 'host_type': 'ip'|'domain' }
    No realiza llamadas de red.
    """
    results = []
    for raw in _extract_raw_candidates(text or ''):
        norm = _normalize_candidate(raw)
        parsed = urlparse(norm)
        netloc = parsed.netloc or ''
        domain, host_type = _domain_and_type(netloc)
        results.append({
            'url': _strip_trailing_punct(raw),
            'domain': domain,
            'host_type': host_type,
        })
    return results

def has_short_url(text: str) -> int:
    """
    Retorna 1 si el texto contiene al menos una URL de acortador conocido, 0 en caso contrario.
    """
    for info in extract_urls(text or ''):
        if info['domain'] in SHORTENER_DOMAINS:
            return 1
    return 0
