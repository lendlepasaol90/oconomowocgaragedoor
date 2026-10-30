#!/usr/bin/env python3
"""Static site generator for oconomowocgaragedoor.com

Edit SITE below (phone, email, form endpoint, logo, favicon), then run:  python3 build.py
Output goes to ./public (deployed as static assets on Cloudflare Workers).
Copy lives in ./content/home.json and ./content/services/<slug>.json
"""
import json, html
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "public"
CONTENT = ROOT / "content"

SITE = {
    "name": "Oconomowoc Garage Door",
    "domain": "https://oconomowocgaragedoor.com",
    "phone": "(262) 000-0000",          # TODO: replace with the real number
    "phone_href": "tel:+12620000000",    # TODO: replace with the real number
    "email": "hello@oconomowocgaragedoor.com",  # TODO: confirm
    "city": "Oconomowoc", "state": "WI", "zip": "53066",
    "hours": "Mon–Sat 7am–7pm",
    "form_endpoint": "",   # e.g. https://formspree.io/f/xxxx  (blank = on-page confirmation only)
    "logo": "/images/logo.webp",  # 2x version at /images/logo@2x.webp (blank = text wordmark)
    "logo_footer": "",     # optional light/white version for the dark footer
    "favicon": True,       # set True once favicon.ico, favicon-32.png, apple-touch-icon.png are in /public
}
HOME_TITLE = "Same Day Garage Door Repair & Installation in Oconomowoc, WI"

CATS = ["Service & Repair", "Garage Doors", "Garage Door Openers"]
CAT_KEY = {"Service & Repair": "repair", "Garage Doors": "doors", "Garage Door Openers": "openers"}

# slug, nav name, category, card blurb, primary image, secondary image
SERVICES = [
    ("garage-door-repairs", "Garage Door Repair", "Service & Repair", "Noisy, stuck, crooked or slow. We trace the real cause and fix it properly the first time.", "garage-door-repair-oconomowoc", "technician-garage-door-panels"),
    ("same-day-garage-door-repair-service", "Emergency Repair", "Service & Repair", "Door stuck open or car trapped inside? Call early and we work to get you moving today.", "same-day-garage-door-repair-winter", "snowy-tudor-home-garage"),
    ("broken-garage-door-springs-repair", "Spring Replacement", "Service & Repair", "Torsion and extension springs sized to your door's weight and balanced by hand.", "garage-door-spring-closeup", "technician-drilling-track"),
    ("garage-door-cable-repair", "Cable Replacement", "Service & Repair", "Frayed or snapped lift cables replaced and wound evenly so the door rises level.", "garage-door-cable-replacement", "garage-door-cable-hardware"),
    ("roller-replacement-repair", "Roller Replacement", "Service & Repair", "Sealed-bearing nylon rollers that end the grinding and take strain off your opener.", "garage-door-roller-track", "technician-ladder-garage"),
    ("garage-door-panel-replacement", "Panel Replacement", "Service & Repair", "Dented or cracked section? We match the panel and restore a straight, sealed door.", "garage-door-panel-replacement", "white-garage-door-modern-home"),
    ("garage-door-track-replacement", "Track Replacement", "Service & Repair", "Bent or misaligned tracks straightened or replaced and brackets re-anchored.", "garage-door-track-replacement", "garage-interior-opener"),
    ("garage-door-drum-replacement", "Drum Replacement", "Service & Repair", "Worn cable drums swapped and set evenly so both sides of the door lift in balance.", "garage-door-drum-replacement", "garage-door-pulley-hardware"),
    ("new-garage-door-installation", "Garage Door Installation", "Garage Doors", "New insulated doors measured, installed, sealed and balanced, with the old door hauled away.", "new-garage-door-installation-oconomowoc", "three-car-garage-red-doors"),
    ("garage-door-materials", "Garage Door Materials", "Garage Doors", "Steel, wood, composite, aluminum and glass, with straight talk on what survives Wisconsin.", "glass-aluminum-garage-door", "wood-look-garage-door"),
    ("garage-door-styles", "Garage Door Styles", "Garage Doors", "Raised panel, carriage house, modern flush or full-view glass, matched to your home.", "brick-craftsman-three-car-garage", "modern-farmhouse-wood-garage-door"),
    ("custom-garage-doors", "Custom Garage Doors", "Garage Doors", "Custom sizes, tall boat and RV doors, real wood, arched tops and one-of-a-kind finishes.", "custom-arched-garage-doors-stone", "wood-carriage-doors-stone"),
    ("new-garage-door-opener-installation", "Opener Installation", "Garage Door Openers", "Quiet belt, chain and wall-mount openers with smart control and battery backup.", "garage-door-opener-installation", "garage-interior-opener"),
    ("garage-door-opener-repair", "Opener Repair", "Garage Door Openers", "Remotes, keypads, sensors, gears and boards diagnosed and repaired on the spot.", "garage-door-opener-repair-remote", "opener-rail-repair"),
]
SVC = {s[0]: s for s in SERVICES}
NAV_LABEL = {"Service & Repair": "Repair", "Garage Doors": "Garage Doors", "Garage Door Openers": "Openers"}

e = html.escape

# ---------------------------------------------------------------- icons
def svg(p, sw=1.7, fill="none"):
    return f'<svg viewBox="0 0 24 24" fill="{fill}" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

