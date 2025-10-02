
import re
from urllib.parse import urlparse

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "buff.ly", "is.gd", "cutt.ly"
}

IPV4_RE = re.compile(r"^(?:\d{1,3}\.){3}\d{1,3}$")

def _strip_port(netloc: str) -> str:
    return netloc.split(":")[0].lower()

def extract_urls(text: str):
    if not text:
        return []
    # simple URL regex for http/https
    pattern = re.compile(r"(https?://[^\s\)\]\}\,]+)", re.IGNORECASE)
    urls = []
    for m in pattern.finditer(text):
        raw = m.group(1).rstrip(").],")
        urls.append(raw)
    return urls

def domain_from_netloc(netloc: str) -> str:
    netloc = _strip_port(netloc)
    if IPV4_RE.match(netloc):
        return netloc
    parts = netloc.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return netloc

def normalize_url(url: str):
    p = urlparse(url)
    netloc = _strip_port(p.netloc)
    domain = domain_from_netloc(netloc)
    host_type = "ip" if IPV4_RE.match(netloc) else "domain"
    return {
        "scheme": p.scheme or "http",
        "netloc": netloc,
        "domain": domain,
        "host_type": host_type,
        "path": p.path
    }

def is_short_url(url: str) -> int:
    try:
        netloc = _strip_port(urlparse(url).netloc)
    except Exception:
        return 0
    return 1 if netloc in SHORTENERS else 0

def looks_like_brand(domain: str, brand_domain: str) -> int:
    """
    Very lightweight homograph-like heuristic:
    - normalize digits/letters pairs: 0->o, 1->l, 3->e, 5->s
    - collapse multiple hyphens
    - compare base domain (last two labels)
    """
    def _norm(s: str) -> str:
        s = s.lower()
        s = s.replace("0","o").replace("1","l").replace("3","e").replace("5","s")
        while "--" in s:
            s = s.replace("--","-")
        return s
    d = _norm(domain_from_netloc(domain))
    b = _norm(domain_from_netloc(brand_domain))
    return 1 if d == b else 0
