#!/usr/bin/env python3
"""Genera il sito statico in public/ a partire da content/*.html.

Uso:  python3 build.py
Ogni file in content/ ha un'intestazione YAML-like tra --- con title, description, path, nav (opzionale).
Il corpo è HTML puro inserito nel template.
"""
import os, re, shutil, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")
PUBLIC = os.path.join(ROOT, "public")
SITE = "https://vegamente.it"
YEAR = datetime.date.today().year

NAV = [
    ("Cibo", "/cibo/"),
    ("Moda", "/moda/"),
    ("Cosmetici", "/cosmetici/"),
    ("Casa", "/casa/"),
    ("Animali", "/animali/"),
    ("Chi siamo", "/chi-siamo/"),
]

LOGO = """<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 58 V32" stroke="#2F5D50" stroke-width="5" stroke-linecap="round" fill="none"/><path d="M32 36 C31 22 20 14 7 16 C7 30 17 41 32 36 Z" fill="#2F5D50"/><path d="M32 29 C33 15 44 7 57 9 C57 23 47 34 32 29 Z" fill="#C8694A"/></svg>"""

TEMPLATE = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Vegamente</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{site}{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{site}{path}">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/" aria-label="Vegamente, home">{logo}<span class="word">vega<em>mente</em></span></a>
    <nav class="nav" aria-label="Principale">{nav}</nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <a class="logo" href="/" style="font-size:1.2rem">{logo}<span class="word">vega<em>mente</em></span></a>
      <p style="margin-top:10px;max-width:46ch">La guida italiana indipendente a tutto ciò che è vegan: cibo, moda, cosmetici e casa. Recensioni verificate, nessuna sponsorizzazione nascosta.</p>
      <p>© {year} Vegamente · P.IVA [DA INSERIRE]</p>
    </div>
    <div>
      <h4>Categorie</h4>
      <ul><li><a href="/cibo/">Cibo</a></li><li><a href="/moda/">Moda e scarpe</a></li><li><a href="/cosmetici/">Cosmetici</a></li><li><a href="/casa/">Casa e pulizia</a></li><li><a href="/animali/">Animali domestici</a></li></ul>
    </div>
    <div>
      <h4>Vegamente</h4>
      <ul><li><a href="/chi-siamo/">Chi siamo</a></li><li><a href="/come-guadagniamo/">Come guadagniamo</a></li><li><a href="/contatti/">Contatti</a></li><li><a href="/privacy/">Privacy</a></li><li><a href="/cookie/">Cookie</a></li></ul>
    </div>
  </div>
</footer>
<div class="cookie" role="dialog" aria-label="Consenso cookie">
  <p>Usiamo solo cookie tecnici. Con il tuo consenso attiviamo statistiche anonime per migliorare il sito. <a href="/cookie/">Dettagli</a></p>
  <button class="ok" type="button">Accetto</button>
  <button class="no" type="button">Solo necessari</button>
</div>
<script src="/assets/site.js"></script>
</body>
</html>
"""

def parse(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, m.group(2)

def nav_html(current):
    out = []
    for label, href in NAV:
        cls = ' class="active"' if href == current else ""
        out.append(f'<a href="{href}"{cls}>{label}</a>')
    return "".join(out)

def build():
    if os.path.exists(PUBLIC):
        shutil.rmtree(PUBLIC)
    os.makedirs(PUBLIC)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(PUBLIC, "assets"))
    pages = []
    for name in sorted(os.listdir(CONTENT)):
        if not name.endswith(".html"):
            continue
        with open(os.path.join(CONTENT, name), encoding="utf-8") as f:
            meta, body = parse(f.read())
        path = meta["path"]
        html = TEMPLATE.format(
            title=meta["title"], description=meta["description"], path=path,
            site=SITE, logo=LOGO, nav=nav_html(path), body=body, year=YEAR,
        )
        out_dir = os.path.join(PUBLIC, path.strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
        pages.append(path)
    # sitemap + robots
    with open(os.path.join(PUBLIC, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in pages:
            f.write(f"  <url><loc>{SITE}{p}</loc></url>\n")
        f.write("</urlset>\n")
    with open(os.path.join(PUBLIC, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Generate {len(pages)} pagine in public/")

if __name__ == "__main__":
    build()