ICON = {
    "phone": svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>', 2),
    "tick": svg('<path d="M20 6 9 17l-5-5"/>', 3),
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>', 2),
    "chev": '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
    "clock": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    "tag": svg('<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>'),
    "shield": svg('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
    "tool": svg('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>'),
    "snow": svg('<path d="M12 2v20M4.9 4.9l14.2 14.2M2 12h20M4.9 19.1 19.1 4.9"/>'),
    "home": svg('<path d="M3 10.5 12 3l9 7.5V21H3z"/><path d="M7 21v-7h10v7M7 17.5h10"/>'),
    "pin": svg('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>', 1.8),
    "mail": svg('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>', 1.8),
    "wave": svg('<path d="M2 12c2.5-3 5-3 7.5 0s5 3 7.5 0 3.5-2 5-1"/><path d="M2 17c2.5-3 5-3 7.5 0s5 3 7.5 0 3.5-2 5-1"/><path d="M2 7c2.5-3 5-3 7.5 0s5 3 7.5 0 3.5-2 5-1"/>'),
    "bolt": svg('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'),
    "spark": svg('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>'),
    "leaf": svg('<path d="M11 20A7 7 0 0 1 4 13c0-6 7-10 16-10 0 9-4 16-10 16"/><path d="M4 21c4-4 7-7 10-10"/>'),
    "sun": svg('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>'),
    "star": svg('<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>', 0, "currentColor"),
}
SEASON_ICON = {"Winter": "snow", "Spring": "leaf", "Summer": "sun", "Fall": "leaf"}
SEASON_IMG = {"Winter": "winter-snow-driveway-home", "Spring": "spring-flowers-garage", "Summer": "summer-home-garage", "Fall": "autumn-home-garage"}

MARK = '''<svg class="mark" viewBox="0 0 48 48" aria-hidden="true"><rect x="1" y="1" width="46" height="46" rx="14" fill="var(--lake)"/><path d="M10 21 24 11l14 10v16H10z" fill="none" stroke="#fff" stroke-width="2.6" stroke-linejoin="round"/><path d="M15 37V25h18v12M15 29h18M15 33h18" stroke="#fff" stroke-width="2" fill="none"/><path d="M6 41c3-2 6-2 9 0s6 2 9 0 6-2 9 0 6 2 9 0" stroke="var(--sunset)" stroke-width="2.4" fill="none" stroke-linecap="round"/></svg>'''

def phone_btn(cls="btn btn--primary", label=None):
    return f'<a class="{cls}" href="{SITE["phone_href"]}" data-magnetic><span class="btn__ico">{ICON["phone"]}</span><span>{e(label or SITE["phone"])}</span></a>'

def arrow_btn(href, label, cls="btn btn--ghost"):
    return f'<a class="{cls}" href="{href}" data-magnetic><span>{e(label)}</span><span class="btn__arrow">{ICON["arrow"]}</span></a>'

def tick_li(text):
    return f'<li><span class="tick">{ICON["tick"]}</span>{e(text)}</li>'

def h2(a, b, cls=""):
    return f'<h2 class="h2 {cls}" data-words>{e(a)} <em>{e(b)}</em></h2>'

def kicker(t, center=False):
    return f'<p class="kicker{" kicker--c" if center else ""}" data-reveal="up"><span class="kicker__dot"></span>{e(t)}</p>'

def img(name, alt, cls="", eager=False, extra=""):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="/images/{name}.webp" alt="{e(alt)}" {load} class="{cls}" {extra}>'

def bg(name, cls="bgimg"):
    return f'<div class="{cls}" aria-hidden="true"><img src="/images/{name}.webp" alt="" loading="lazy" decoding="async" data-parallax="0.08"></div>'

def logo(footer=False):
    src = SITE["logo_footer"] if footer and SITE["logo_footer"] else SITE["logo"]
    if src:
        cls = "logo logo--footer" if footer else "logo"
        return f'<a class="{cls}" href="/" aria-label="{e(SITE["name"])} home"><img src="{src}" srcset="{src} 1x, {src.replace(".webp", "@2x.webp")} 2x" alt="{e(SITE["name"])} logo" width="520" height="250" class="logo__img"{"" if footer else " fetchpriority=" + chr(34) + "high" + chr(34)}></a>'
    return f'<a class="logo" href="/" aria-label="{e(SITE["name"])} home">{MARK}<span class="logo__txt"><b>Oconomowoc</b><small>Garage Door</small></span></a>'

# ---------------------------------------------------------------- chrome
def nav_html(current=None):
    groups = []
    for cat in CATS:
        items = "".join(
            f'<li><a href="/{s[0]}/"{" aria-current=page" if s[0]==current else ""}><span class="dd__thumb">{img(s[4], "")}</span><span><b>{e(s[1])}</b><small>{e(s[3][:58].rsplit(" ",1)[0])}…</small></span></a></li>'
            for s in SERVICES if s[2] == cat)
        groups.append(f'<li class="has-dd"><button type="button" aria-haspopup="true" aria-expanded="false">{e(NAV_LABEL[cat])}{ICON["chev"]}</button><ul class="dd">{items}</ul></li>')
    return ('<ul class="nav" id="nav"><li><a href="/">Home</a></li>' + "".join(groups) +
            '<li><a href="/#service-area">Service Area</a></li><li><a href="/#faq">FAQ</a></li></ul>')

def header(current=None):
    return f'''<div class="progress" aria-hidden="true"></div>
<div class="topbar"><div class="wrap"><span class="topbar__live"><i></i>Same-day appointments across Oconomowoc &amp; Lake Country</span><span class="hide-sm">{e(SITE["hours"])} · <a href="{SITE["phone_href"]}">{e(SITE["phone"])}</a></span></div></div>
<header class="header"><div class="wrap header__in">
{logo()}
<nav aria-label="Main">{nav_html(current)}</nav>
<div class="header__cta">{phone_btn("btn btn--primary btn--sm")}<button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button></div>
</div></header>'''

def quote_form(h="Get Your Free Quote", service=None):
    opts = "".join(f'<option{" selected" if service==s[0] else ""}>{e(s[1])}</option>' for s in SERVICES) + "<option>Not sure yet</option>"
    ep = f' data-endpoint="{e(SITE["form_endpoint"])}"' if SITE["form_endpoint"] else ""
    return f'''<aside class="quote" id="quote" aria-labelledby="quote-h" data-reveal="rise">
<div class="quote__head"><span class="quote__badge">{ICON["bolt"]}Fast Reply</span><h2 id="quote-h">{e(h)}</h2><p>Tell us what the door is doing. A local technician calls back to set a time.</p></div>
<form class="quote-form" novalidate{ep}>
<div class="hp" aria-hidden="true"><label>Leave this empty<input name="company" tabindex="-1" autocomplete="off"></label></div>
<div class="row2"><div class="field"><input id="q-name" name="name" autocomplete="name" placeholder=" " required><label for="q-name">Full Name</label></div>
<div class="field"><input id="q-phone" name="phone" type="tel" autocomplete="tel" placeholder=" " required><label for="q-phone">Phone</label></div></div>
<div class="row2"><div class="field"><input id="q-zip" name="zip" inputmode="numeric" autocomplete="postal-code" placeholder=" " required><label for="q-zip">ZIP Code</label></div>
<div class="field field--select"><select id="q-svc" name="service">{opts}</select><label for="q-svc">Service</label></div></div>
<div class="field"><textarea id="q-msg" name="message" rows="2" placeholder=" "></textarea><label for="q-msg">What's the door doing? (optional)</label></div>
<button class="btn btn--primary btn--block" type="submit"><span>Request My Free Quote</span><span class="btn__arrow">{ICON["arrow"]}</span></button>
<p class="quote__note">{ICON["shield"]}No obligation. Price quoted before any work starts.</p>
</form>
<div class="quote__done" role="status"><span class="tick">{ICON["tick"]}</span><h3>Request Received</h3><p>Thanks. An Oconomowoc technician will call you shortly to set your appointment window.</p></div>
</aside>'''

def trust_card():
    items = [("clock", "Call Early", "Same-day visits"), ("tag", "Upfront", "Price before work"), ("pin", "Local", "Lake Country team")]
    return '<ul class="trust" data-reveal="up">' + "".join(f'<li><span>{ICON[i]}</span><b>{e(a)}</b><small>{e(b)}</small></li>' for i, a, b in items) + '</ul>'

MAP_SRC = "https://www.google.com/maps?q=Oconomowoc,+WI+53066&z=12&output=embed"

def footer():
    def col(cat):
        return "".join(f'<li><a href="/{s[0]}/">{e(s[1])}</a></li>' for s in SERVICES if s[2] == cat)
    return f'''<footer class="footer">
<div class="footer__wave" aria-hidden="true"><svg viewBox="0 0 1440 80" preserveAspectRatio="none"><path class="w1" style="--per:-560px" d="{wave_path(36, 20, 560, 80)}"/><path class="w2" style="--per:-720px" d="{wave_path(50, 14, 720, 80)}"/></svg></div>
<div class="footer__bg" aria-hidden="true"><img src="/images/lake-jetty-twilight.webp" alt="" loading="lazy"></div>
<div class="wrap">
<div class="footer__top" data-reveal="up"><h2 class="footer__big">Lake Country's <em>garage door</em> team.</h2>{phone_btn("btn btn--light", "Call " + SITE["phone"])}</div>
<div class="footer__grid">
<div class="footer__brand">{logo(True)}
<p>Garage door repair, new doors and opener service for homes on Lac La Belle, Fowler Lake, Oconomowoc Lake and across Lake Country.</p>
<ul class="footer__contact"><li>{ICON["phone"]}<a href="{SITE["phone_href"]}">{e(SITE["phone"])}</a></li><li>{ICON["mail"]}<a href="mailto:{SITE["email"]}">{e(SITE["email"])}</a></li><li>{ICON["pin"]}Oconomowoc, WI 53066</li><li>{ICON["clock"]}{e(SITE["hours"])}</li></ul></div>
<div><h3>Service &amp; Repair</h3><ul>{col("Service & Repair")}</ul></div>
<div><h3>Garage Doors</h3><ul>{col("Garage Doors")}</ul><h3 class="mt">Openers</h3><ul>{col("Garage Door Openers")}</ul></div>
<div class="footer__map"><h3>Find Us In Oconomowoc</h3><div class="map"><iframe src="{MAP_SRC}" title="Map of Oconomowoc, Wisconsin" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
<p class="map__cap">{ICON["pin"]}Serving Oconomowoc, WI 53066 &amp; nearby communities</p></div>
</div>
<div class="footer__bar"><span>© <span data-year>2026</span> {e(SITE["name"])}. All Rights Reserved.</span><span><a href="/">Home</a> · <a href="/#service-area">Service Area</a> · <a href="/#faq">FAQ</a> · <a href="/sitemap.xml">Sitemap</a></span></div>
</div></footer>
<a class="totop" href="#main" aria-label="Back to top"><svg viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="20" class="totop__track"/><circle cx="22" cy="22" r="20" class="totop__ring"/></svg>{ICON["arrow"]}</a>
<div class="callbar">{phone_btn("btn btn--primary", "Call Now")}<a class="btn btn--ghost" href="#quote">Free Quote</a></div>'''

def page(title, desc, path, body, current=None, schema=None, image="oconomowoc-garage-door-hero"):
    url = SITE["domain"] + path
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    fav = '''<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">''' if SITE["favicon"] else ""
    return f'''<!doctype html>
<html lang="en" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#4a7c94">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE["domain"]}/images/{image}.webp">
{fav}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400;1,9..144,500&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="/images/{image}.webp">
<link rel="stylesheet" href="/assets/css/site.css">
{ld}
</head><body>
<a class="skip" href="#main">Skip to content</a>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="/assets/js/site.js" defer></script>
</body></html>'''

def wave_path(y, amp, per, h=120):
    half = per / 2
    d = f"M{-per} {y}"
    x = -per
    while x < 1440 + per:
        d += f" q{half/2:.0f} {-amp} {half:.0f} 0 t{half:.0f} 0"
        x += per
    return d + f" V{h} H{-per} Z"

def waves(cls=""):
    return f'''<div class="waves {cls}" aria-hidden="true"><svg viewBox="0 0 1440 120" preserveAspectRatio="none"><path class="w1" style="--per:-480px" d="{wave_path(60, 26, 480)}"/><path class="w2" style="--per:-640px" d="{wave_path(78, 18, 640)}"/><path class="w3" style="--per:-720px" d="{wave_path(96, 12, 720)}"/></svg></div>'''

def ticker(words):
    spans = "".join(f"<span>{e(w)}</span><i>{ICON['wave']}</i>" for w in words) * 2
    return f'<div class="ticker" aria-hidden="true"><div class="ticker__track">{spans}</div></div>'

def faq_html(faqs):
    out = []
    for i, f in enumerate(faqs):
        out.append(f'<details class="faq__item" data-reveal="up" style="--d:{i*0.04:.2f}s"><summary><span class="faq__n">{i+1:02d}</span><span class="faq__q">{e(f["q"])}</span><span class="faq__plus" aria-hidden="true"></span></summary><div class="faq__a"><p>{e(f["a"])}</p></div></details>')
    return '<div class="faq">' + "".join(out) + "</div>"

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]}

