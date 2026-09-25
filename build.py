import re, html, pathlib
D = pathlib.Path.home()/"Library/CloudStorage/GoogleDrive-hackerfrik1@gmail.com/My Drive/Fokus App"
NAME, ADDR, MAIL, STAND = "[Vor- und Nachname]", "[Straße, Hausnummer, PLZ Ort]", "[E-Mail-Adresse]", "26. September 2026"

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", s)

def md(path, shift=0):
    t = path.read_text(encoding="utf-8")
    t = t.split("\n---\n", 1)[1]                      # Bearbeitungshinweis am Anfang weg
    t = re.sub(r"\*\*Stand:\*\*.*\n", "", t)
    out, para, lst = [], [], False
    def flush():
        nonlocal para
        if para: out.append("<p>"+inline(" ".join(para))+"</p>"); para = []
    for l in t.splitlines():
        if l.startswith("## "):
            flush(); out.append(f"<h{2+shift}>{inline(l[3:])}</h{2+shift}>")
        elif l.startswith("- "):
            flush()
            if not lst: out.append("<ul>"); lst = True
            out.append("<li>"+inline(l[2:])+"</li>")
        else:
            if lst and not l.startswith("- "): out.append("</ul>"); lst = False
            if not l.strip(): flush()
            else: para.append(l.strip())
    flush()
    if lst: out.append("</ul>")
    body = "\n".join(out)
    # Verantwortlich-Block und Platzhalter ersetzen
    body = re.sub(r"<p>\[Vor- und Nachname\].*?</p>", f"<p>{NAME}<br>{ADDR}<br>E-Mail: {MAIL}</p>", body, flags=re.S)
    return body.replace("[E-Mail-Adresse]", MAIL)

CSS = """:root{--bg:#fff;--fg:#1c1c1e;--mut:#6b6b70;--acc:#2f6f4f;--line:#e4e4e7}
@media(prefers-color-scheme:dark){:root{--bg:#141416;--fg:#ececee;--mut:#9a9aa0;--acc:#6fcf97;--line:#2a2a2e}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.6 system-ui,-apple-system,sans-serif}
main,header,footer{max-width:42rem;margin:0 auto;padding:0 16px}header{padding-top:24px;display:flex;gap:16px;flex-wrap:wrap;align-items:baseline;justify-content:space-between}
header a.logo{font-weight:700;font-size:1.2rem;color:var(--fg);text-decoration:none}nav a{margin-right:14px}
a{color:var(--acc)}h1{font-size:2rem;line-height:1.2;margin:1.5rem 0 .5rem}h2{margin-top:2rem}h3{margin-top:1.5rem}
.lead{font-size:1.2rem;color:var(--mut)}.card{border:1px solid var(--line);border-radius:12px;padding:4px 18px;margin:1.2rem 0}
footer{padding:32px 16px;color:var(--mut);font-size:.9rem;border-top:1px solid var(--line);margin-top:3rem}code{font-size:.9em}"""

def page(fn, title, body):
    pathlib.Path(fn).write_text(f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<meta name="description" content="Plan A: Bildschirmzeit-Begrenzung ohne Konto, ohne Server, ohne Tracking.">
<style>{CSS}</style></head><body>
<header><a class="logo" href="index.html">Plan A</a><nav><a href="datenschutz.html">Datenschutz</a><a href="impressum.html">Impressum</a></nav></header>
<main>{body}</main>
<footer>© 2026 {NAME} · <a href="datenschutz.html">Datenschutz</a> · <a href="impressum.html">Impressum</a></footer>
</body></html>""", encoding="utf-8")

page("index.html", "Plan A", f"""<h1>Plan A</h1>
<p class="lead">Weniger Bildschirmzeit, ohne dass jemand mitliest. Plan A sperrt Apps nach deinen Regeln und gibt sie frei, wenn du dein Ziel erreicht hast.</p>
<div class="card"><h2>Ohne Konto, ohne Server</h2>
<p>Alle Einstellungen bleiben auf deinem Gerät. Es gibt keine Anmeldung, kein Tracking und keine Werbung. Die Android-App hat nicht einmal eine Internet-Berechtigung.</p></div>
<div class="card"><h2>Für iPhone und Android</h2>
<p>Die App befindet sich in der Testphase. Die Store-Links folgen mit der Veröffentlichung.</p></div>
<p>Fragen oder Rückmeldung: <a href="mailto:{MAIL}">{MAIL}</a></p>
<p><a href="datenschutz.html">Datenschutzerklärung</a></p>""")

page("datenschutz.html", "Datenschutzerklärung – Plan A", f"""<h1>Datenschutzerklärung</h1>
<p class="lead">Stand: {STAND}. Sie gilt für Plan A auf iOS und auf Android.</p>
<p><a href="#ios">iOS</a> · <a href="#android">Android</a></p>
<section id="ios"><h2 style="font-size:1.6rem">Plan A für iOS</h2>{md(D/"iOS App Store/02 Datenschutzerklaerung.md",1)}</section>
<section id="android"><h2 style="font-size:1.6rem">Plan A für Android</h2>{md(D/"Android Play Store/02 Datenschutzerklaerung-Android.md",1)}</section>""")

page("impressum.html", "Impressum – Plan A", f"""<h1>Impressum</h1>
<p>Angaben gemäß § 5 DDG</p><p>{NAME}<br>{ADDR}</p><p>E-Mail: {MAIL}</p>""")