def cta(title, text, img_name="calm-lake-pier-dusk"):
    return f'''<section class="cta-sec"><div class="wrap"><div class="cta" data-reveal="arch">
<div class="cta__bg" aria-hidden="true"><img src="/images/{img_name}.webp" alt="" loading="lazy" data-parallax="0.1"></div>
<div class="cta__in">{kicker("Oconomowoc Garage Door")}<h2 class="h2" data-words>{e(title)}</h2><p>{e(text)}</p>
<div class="actions">{phone_btn("btn btn--light", "Call " + SITE["phone"])}{arrow_btn("#quote", "Request A Free Quote", "btn btn--glass")}</div></div>
</div></div></section>'''

def svc_card(s, i=0, big=False):
    tag = NAV_LABEL[s[2]]
    return f'''<a class="svc{" svc--big" if big else ""}" href="/{s[0]}/" data-cat="{CAT_KEY[s[2]]}" data-glow data-reveal="up" style="--d:{(i%4)*0.06:.2f}s">
<div class="svc__img">{img(s[4], s[1] + " in Oconomowoc, WI")}</div>
<div class="svc__body"><span class="svc__tag">{e(tag)}</span><h3>{e(s[1])}</h3><p>{e(s[3])}</p><span class="svc__more">Learn more <span class="btn__arrow">{ICON["arrow"]}</span></span></div></a>'''

BUSINESS = {
    "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": SITE["name"],
    "url": SITE["domain"], "telephone": SITE["phone"], "email": SITE["email"], "image": SITE["domain"] + "/images/oconomowoc-garage-door-hero.webp",
    "address": {"@type": "PostalAddress", "addressLocality": "Oconomowoc", "addressRegion": "WI", "postalCode": "53066", "addressCountry": "US"},
    "geo": {"@type": "GeoCoordinates", "latitude": 43.1117, "longitude": -88.4993},
    "areaServed": ["Oconomowoc", "Lac La Belle", "Oconomowoc Lake", "Summit", "Okauchee", "Delafield", "Nashotah", "Hartland", "Dousman", "Ixonia", "Merton", "Chenequa", "Watertown"],
    "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
}

# ---------------------------------------------------------------- homepage
def home():
    H = json.loads((CONTENT / "home.json").read_text())
    ab = H["about"]
    bento_order = ["garage-door-repairs", "broken-garage-door-springs-repair", "same-day-garage-door-repair-service", "new-garage-door-installation"]
    cards = "".join(svc_card(SVC[k], i, big=(i == 0)) for i, k in enumerate(bento_order))
    cards += "".join(svc_card(s, i) for i, s in enumerate([s for s in SERVICES if s[0] not in bento_order]))
    cards += f'''<div class="svc-cta" data-reveal="up"><div class="svc-cta__bg" aria-hidden="true">{img("lac-la-belle-lake-morning", "")}</div><div><p class="kicker kicker--light"><span class="kicker__dot"></span>Not Sure What's Wrong?</p><h3>Describe the noise or the symptom. We'll tell you what it likely is and what it costs to fix.</h3></div><div class="actions">{phone_btn("btn btn--light", "Call " + SITE["phone"])}{arrow_btn("#quote", "Free Quote", "btn btn--glass")}</div></div>'''

    calls = "".join(f'''<article class="call" data-glow data-reveal="up" style="--d:{i*0.08:.2f}s"><span class="call__n">0{i+1}</span><p class="call__label">{e(c["label"])}</p><h3>{e(c["title"])}</h3><p>{e(c["text"])}</p>{arrow_btn("/" + c["slug"] + "/", "How we fix it", "link")}</article>''' for i, c in enumerate(H["commonCalls"]))

    ficons = ["clock", "tag", "shield", "tool", "snow", "home"]
    feats = "".join(f'<div class="feat" data-glow data-reveal="up" style="--d:{(i%3)*0.07:.2f}s"><span class="feat__ico">{ICON[ficons[i%6]]}</span><h3>{e(f["title"])}</h3><p>{e(f["text"])}</p></div>' for i, f in enumerate(H["features"]))

    steps = "".join(f'<li class="step" data-reveal="up" style="--d:{i*0.1:.2f}s"><span class="step__n">{i+1}</span><div><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></div></li>' for i, s in enumerate(H["steps"]))

    rr = H["repairReplace"]
    def plan(p, cls, link, label):
        return f'''<div class="plan {cls}" data-glow data-reveal="up"><h3>{e(p["title"])}</h3><p>{e(p["note"])}</p><ul class="checks">{"".join(tick_li(b) for b in p["bullets"])}</ul>{arrow_btn(link, label, "btn btn--ghost btn--sm")}</div>'''

    seasons = "".join(f'''<article class="season" data-reveal="up" style="--d:{i*0.08:.2f}s"><div class="season__img">{img(SEASON_IMG.get(s["label"], "summer-home-garage"), s["label"] + " garage door care in Oconomowoc")}<span class="season__chip">{ICON[SEASON_ICON.get(s["label"], "sun")]}{e(s["label"])}</span></div><div class="season__body"><h3>{e(s["title"])}</h3><p>{e(s["text"])}</p></div></article>''' for i, s in enumerate(H["seasons"]))

    tu = H["tuneup"]; ar = H["area"]; nd = H["newDoors"]; fw = H["fullwidth"]

    body = f'''
<section class="hero">
<div class="hero__bg" aria-hidden="true"><img src="/images/lac-la-belle-lake-morning.webp" alt="" fetchpriority="high" data-parallax="0.18"></div>
<div class="hero__blob hero__blob--a" aria-hidden="true"></div><div class="hero__blob hero__blob--b" aria-hidden="true"></div>
<div class="wrap hero__grid">
<div class="hero__copy">
{kicker(H["heroKicker"])}
<h1 class="h1" data-words>Same Day Garage Door Repair &amp; Installation in <em>Oconomowoc, WI</em></h1>
<p class="hero__intro" data-reveal="up">{e(H["heroIntro"])}</p>
<ul class="hero__checks" data-reveal="up">{tick_li("Same-day repairs")}{tick_li("Price before we start")}{tick_li("All makes & models")}</ul>
<div class="actions" data-reveal="up">{phone_btn("btn btn--primary", "Call " + SITE["phone"])}{arrow_btn("#services", "Explore Services")}</div>
<div class="hero__photo" data-reveal="arch"><img src="/images/oconomowoc-garage-door-hero.webp" alt="Two-story Lake Country home with a pair of dark insulated garage doors" fetchpriority="high"><span class="hero__chip"><b data-count="14">14</b><small>garage door services<br>one local team</small></span></div>
</div>
<div class="hero__side">{quote_form()}{trust_card()}</div>
</div>
{waves()}
</section>
{ticker(["Garage Door Repair", "Spring Replacement", "Opener Installation", "Same Day Service", "New Garage Doors", "Oconomowoc, WI", "Lake Country"])}

<section class="sec" id="about"><div class="wrap split split--top">
<div class="collage sticky" data-reveal="arch">
<div class="collage__main">{img("oconomowoc-garage-door-technician", "Oconomowoc Garage Door technician standing beside a garage door and service van")}</div>
<div class="collage__inset" data-parallax-el="-0.06">{img("garage-door-spring-closeup", "Close-up of a garage door spring and hook")}</div>
<div class="seal" aria-hidden="true"><svg viewBox="0 0 200 200"><defs><path id="ring" d="M100,100 m-78,0 a78,78 0 1,1 156,0 a78,78 0 1,1 -156,0"/></defs><text><textPath href="#ring">Oconomowoc · Lake Country · Same Day Service ·</textPath></text></svg><span>{ICON["wave"]}</span></div>
</div>
<div>
{kicker(ab["eyebrow"])}
{h2(ab["h2a"], ab["h2b"])}
<div class="prose" data-reveal="up">{"".join(f"<p>{e(p)}</p>" for p in ab["paragraphs"])}</div>
<div class="stats" data-reveal="up"><div><b data-count="14">14</b><small>Door &amp; opener services</small></div><div><b data-count="3">3</b><small>Lakes in the city</small></div><div><b data-count="13">13</b><small>Communities served</small></div></div>
</div>
</div></section>

<section class="sec sec--tint has-bg" id="services">{bg("lake-jetty-twilight")}<div class="wrap">
<div class="head">{kicker("What We Do")}{h2("Every Part Of The Door,", "From Springs To Smart Openers")}
<p class="lead" data-reveal="up">Fourteen services, one local team. A single snapped cable or a full new door and opener package, the same technicians handle it from the first call to the final safety test.</p></div>
<div class="filters" role="tablist" data-reveal="up"><button class="filter is-on" role="tab" aria-selected="true" data-cat="all">All Services</button><button class="filter" role="tab" aria-selected="false" data-cat="repair">Service &amp; Repair</button><button class="filter" role="tab" aria-selected="false" data-cat="doors">Garage Doors</button><button class="filter" role="tab" aria-selected="false" data-cat="openers">Openers</button></div>
<div class="bento">{cards}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="head head--row"><div>{kicker("The Calls We Get Most")}{h2("Three Problems,", "Handled Fast")}</div>{arrow_btn("/same-day-garage-door-repair-service/", "Emergency Repair", "btn btn--primary btn--sm")}</div>
<div class="calls">{calls}</div>
</div></section>

<section class="full" aria-labelledby="full-h">
<div class="full__bg" aria-hidden="true"><img src="/images/lake-country-pier-sunset.webp" alt="" loading="lazy" data-parallax="0.22"></div>
<div class="wrap full__in">
<p class="kicker kicker--light" data-reveal="up"><span class="kicker__dot"></span>{e(fw["eyebrow"])}</p>
<h2 class="full__title" id="full-h" data-words>{e(fw["title"])}</h2>
<p class="full__text" data-reveal="up">{e(fw["text"])}</p>
<div class="full__stats" data-reveal="up"><div><b>40<small>in</small></b><span>Average yearly snowfall</span></div><div><b>−33<small>°F</small></b><span>Record low temperature</span></div><div><b>3</b><span>Lakes inside city limits</span></div></div>
<div class="actions" data-reveal="up">{phone_btn("btn btn--light", "Call " + SITE["phone"])}{arrow_btn("/broken-garage-door-springs-repair/", "Winter Spring Repair", "btn btn--glass")}</div>
</div>
</section>

<section class="sec sec--sand"><div class="wrap">
<div class="head head--c">{kicker("Why Oconomowoc Calls Us", True)}{h2("Straight Answers, Careful Work", "And Fair Prices")}
<p class="lead" data-reveal="up">A garage door is the largest moving object in most homes. It deserves a technician who takes the time to do it right, explains the work and stands behind it.</p></div>
<div class="feats">{feats}</div>
</div></section>

<section class="sec"><div class="wrap split split--top">
<div class="sticky">
{kicker("How It Works")}{h2("From Your Call", "To A Quiet, Balanced Door")}
<p class="lead" data-reveal="up">No guesswork and no surprise invoices. Here is what happens after you reach out.</p>
<div class="sticky__img" data-reveal="arch">{img("technician-garage-door-panels", "Technician working on the top section of a garage door")}</div>
</div>
<ol class="steps">{steps}</ol>
</div></section>

<section class="sec sec--tint has-bg">{bg("calm-lake-pier-dusk")}<div class="wrap">
<div class="head head--c">{kicker("Repair Or Replace?", True)}{h2(rr["h2a"], rr["h2b"])}<p class="lead" data-reveal="up">{e(rr["intro"])}</p></div>
<div class="plans">{plan(rr["repair"], "", "/garage-door-repairs/", "Garage Door Repair")}{plan(rr["replace"], "plan--alt", "/new-garage-door-installation/", "New Door Installation")}</div>
</div></section>

<section class="sec"><div class="wrap split split--top">
<div>
{kicker("New Garage Doors")}{h2(nd["h2a"], nd["h2b"])}
<div class="prose" data-reveal="up">{"".join(f"<p>{e(p)}</p>" for p in nd["paragraphs"])}</div>
<div class="actions" data-reveal="up">{arrow_btn("/garage-door-styles/", "Browse Door Styles", "btn btn--primary")}{arrow_btn("/garage-door-materials/", "Compare Materials")}</div>
</div>
<div class="gallery sticky" data-reveal="arch">
<figure class="g1">{img("modern-farmhouse-wood-garage-door", "Modern farmhouse with a wood garage door")}</figure>
<figure class="g2">{img("brick-craftsman-three-car-garage", "Brick craftsman home with three raised-panel garage doors")}</figure>
<figure class="g3">{img("glass-aluminum-garage-door", "Full-view aluminum and glass garage door")}</figure>
<span class="gallery__chip"><span class="tick">{ICON["tick"]}</span>Insulated · Custom sizes · Wood-look finishes</span>
</div>
</div></section>

<section class="sec sec--sand"><div class="wrap">
<div class="head">{kicker("Seasonal Care")}{h2("What Lake Country Weather Does", "To Your Garage Door")}
<p class="lead" data-reveal="up">Four real seasons and plenty of lake moisture put steady stress on springs, seals and openers. Here is what to watch for through the year.</p></div>
<div class="seasons">{seasons}</div>
</div></section>

<section class="sec"><div class="wrap split split--top">
<div class="photo-stack" data-reveal="arch">{img("opener-rail-repair", "Technician tightening an opener rail bracket with a drill")}<div class="photo-stack__b">{img("garage-door-roller-track", "Garage door rollers and track inside a new garage")}</div></div>
<div>
{kicker("Annual Tune-Up")}{h2("What's Included In A", "Garage Door Tune-Up")}
<div class="prose" data-reveal="up"><p>{e(tu["intro"])}</p></div>
<ul class="checks checks--2" data-reveal="up">{"".join(tick_li(b) for b in tu["bullets"])}</ul>
<div class="prose" data-reveal="up"><p>{e(tu["outro"])}</p></div>
{arrow_btn("#quote", "Schedule A Tune-Up", "btn btn--primary")}
</div>
</div></section>

<section class="sec sec--deep has-bg" id="service-area">{bg("lake-town-aerial", "bgimg bgimg--deep")}<div class="wrap split">
<div>
<p class="kicker kicker--light" data-reveal="up"><span class="kicker__dot"></span>Service Area</p>
{h2("One Call Covers", "Oconomowoc & Lake Country", "h2--light")}
<div class="prose prose--light" data-reveal="up">{"".join(f"<p>{e(p)}</p>" for p in ar["paragraphs"])}</div>
<ul class="areas">{"".join(f'<li data-reveal="pop" style="--d:{i*0.03:.2f}s">{ICON["pin"]}{e(a)}</li>' for i, a in enumerate(ar["places"]))}</ul>
{arrow_btn("#quote", "Check Availability", "btn btn--light")}
</div>
<div class="area-map" data-reveal="arch"><iframe src="{MAP_SRC}" title="Oconomowoc service area map" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe><span class="area-map__chip">{ICON["pin"]}Oconomowoc, WI 53066</span></div>
</div></section>

<section class="sec" id="faq"><div class="wrap split split--top">
<div class="sticky">{kicker("FAQ")}{h2("Garage Door Questions", "From Oconomowoc Homeowners")}<p class="lead" data-reveal="up">Straight answers to what we hear most. Don't see yours? Call and ask a technician.</p>{phone_btn("btn btn--primary", "Ask A Technician")}</div>
{faq_html(H["faqs"])}
</div></section>

{cta(H["cta"]["title"], H["cta"]["text"])}
'''
    schema = [BUSINESS, faq_schema(H["faqs"])]
    return page(HOME_TITLE,
                "Same-day garage door repair, spring and cable replacement, new garage doors and opener installation in Oconomowoc, WI and Lake Country. Upfront pricing. Free quote.",
                "/", body, schema=schema)

# ---------------------------------------------------------------- service pages
def service_page(d):
    s = SVC[d["slug"]]
    secs = d["sections"]
    def sec(x):
        bl = ""
        if x.get("bullets"):
            bl = f'<ul class="checks{" checks--2" if len(x["bullets"]) > 4 else ""}" data-reveal="up">' + "".join(tick_li(b) for b in x["bullets"]) + "</ul>"
        ps = "".join(f"<p>{e(p)}</p>" for p in x["paragraphs"])
        return f'<div class="block">{kicker(x["eyebrow"])}{h2(x["h2a"], x["h2b"])}<div class="prose" data-reveal="up">{ps}</div>{bl}</div>'

    facts = "".join(f'<div class="fact" data-reveal="up" style="--d:{i*0.06:.2f}s"><span class="fact__ico">{ICON[["clock","bolt","tag","home"][i%4]]}</span><small>{e(q["label"])}</small><b>{e(q["value"])}</b></div>' for i, q in enumerate(d.get("quickFacts", [])))
    ficons = ["tool", "shield", "clock", "snow", "home", "tag"]
    signs = "".join(f'<div class="feat" data-glow data-reveal="up" style="--d:{(i%3)*0.07:.2f}s"><span class="feat__ico">{ICON[ficons[i % 6]]}</span><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></div>' for i, x in enumerate(d["signs"]))
    steps = "".join(f'<li class="step" data-reveal="up" style="--d:{i*0.1:.2f}s"><span class="step__n">{i+1}</span><div><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></div></li>' for i, x in enumerate(d["process"]))
    side_links = "".join(f'<li><a href="/{x[0]}/"{" aria-current=page" if x[0]==s[0] else ""}>{e(x[1])}<span class="btn__arrow">{ICON["arrow"]}</span></a></li>' for x in SERVICES if x[2] == s[2])
    others = [x for x in SERVICES if x[0] != s[0]]
    idx = SERVICES.index(s)
    related = [others[(idx + k) % len(others)] for k in range(3)]
    rel_cards = "".join(svc_card(x, i) for i, x in enumerate(related))
    ln = d.get("localNote", {})

    body = f'''
<section class="hero hero--svc">
<div class="hero__bg" aria-hidden="true"><img src="/images/{s[4]}.webp" alt="" fetchpriority="high" data-parallax="0.18"></div>
<div class="hero__blob hero__blob--a" aria-hidden="true"></div><div class="hero__blob hero__blob--b" aria-hidden="true"></div>
<div class="wrap hero__grid">
<div class="hero__copy">
<ol class="crumbs" data-reveal="up"><li><a href="/">Home</a></li><li><a href="/#services">{e(s[2])}</a></li><li aria-current="page">{e(s[1])}</li></ol>
{kicker(d.get("kicker", s[2]) + " · Oconomowoc, WI")}
<h1 class="h1" data-words>{e(d["h1"].replace(" in Oconomowoc, WI", ""))} <em>in Oconomowoc, WI</em></h1>
<p class="hero__intro" data-reveal="up">{e(d["intro"])}</p>
<ul class="hero__checks" data-reveal="up">{tick_li("Same-day service")}{tick_li("Price before we start")}{tick_li("Safety-tested")}</ul>
<div class="actions" data-reveal="up">{phone_btn("btn btn--primary", "Call " + SITE["phone"])}{arrow_btn("#details", "Read The Details")}</div>
</div>
<div class="hero__side">{quote_form("Get A Free Quote", s[0])}{trust_card()}</div>
</div>
{waves()}
</section>
{ticker([s[1], "Oconomowoc, WI", "Same Day Service", "Upfront Pricing", "Safety Tested", "Lake Country"])}

<section class="facts-sec"><div class="wrap"><div class="facts">{facts}</div></div></section>

<section class="sec" id="details"><div class="wrap layout">
<div class="layout__main">
{sec(secs[0])}
<figure class="wide-img" data-reveal="arch">{img(s[4], d["h1"])}<figcaption>{ICON["pin"]}{e(s[1])} for Oconomowoc &amp; Lake Country homes</figcaption></figure>
{sec(secs[1])}
{sec(secs[2])}
</div>
<aside class="aside">
<div class="aside__pin">
<div class="aside__call"><div class="aside__call-bg" aria-hidden="true"><img src="/images/{s[5]}.webp" alt="" loading="lazy"></div><span class="quote__badge">{ICON["bolt"]}Same-Day Service</span><h3>Need Help Today?</h3><p>Call early for same-day {e(s[1].lower())} anywhere in Oconomowoc and nearby communities.</p>{phone_btn("btn btn--light btn--block")}<a class="btn btn--glass btn--block" href="#quote">Free Quote</a></div>
<div class="aside__box"><h3>{e(s[2])}</h3><ul class="aside__links">{side_links}</ul></div>
</div>
</aside>
</div></section>

<section class="sec sec--tint has-bg">{bg("lake-jetty-twilight")}<div class="wrap">
<div class="head head--row"><div>{kicker("What To Look For")}{h2(d["signsHeading"][0], d["signsHeading"][1])}</div>{arrow_btn("#quote", "Get A Free Quote", "btn btn--primary btn--sm")}</div>
<div class="feats">{signs}</div>
</div></section>

<section class="sec"><div class="wrap split split--top">
<div class="sticky">{kicker("Our Process")}{h2("How We Handle", s[1])}
<div class="sticky__img" data-reveal="arch">{img(s[5], s[1] + " work at an Oconomowoc home")}</div></div>
<ol class="steps">{steps}</ol>
</div></section>

<section class="sec sec--sand"><div class="wrap duo">
<div>{sec(secs[3])}</div>
<div>{sec(secs[4])}</div>
</div></section>

<section class="sec local-sec"><div class="wrap"><div class="local" data-reveal="arch">
<div class="local__img">{img("lake-town-aerial", "Aerial view of a lake town in autumn")}</div>
<div class="local__body"><p class="kicker"><span class="kicker__dot"></span>Local Know-How</p><h2 class="h2 h2--sm" data-words>{e(ln.get("title", "Built For Oconomowoc Homes"))}</h2><p>{e(ln.get("text", ""))}</p></div>
</div></div></section>

<section class="sec" id="faq"><div class="wrap split split--top">
<div class="sticky">{kicker(s[1] + " FAQ")}{h2("Questions About", s[1])}<p class="lead" data-reveal="up">Answers from the technicians who do this work across Oconomowoc every week.</p>{phone_btn("btn btn--primary", "Ask A Technician")}</div>
{faq_html(d["faqs"])}
</div></section>

{cta(d["ctaTitle"], d["ctaText"])}

<section class="sec sec--tint"><div class="wrap">
<div class="head head--row"><div>{kicker("More Services")}{h2("Other Ways We Help", "Oconomowoc Homeowners")}</div>{arrow_btn("/#services", "All Services", "btn btn--ghost btn--sm")}</div>
<div class="bento bento--3">{rel_cards}</div>
</div></section>
'''
    schema = [
        {"@context": "https://schema.org", "@type": "Service", "name": s[1], "serviceType": s[1],
         "provider": {"@type": "HomeAndConstructionBusiness", "name": SITE["name"], "url": SITE["domain"], "telephone": SITE["phone"]},
         "areaServed": {"@type": "City", "name": "Oconomowoc, WI"}, "description": d["metaDescription"]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["domain"] + "/"},
            {"@type": "ListItem", "position": 2, "name": s[1], "item": f'{SITE["domain"]}/{s[0]}/'}]},
        faq_schema(d["faqs"]),
    ]
    return page(d["metaTitle"], d["metaDescription"], f"/{s[0]}/", body, current=s[0], schema=schema, image=s[4])

def not_found():
    body = f'''<section class="hero hero--404"><div class="hero__bg" aria-hidden="true"><img src="/images/calm-lake-pier-dusk.webp" alt=""></div><div class="wrap"><div class="hero__copy">{kicker("404")}<h1 class="h1" data-words>This page came <em>off its track.</em></h1><p class="hero__intro">The page you were looking for doesn't exist. Head back home, or call us if your garage door needs help.</p><div class="actions">{arrow_btn("/", "Back To Home", "btn btn--primary")}{phone_btn("btn btn--ghost")}</div></div></div>{waves()}</section>'''
    return page("Page Not Found | " + SITE["name"], "Page not found.", "/404", body)

def main():
    (OUT / "index.html").write_text(home())
    for s in SERVICES:
        d = json.loads((CONTENT / "services" / f"{s[0]}.json").read_text())
        p = OUT / s[0]; p.mkdir(parents=True, exist_ok=True)
        (p / "index.html").write_text(service_page(d))
    (OUT / "404.html").write_text(not_found())
    urls = ["/"] + [f"/{s[0]}/" for s in SERVICES]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE['domain']}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")
    (OUT / "site.webmanifest").write_text(json.dumps({"name": SITE["name"], "short_name": "Oconomowoc GD", "icons": [{"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}], "theme_color": "#4a7c94", "background_color": "#f7f3ec", "display": "standalone"}, indent=1))
    print("built", len(urls), "pages")

if __name__ == "__main__":
    main()
