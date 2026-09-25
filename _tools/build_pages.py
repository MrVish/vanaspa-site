#!/usr/bin/env python3
"""Builds VĀNA's treatment, area, offers and journal pages, plus sitemap.xml.

Run from the repo root:   python3 _tools/build_pages.py

Prices live in MENU below and are the single source for every generated page.
The homepage (index.html) is hand-written, so when a price changes here, change
it in index.html too (the menu section and the JSON-LD near the top).

The folder starts with "_" so GitHub Pages does not publish it.
"""
import html
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://vanaspa.com"
TODAY = date.today().isoformat()

PHONE_DISPLAY = "+91 81296 62890"
PHONE_TEL = "+918129662890"
WA_NUMBER = "918129662890"
EMAIL = "hello@vanaspa.com"
ADDRESS_LINES = ["E Tower, 1st &amp; 2nd Floor, Kollamkudimugal Road", "Athani, Kakkanad, Kochi 682030"]
MAPS_URL = "https://share.google/J33BrEqedsUDC5wgM"
INSTAGRAM = "https://www.instagram.com/vana_wellness_spa/"

# ── Menu: single source of prices (INR) ──────────────────────────────────────
# Mirrors the printed treatment booklet.
MENU = {
    "swedish":     {"name": "Swedish Restore",     "generic": "Swedish massage",     "prices": {60: 2500, 90: 3200}},
    "aroma":       {"name": "Aromatherapy Calm",   "generic": "Aromatherapy massage", "prices": {60: 2600, 90: 3200}},
    "balinese":    {"name": "Balinese Harmony",    "generic": "Balinese massage",    "prices": {60: 2700, 90: 3500}},
    "deep":        {"name": "Deep Tissue Release", "generic": "Deep tissue massage", "prices": {60: 2800, 90: 3500}, "steam": True},
    "sports":      {"name": "Sports Recovery",     "generic": "Sports massage",      "prices": {60: 3000, 90: 3500}, "steam": True},
    "fourhands":   {"name": "Four Hands",          "generic": "Four hands massage",  "prices": {60: 4800, 90: 5800}},
    "signature":   {"name": "Signature (alone)",    "generic": "Scrub, massage & private steam", "prices": {120: 3800}, "steam": True},
    "couples":     {"name": "Couples Signature",   "generic": "Couples massage",     "prices": {90: 5700, 120: 6500}, "steam": True},
    "reflexology": {"name": "Reflexology & Foot Restore", "generic": "Foot reflexology", "prices": {30: 700, 45: 1400}},
    "head":        {"name": "Head & Scalp",        "generic": "Head massage",        "prices": {30: 1000}},
    "nbs":         {"name": "Neck, Back & Shoulders", "generic": "Back and shoulder massage", "prices": {30: 1500, 45: 1800}},
    "detan":       {"name": "De-Tan",              "generic": "De-tan body treatment", "prices": {30: 1200}},
    "steam":       {"name": "Steam & Shower",      "generic": "Private steam",       "prices": {15: 500}},
    "foot_head":   {"name": "Foot & Head",         "generic": "Express combination", "prices": {60: 2200}},
    "back_head":   {"name": "Back & Head",         "generic": "Express combination", "prices": {60: 2200}},
    "fhb":         {"name": "Foot, Head & Back",   "generic": "Express combination", "prices": {60: 2600}},
    "facial_deep": {"name": "Deep Cleanse Facial", "generic": "Facial",              "prices": {45: 2300}},
    "facial_hyd":  {"name": "Hydrating Facial",    "generic": "Facial",              "prices": {60: 2300}},
    "facial_sig":  {"name": "VĀNA Signature Facial", "generic": "Facial",            "prices": {60: 2500}},
    "pedi":        {"name": "Classic Pedicure",    "generic": "Pedicure",            "prices": {45: 1600}},
    "pedi_lux":    {"name": "Luxury Pedicure",     "generic": "Pedicure",            "prices": {60: 2300}},
    "mani":        {"name": "Classic Manicure",    "generic": "Manicure",            "prices": {45: 1400}},
    "mani_lux":    {"name": "Luxury Manicure",     "generic": "Manicure",            "prices": {60: 2000}},
    "mani_pedi":   {"name": "Manicure & Pedicure", "generic": "Manicure and pedicure", "prices": {90: 2800}},
    "scrub":       {"name": "Forest Scrub",        "generic": "Body scrub",          "prices": {45: 2200}},
    "wrap":        {"name": "Cocoon Wrap",         "generic": "Body wrap",           "prices": {45: 2200}},
    "scrub_wrap":  {"name": "Scrub & Cocoon",      "generic": "Body scrub and wrap", "prices": {60: 3300}},
}

COMBOS = {
    "desk":      ("Desk Rescue", "Neck, Back &amp; Shoulders 45 + Head &amp; Scalp", 2500),
    "feet":      ("Feet First", "Reflexology 30 + Classic Pedicure", 2050),
    "evening":   ("The Long Evening", "90-minute massage + VĀNA Signature Facial", 5100),
    "polished":  ("Polished", "90-minute massage + Forest Scrub", 4850),
    "halfday":   ("Half Day", "90-minute massage + Forest Scrub + Cocoon Wrap", 6800),
    "afternoon": ("The Whole Afternoon", "90-minute massage + Scrub + Wrap + Manicure &amp; Pedicure", 9300),
    "two":       ("Two of Us", "Couples Signature, 90 min + Reflexology 30 for both", 6400),
}

DESCRIPTIONS = {
    "swedish": "Long, warm strokes that settle the whole nervous system. The classic, for good reason.",
    "aroma": "Essential oils and slow, gentle strokes that quiet the nervous system. The softest landing on the menu.",
    "balinese": "Acupressure and rhythm in the island tradition — firm, flowing, deeply restful.",
    "deep": "Slow, deliberate work into chronic knots. Built for desk shoulders and stubborn backs.",
    "sports": "Targeted work for overused muscles — warm-up, release, recover. For runners, gym regulars and weekend athletes.",
    "fourhands": "Two therapists, one synchronised rhythm. Twice the hands, half the thinking — our most indulgent hour.",
    "signature": "Our finest ritual — scrub, massage and a private steam, for one.",
    "couples": "The Signature ritual side by side in the couples suite, which has its own steam and shower.",
    "reflexology": "Pressure-point work for tired feet and lower legs. The quickest reset on the menu.",
    "head": "A focused head, scalp and neck reset. The fastest way to put down a long day.",
    "nbs": "Straight to screen-and-commute tension — neck, upper back, shoulders. In and out, lighter.",
    "detan": "A brightening body treatment for sun-tired skin.",
    "steam": "A private steam-and-shower reset — a quiet 15 minutes to yourself, before or after your massage.",
    "facial_deep": "Cleanse, exfoliate, extract, calm.",
    "facial_hyd": "Deep moisture for dry, tired skin.",
    "facial_sig": "Our fullest facial — cleanse, massage, mask, glow.",
    "scrub": "Full-body exfoliation with natural grains and warm oil.",
    "wrap": "A nourishing full-body wrap — hydrate, detox, rest.",
    "scrub_wrap": "Both, back to back.",
}


def inr(n):
    return "₹{:,}".format(n)


def price_range(key):
    p = MENU[key]["prices"]
    lo, hi = min(p.values()), max(p.values())
    return inr(lo) if lo == hi else "{} – {:,}".format(inr(lo), hi)


def durations(key):
    return " / ".join(str(m) for m in sorted(MENU[key]["prices"])) + " min"


def per_duration(key):
    p = MENU[key]["prices"]
    return " · ".join("{} min {}".format(m, inr(v)) for m, v in sorted(p.items()))


def wa(msg):
    from urllib.parse import quote
    return "https://wa.me/{}?text={}".format(WA_NUMBER, quote(msg))


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>')


def row(key, link=None, extra=""):
    m = MENU[key]
    name = html.escape(m["name"]).replace("&amp;amp;", "&amp;")
    if link:
        name = '<a href="{}">{}</a>'.format(link, name)
    desc = DESCRIPTIONS.get(key, "")
    if m.get("steam") and key in ("deep", "sports"):
        desc += " Includes a complimentary 10-minute steam &amp; shower."
    if extra:
        desc += " " + extra
    return ('<div class="price-row"><span class="nm">{}</span><span class="pr">{}</span>'
            '<span class="ds">{} <em>{}</em></span></div>').format(name, price_range(key), desc, durations(key))


def combo_row(key):
    n, d, p = COMBOS[key]
    return '<div class="price-row"><span class="nm">{}</span><span class="pr">{}</span><span class="ds">{}</span></div>'.format(n, inr(p), d)


def prices(*rows, note="Every price is the full price — what's written is what you pay."):
    return '<div class="prices">{}</div><p class="price-note">{}</p>'.format("".join(rows), note)


def faq_html(faqs):
    items = "".join('<details><summary>{}</summary><p>{}</p></details>'.format(q, a) for q, a in faqs)
    return '<div class="faq">{}</div>'.format(items)


def strip_tags(s):
    import re
    return html.unescape(re.sub(r"<[^>]+>", "", s))


# ── Shared structured data ───────────────────────────────────────────────────
BUSINESS_REF = {
    "@type": "DaySpa",
    "@id": SITE + "/#business",
    "name": "VĀNA Wellness Spa",
    "url": SITE + "/",
    "telephone": PHONE_TEL,
    "image": SITE + "/assets/og-image.jpg",
    "priceRange": "₹₹",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "E Tower, 1st & 2nd Floor, Kollamkudimugal Road, Athani",
        "addressLocality": "Kakkanad, Kochi",
        "addressRegion": "Kerala",
        "postalCode": "682030",
        "addressCountry": "IN",
    },
}

# ── Page chrome ──────────────────────────────────────────────────────────────
FOOT_TREATMENTS = [
    ("/massage-kakkanad/", "Massage in Kakkanad"),
    ("/deep-tissue-massage-kakkanad/", "Deep tissue massage"),
    ("/swedish-massage-kakkanad/", "Swedish massage"),
    ("/balinese-massage-kakkanad/", "Balinese massage"),
    ("/sports-massage-kakkanad/", "Sports massage"),
    ("/couples-spa-kakkanad/", "Couples spa"),
    ("/facials-body-care/", "Facials, scrubs &amp; wraps"),
    ("/manicure-pedicure-kakkanad/", "Manicure &amp; pedicure"),
]
FOOT_MORE = [
    ("/spa-near-infopark/", "Spa near Infopark"),
    ("/offers/", "Offers &amp; memberships"),
    ("/journal/", "Journal"),
    ("/#visit", "Hours &amp; directions"),
    (INSTAGRAM, "Instagram"),
]


def header(book_msg):
    return """<header class="site-head">
  <a class="head-brand" href="/" aria-label="VĀNA Wellness Spa — home">
    <svg class="head-mark" viewBox="0 0 200 240" fill="none" aria-hidden="true"><g stroke="#B0832E" stroke-linecap="round"><path d="M 65 24 C 80 12 120 12 135 24" stroke-width="7"/><path d="M 74 17 C 86 9 114 9 126 17" stroke-width="5" opacity="0.6"/></g><g stroke="#23201A" stroke-linecap="round"><path d="M 100 34 L 34 214" stroke-width="8"/><path d="M 100 34 L 166 214" stroke-width="8"/><path d="M 60 158 Q 100 150 140 158" stroke-width="5" opacity="0.65"/></g></svg>
    <span class="head-word">VĀNA</span>
  </a>
  <nav class="head-nav" aria-label="Main">
    <a href="/massage-kakkanad/">Massage</a>
    <a href="/couples-spa-kakkanad/">Couples</a>
    <a href="/offers/">Offers</a>
    <a href="/#visit">Visit</a>
    <a class="head-cta" href="{wa}" target="_blank" rel="noopener">Book on WhatsApp</a>
  </nav>
</header>""".format(wa=wa(book_msg))


def footer():
    t = "".join('<li><a href="{}">{}</a></li>'.format(u, n) for u, n in FOOT_TREATMENTS)
    m = "".join('<li><a href="{}"{}>{}</a></li>'.format(u, ' target="_blank" rel="noopener"' if u.startswith("http") else "", n) for u, n in FOOT_MORE)
    return """<footer class="site-foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <div class="foot-brand">VĀNA</div>
        <p>VĀNA Wellness Spa — a boutique wellness spa at E Tower, Kollamkudimugal Road, Athani, Kakkanad, Kochi 682030, a few minutes from Infopark and SmartCity.<br>
        <a href="tel:{tel}">{phone}</a> · <a href="mailto:{email}">{email}</a><br>
        Mon–Thu 12 PM – 9 PM · Fri–Sun 11 AM – 9:30 PM</p>
      </div>
      <div><h4>Treatments</h4><ul>{t}</ul></div>
      <div><h4>More</h4><ul>{m}</ul></div>
    </div>
    <p class="foot-legal">VĀNA Wellness Spa is operated by Vana Serene LLP, Ernakulam, Kerala. Prices in INR.</p>
  </div>
</footer>""".format(t=t, m=m, tel=PHONE_TEL, phone=PHONE_DISPLAY, email=EMAIL)


VISIT = """<section class="band band-sand" id="visit">
  <div class="wrap">
    <p class="eyebrow">Visit</p>
    <h2 style="margin-top:12px">Find VĀNA in Athani, Kakkanad</h2>
    <div class="visit">
      <div>
        <h3>Where</h3>
        <p class="big">{a0},<br>{a1}</p>
        <p>A few minutes from Infopark and SmartCity. Parking on site, lift access.</p>
        <p style="margin-top:14px"><a class="btn btn-dark" href="{maps}" target="_blank" rel="noopener">Open in Google Maps</a></p>
      </div>
      <div>
        <h3>Hours · Open every day</h3>
        <div class="hrs"><span>Monday – Thursday</span><span>12:00 PM – 9:00 PM</span></div>
        <div class="hrs"><span>Friday – Sunday</span><span>11:00 AM – 9:30 PM</span></div>
        <div class="hrs"><span>Last session</span><span>90 min before close</span></div>
        <p style="margin-top:14px">WhatsApp or call <a href="tel:{tel}">{phone}</a></p>
      </div>
    </div>
  </div>
</section>""".format(a0=ADDRESS_LINES[0], a1=ADDRESS_LINES[1], maps=MAPS_URL, tel=PHONE_TEL, phone=PHONE_DISPLAY)


def cta_band(title, text, book_msg):
    return """<section class="band band-forest cta-band">
  <div class="wrap">
    <p class="eyebrow">Book</p>
    <h2 style="margin-top:12px">{title}</h2>
    <p>{text}</p>
    <div class="p-ctas">
      <a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">{svg}Book on WhatsApp</a>
      <a class="btn btn-light" href="tel:{tel}">Call {phone}</a>
    </div>
  </div>
</section>""".format(title=title, text=text, wa=wa(book_msg), svg=WA_SVG, tel=PHONE_TEL, phone=PHONE_DISPLAY)


def related_html(slugs):
    cards = []
    for s in slugs:
        p = PAGE_INDEX[s]
        cards.append('<a href="/{}/"><b>{}</b><span>{}</span><em>{}</em></a>'.format(s, p["card_title"], p["card_text"], p.get("card_price", "Read more")))
    return '<div class="related">{}</div>'.format("".join(cards))


def render(p):
    url = "{}/{}/".format(SITE, p["slug"])
    book_msg = p.get("book_msg", "Hi, I'd like to book a session at VĀNA Wellness Spa.")
    crumbs = [("Home", SITE + "/")] + p.get("crumbs", []) + [(p["crumb"], url)]
    crumb_html = '<nav class="crumbs" aria-label="Breadcrumb">' + '<span>/</span>'.join(
        '<a href="{}">{}</a>'.format(u.replace(SITE, ""), n) if i < len(crumbs) - 1 else n
        for i, (n, u) in enumerate(crumbs)) + "</nav>"

    graph = [
        BUSINESS_REF,
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": strip_tags(p["title"]),
         "description": p["description"], "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#business"},
         "primaryImageOfPage": SITE + p["image"]},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": strip_tags(n), "item": u} for i, (n, u) in enumerate(crumbs)]},
    ]
    if p.get("service"):
        s = p["service"]
        offers = []
        for key in s["keys"]:
            for mins, price in sorted(MENU[key]["prices"].items()):
                offers.append({"@type": "Offer", "name": "{} — {} minutes".format(MENU[key]["name"], mins),
                               "price": str(price), "priceCurrency": "INR", "url": url})
        graph.append({"@type": "Service", "@id": url + "#service", "name": s["name"], "serviceType": s["type"],
                      "description": p["description"], "provider": {"@id": SITE + "/#business"},
                      "areaServed": ["Kakkanad", "Athani", "Infopark", "SmartCity Kochi", "Thrikkakara", "Kochi"],
                      "offers": offers})
    if p.get("article"):
        graph.append({"@type": "Article", "headline": strip_tags(p["h1"]), "description": p["description"],
                      "image": SITE + p["image"], "datePublished": p["article"], "dateModified": p["article"],
                      "author": {"@type": "Organization", "name": "VĀNA Wellness Spa", "url": SITE + "/"},
                      "publisher": {"@id": SITE + "/#business"}, "mainEntityOfPage": url})
    if p.get("faqs"):
        graph.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in p["faqs"]]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)

    facts = ""
    if p.get("facts"):
        facts = '<div class="p-facts">' + "".join('<div><b>{}</b><small>{}</small></div>'.format(b, s) for b, s in p["facts"]) + "</div>"
    faqs = ""
    if p.get("faqs"):
        faqs = '<section class="band"><div class="wrap narrow"><p class="eyebrow">Questions</p><h2 style="margin-top:12px">{}</h2>{}</div></section>'.format(
            p.get("faq_title", "Questions, answered plainly"), faq_html(p["faqs"]))
    related = ""
    if p.get("related"):
        related = '<section class="band band-cream"><div class="wrap"><p class="eyebrow">You might also like</p><h2 style="margin-top:12px">More at VĀNA</h2>{}</div></section>'.format(related_html(p["related"]))

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-7RVEWWMJKN"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-7RVEWWMJKN');</script>
<title>{title_e}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#23311E">
<link rel="icon" type="image/x-icon" href="/favicon.ico">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{ogtype}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="VĀNA Wellness Spa">
<meta property="og:title" content="{title_e}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{site}{image}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=DM+Sans:wght@300;400;500&family=Plus+Jakarta+Sans:ital,wght@1,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/pages.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
{header}
<main>
<div class="wrap">
  {crumbs}
  <section class="p-hero">
    <div>
      <p class="eyebrow">{eyebrow}</p>
      <h1>{h1}</h1>
      <p class="p-lede">{lede}</p>
      {facts}
      <div class="p-ctas">
        <a class="btn btn-primary" href="{wa}" target="_blank" rel="noopener">{svg}Book on WhatsApp</a>
        <a class="btn btn-dark" href="{cta2_url}">{cta2}</a>
      </div>
    </div>
    <figure class="p-figure">
      <img src="{image}" alt="{alt}">
      <figcaption>Design visualisation of the space at VĀNA</figcaption>
    </figure>
  </section>
</div>
{body}
{faqs}
{cta}
{related}
{visit}
</main>
{footer}
<a class="fa-wa" href="{wa}" target="_blank" rel="noopener" aria-label="Message VĀNA on WhatsApp">{svg}</a>
</body>
</html>
""".format(
        title_e=html.escape(p["title"], quote=True), desc=html.escape(p["description"], quote=True), url=url, site=SITE, image=p["image"],
        ogtype="article" if p.get("article") else "website", ld=ld, header=header(book_msg), crumbs=crumb_html,
        eyebrow=p["eyebrow"], h1=p["h1"], lede=p["lede"], facts=facts, wa=wa(book_msg), svg=WA_SVG,
        cta2_url=p.get("cta2_url", "#details"), cta2=p.get("cta2", "Prices &amp; details"),
        alt=html.escape(p["alt"], quote=True), body=p["body"], faqs=faqs,
        cta=cta_band(p.get("cta_title", "Book your session"), p.get("cta_text", "Message us on WhatsApp with a day and time. We'll confirm your slot, then send three short questions the day before so your therapist is ready when you arrive."), book_msg),
        related=related, visit=VISIT, footer=footer())


def section(inner, cls="", sid="details"):
    return '<section class="band {}" id="{}"><div class="wrap narrow prose">{}</div></section>'.format(cls, sid, inner)


HOW_IT_WORKS = """<ol class="steps">
  <li><span class="n">01</span><div><b>You book on WhatsApp or by phone</b>Tell us the treatment, day and time. Ask for a female therapist if you'd prefer one.</div></li>
  <li><span class="n">02</span><div><b>We ask three questions the day before</b>What hurts, what you're hoping for, what to avoid — on WhatsApp, two minutes of your time.</div></li>
  <li><span class="n">03</span><div><b>Arrive ten minutes early</b>Let the day settle before the session does. Your therapist is already briefed — no clipboard at the door.</div></li>
  <li><span class="n">04</span><div><b>Your session, in a private room</b>Every treatment room at VĀNA has its own private bath. Pressure is a conversation — say if it's too much or too little.</div></li>
  <li><span class="n">05</span><div><b>A note from us that evening</b>What was worked, what to carry forward, and when it would help to come back.</div></li>
</ol>"""

# ── Pages ────────────────────────────────────────────────────────────────────
PAGES = []

PAGES.append(dict(
    slug="massage-kakkanad",
    title="Massage in Kakkanad | Full-Body Massage Prices — VĀNA Wellness Spa",
    description="Full-body massage in Kakkanad, Kochi at VĀNA Wellness Spa, Athani — Swedish, aromatherapy, Balinese, deep tissue, sports and four-hands massage from ₹2,500, plus 30-minute express resets. Near Infopark, open every day.",
    crumb="Massage in Kakkanad",
    card_title="Massage in Kakkanad", card_text="Every massage on the menu, with prices and a guide to choosing.", card_price="From ₹2,500",
    eyebrow="Massage · Athani, Kakkanad",
    h1="Massage in Kakkanad, done properly",
    lede="Five full-body massages, a four-hands session, a Signature ritual and short express resets — all in private rooms with their own bath, a few minutes from Infopark. Every price is the full price.",
    facts=[("From ₹2,500", "60-minute massage"), ("60 / 90 min", "Full-body sessions"), ("Every day", "Open until 9:30 PM Fri–Sun")],
    image="/assets/img/massage.jpg", alt="A massage in a warm, low-lit treatment room at VĀNA Wellness Spa, Kakkanad",
    service=dict(name="Massage at VĀNA Wellness Spa, Kakkanad", type="Massage therapy", keys=["swedish", "aroma", "balinese", "deep", "sports", "fourhands"]),
    body=section("""
<h2>The massage menu</h2>
<p>Every full-body massage comes in 60 or 90 minutes. The lower price in each range is the 60-minute session; the higher is 90 minutes.</p>
""" + prices(
        row("swedish", "/swedish-massage-kakkanad/"),
        row("aroma"),
        row("balinese", "/balinese-massage-kakkanad/"),
        row("deep", "/deep-tissue-massage-kakkanad/"),
        row("sports", "/sports-massage-kakkanad/"),
        row("fourhands"),
        row("signature", "/couples-spa-kakkanad/"),
    ) + """
<h2>Short on time? Express resets</h2>
<p>Thirty to sixty minutes, made for the evening after work. Pair two areas in one 60-minute session for a little less.</p>
""" + prices(row("nbs"), row("head"), row("reflexology"), row("foot_head"), row("back_head"), row("fhb"), combo_row("desk"), row("steam")) + """
<h2>Which massage should I choose?</h2>
<ul>
  <li><strong>First massage, or you simply want to switch off:</strong> <a href="/swedish-massage-kakkanad/">Swedish Restore</a>. Pressure is adjustable from light to firm.</li>
  <li><strong>Want it softer and scented:</strong> Aromatherapy Calm — slow, gentle strokes with essential oils.</li>
  <li><strong>Knots in the shoulders, a back that won't let go:</strong> <a href="/deep-tissue-massage-kakkanad/">Deep Tissue Release</a>.</li>
  <li><strong>You run, lift or play:</strong> <a href="/sports-massage-kakkanad/">Sports Recovery</a>.</li>
  <li><strong>You like firm, flowing pressure and acupressure:</strong> <a href="/balinese-massage-kakkanad/">Balinese Harmony</a>.</li>
  <li><strong>Two of you:</strong> the <a href="/couples-spa-kakkanad/">couples suite</a>.</li>
</ul>
<p>Still unsure? Our guide to <a href="/journal/swedish-vs-deep-tissue-massage/">Swedish vs deep tissue massage</a> covers the most common question we get — or just tell us on WhatsApp what's bothering you and we'll suggest one.</p>
<h2>How a massage at VĀNA works</h2>
""" + HOW_IT_WORKS + """
<h2>Good to know</h2>
<ul>
  <li><strong>Female therapist on request.</strong> Just say so when you book.</li>
  <li><strong>Tell us everything.</strong> Injuries, pregnancy, blood pressure, a bad night's sleep — it all changes how we work.</li>
  <li><strong>Phones rest too.</strong> Silent, please; the quiet is part of the treatment.</li>
  <li><strong>Safety, by design.</strong> Certified therapists, documented protocols, CCTV in common areas and never in treatment rooms.</li>
</ul>
"""),
    faqs=[
        ("How much does a massage cost at VĀNA in Kakkanad?", "A 60-minute full-body massage is ₹2,500–3,000 depending on the style, and 90 minutes is ₹3,200–3,500. Express sessions start at ₹700 for 30 minutes of reflexology. Prices shown are the full price."),
        ("Which massage is best for neck and shoulder pain from desk work?", "Deep Tissue Release if the tension is long-standing, or a 30/45-minute Neck, Back &amp; Shoulders session if you want a quick reset after work. See our note on <a href=\"/journal/massage-for-neck-and-shoulder-tension-desk-work/\">massage for desk tension</a>."),
        ("Can I ask for a female therapist?", "Yes. Mention it when you book on WhatsApp or by phone and we'll arrange it."),
        ("How late can I book a massage?", "We're open until 9 PM Monday to Thursday and 9:30 PM Friday to Sunday. The last session begins 90 minutes before closing."),
        ("Is there parking?", "Yes, parking is on site at E Tower, Athani, with lift access to both floors."),
    ],
    related=["deep-tissue-massage-kakkanad", "couples-spa-kakkanad", "spa-near-infopark"],
    book_msg="Hi, I'd like to book a massage at VĀNA.",
))

PAGES.append(dict(
    slug="deep-tissue-massage-kakkanad",
    title="Deep Tissue Massage in Kakkanad — VĀNA Wellness Spa, near Infopark",
    description="Deep tissue massage in Kakkanad, Kochi: VĀNA's Deep Tissue Release — slow, firm work into chronic knots for desk shoulders and stubborn backs. 60 min ₹2,800, 90 min ₹3,500, with a complimentary steam & shower. Athani, near Infopark.",
    crumb="Deep tissue massage", crumbs=[("Massage", SITE + "/massage-kakkanad/")],
    card_title="Deep tissue massage", card_text="Slow, firm work into chronic knots. Steam &amp; shower included.", card_price=price_range("deep"),
    eyebrow="Deep Tissue Release · Deep tissue massage",
    h1="Deep tissue massage in Kakkanad",
    lede="Deep Tissue Release is our slowest, most deliberate massage — firm, focused work into the chronic knots that a lighter massage slides over. Built for desk shoulders, laptop necks and backs that never quite let go.",
    facts=[(inr(2800), "60 minutes"), (inr(3500), "90 minutes"), ("Included", "10-min steam &amp; shower")],
    image="/assets/img/treatment-room.jpg", alt="A private treatment room at VĀNA Wellness Spa, Kakkanad, prepared for a deep tissue massage",
    service=dict(name="Deep Tissue Release — deep tissue massage", type="Deep tissue massage", keys=["deep"]),
    body=section("""
<h2>What deep tissue massage is</h2>
<p>Deep tissue massage uses slow strokes and sustained pressure to reach the deeper layers of muscle and the connective tissue around them. The therapist works with forearms, knuckles and thumbs as well as open hands, and spends longer on fewer areas — usually the neck, shoulders, upper and lower back.</p>
<p>It isn't simply a Swedish massage done harder. The pace is slower and the pressure builds gradually, so the muscle has time to soften rather than brace against it.</p>
<h2>Price and duration</h2>
""" + prices(row("deep"), note="60 minutes ₹2,800 · 90 minutes ₹3,500 · a complimentary 10-minute steam &amp; shower is included with both.") + """
<p><strong>60 or 90 minutes?</strong> Sixty minutes is enough for one or two problem areas — say, neck and shoulders. Choose 90 if you want the whole back and legs worked properly, or if it's your first deep tissue session and you'd like time to warm up into the pressure.</p>
<h2>Who it's for</h2>
""" + """<div class="cols" style="margin-top:22px">
<div class="fit"><h3>A good choice if…</h3><ul>
<li>You sit at a desk or laptop most of the day</li>
<li>You have knots you can press on and feel</li>
<li>A lighter massage feels pleasant but doesn't last</li>
<li>You train and carry general tightness (or see <a href="/sports-massage-kakkanad/">Sports Recovery</a>)</li>
</ul></div>
<div class="fit"><h3>Tell us first, or choose something else, if…</h3><ul>
<li>You're pregnant, have high blood pressure or take blood thinners</li>
<li>You have a recent injury, strain or surgery</li>
<li>You bruise easily or have a skin condition in the area</li>
<li>You want pure relaxation — try <a href="/swedish-massage-kakkanad/">Swedish Restore</a></li>
</ul></div></div>
<p class="note">Massage is not a substitute for medical care. Numbness, tingling, pain that spreads down an arm or leg, or pain after an accident should be seen by a doctor or physiotherapist first.</p>
<h2>What happens in your session</h2>
""" + HOW_IT_WORKS + """
<h2>Does deep tissue massage hurt?</h2>
<p>It should feel intense in places, never sharp. A useful rule is that you should be able to breathe slowly through it; if you're holding your breath or tensing up, the pressure is too much and the muscle will fight back. Pressure is a conversation — tell your therapist, and they'll adjust. The right pressure is the one you'd ask for again.</p>
<h2>Afterwards</h2>
<ul>
<li>Take the complimentary steam and shower — warmth helps the work settle.</li>
<li>Drink water and keep the evening easy.</li>
<li>Some tenderness for a day or two is normal, a bit like after a workout. Gentle movement helps.</li>
<li>Your follow-up note that evening will suggest a stretch or two and when it would help to come back.</li>
</ul>
"""),
    faqs=[
        ("How much is a deep tissue massage at VĀNA?", "₹2,800 for 60 minutes and ₹3,500 for 90 minutes, including a complimentary 10-minute steam and shower."),
        ("How often should I get a deep tissue massage?", "For long-standing desk tension, many people find every two to four weeks keeps it from building back up. Our Monthly Deep membership (₹2,500 a month) covers one Deep Tissue or Sports session a month. See <a href=\"/offers/\">offers and memberships</a>."),
        ("What's the difference between deep tissue and Swedish massage?", "Swedish uses long, flowing strokes over the whole body to relax you; deep tissue is slower and firmer, and focuses on fewer areas. We've written a <a href=\"/journal/swedish-vs-deep-tissue-massage/\">full comparison</a>."),
        ("What's the difference between deep tissue and sports massage?", "Deep tissue targets chronic tension wherever it sits. Sports Recovery is organised around training — warming up, releasing and recovering the muscles you use most."),
        ("Can I book a deep tissue massage in the evening?", "Yes. We're open until 9 PM Monday to Thursday and 9:30 PM Friday to Sunday; the last 90-minute session starts 90 minutes before closing."),
    ],
    related=["sports-massage-kakkanad", "swedish-massage-kakkanad", "spa-near-infopark"],
    book_msg="Hi, I'd like to book a Deep Tissue massage at VĀNA.",
))

PAGES.append(dict(
    slug="swedish-massage-kakkanad",
    title="Swedish Massage in Kakkanad — VĀNA Wellness Spa, Athani",
    description="Swedish massage in Kakkanad, Kochi: VĀNA's Swedish Restore — long, warm strokes for full-body relaxation. 60 min ₹2,500, 90 min ₹3,200. Also Aromatherapy Calm. Private rooms, near Infopark, open every day.",
    crumb="Swedish massage", crumbs=[("Massage", SITE + "/massage-kakkanad/")],
    card_title="Swedish massage", card_text="Long, warm strokes. The classic first massage.", card_price=price_range("swedish"),
    eyebrow="Swedish Restore · Swedish massage",
    h1="Swedish massage in Kakkanad",
    lede="Swedish Restore is the classic full-body massage — long, warm, flowing strokes that settle the whole nervous system. If you've never had a massage, or you simply want an hour to switch off, start here.",
    facts=[(inr(2500), "60 minutes"), (inr(3200), "90 minutes"), ("Light → firm", "Pressure, your choice")],
    image="/assets/img/details-oils.jpg", alt="Warm massage oils and linen at VĀNA Wellness Spa, prepared for a Swedish massage",
    service=dict(name="Swedish Restore — Swedish massage", type="Swedish massage", keys=["swedish", "aroma"]),
    body=section("""
<h2>What Swedish massage is</h2>
<p>Swedish massage is built on a handful of classic techniques: long gliding strokes, kneading, gentle friction and rhythmic movement, worked over the whole body in a steady, unhurried sequence. The aim is circulation, softness and rest — the feeling of a long day being put down.</p>
<p>Pressure is adjustable. Many guests ask for medium-firm; if you want it softer, say so, and if you want real knot work, <a href="/deep-tissue-massage-kakkanad/">deep tissue</a> is the better choice.</p>
<h2>Prices</h2>
""" + prices(row("swedish"), row("aroma")) + """
<h3>Swedish or Aromatherapy?</h3>
<p>Aromatherapy Calm follows a similar flow but slower and gentler, with essential oils chosen for calm. It's the softest landing on our menu — good for poor sleep and busy minds. Swedish Restore is a little more active and a little firmer.</p>
<h2>Who it's for</h2>
<ul>
<li>Your first professional massage</li>
<li>Stress, tiredness, a week that won't end</li>
<li>General stiffness rather than one specific knot</li>
<li>A gift for someone who hasn't been to a spa before — see <a href="/offers/">gift cards</a></li>
</ul>
<h2>What happens in your session</h2>
""" + HOW_IT_WORKS + """
<h2>60 or 90 minutes?</h2>
<p>Sixty minutes covers back, legs, arms and shoulders at a comfortable pace. Ninety gives time for the neck, scalp and feet as well, and for the slowness that makes Swedish massage work. For ₹700 more, most people who try 90 don't go back.</p>
"""),
    faqs=[
        ("How much does a Swedish massage cost at VĀNA?", "₹2,500 for 60 minutes and ₹3,200 for 90 minutes. Aromatherapy Calm is ₹2,600 and ₹3,200."),
        ("Is Swedish massage good for a first-timer?", "Yes — it's the one we suggest most often for a first visit. Your therapist will check pressure early on and adjust as you go."),
        ("Can I add a steam?", "Yes, a private 15-minute Steam &amp; Shower is ₹500. During our Opening Month offers it's complimentary with any massage on weekday afternoons."),
        ("Will I be comfortable?", "Every treatment room is private with its own bath, and you can ask for a female therapist when you book. Tell us anything that matters — injuries, pregnancy, what to avoid."),
    ],
    related=["deep-tissue-massage-kakkanad", "balinese-massage-kakkanad", "couples-spa-kakkanad"],
    book_msg="Hi, I'd like to book a Swedish massage at VĀNA.",
))

PAGES.append(dict(
    slug="balinese-massage-kakkanad",
    title="Balinese Massage in Kakkanad — VĀNA Wellness Spa, near Infopark",
    description="Balinese massage in Kakkanad, Kochi: VĀNA's Balinese Harmony combines acupressure with firm, flowing rhythm. 60 min ₹2,700, 90 min ₹3,500. Private rooms in Athani, near Infopark, open every day.",
    crumb="Balinese massage", crumbs=[("Massage", SITE + "/massage-kakkanad/")],
    card_title="Balinese massage", card_text="Acupressure and firm, flowing rhythm.", card_price=price_range("balinese"),
    eyebrow="Balinese Harmony · Balinese massage",
    h1="Balinese massage in Kakkanad",
    lede="Balinese Harmony works in the island tradition: acupressure along the body, then long, firm, rhythmic strokes that join it all together. Firmer than Swedish, gentler than deep tissue — and deeply restful.",
    facts=[(inr(2700), "60 minutes"), (inr(3500), "90 minutes"), ("Firm", "Flowing pressure")],
    image="/assets/img/corridor.jpg", alt="The warm-lit arrival corridor at VĀNA Wellness Spa, Athani, Kakkanad",
    service=dict(name="Balinese Harmony — Balinese massage", type="Balinese massage", keys=["balinese"]),
    body=section("""
<h2>What Balinese massage is</h2>
<p>Traditional Balinese massage blends several techniques: thumb and palm acupressure along the muscles, gentle stretching, skin rolling and long, sweeping strokes. The pressure is firm but the rhythm is continuous, so it feels both grounding and relaxing.</p>
<p>It suits people who find Swedish massage too light but don't want the slow, targeted intensity of deep tissue.</p>
<h2>Price</h2>
""" + prices(row("balinese")) + """
<h2>Who it's for</h2>
<ul>
<li>You like firm pressure but want the whole body worked, not one area</li>
<li>General stiffness and fatigue, especially after travel</li>
<li>You've had Swedish massages before and want something with more depth</li>
</ul>
<p class="note">As with any firm massage, tell us about pregnancy, blood pressure, recent injuries or surgery before your session.</p>
<h2>What happens in your session</h2>
""" + HOW_IT_WORKS + """
<h2>Make an evening of it</h2>
<p>Pair a 90-minute massage with a Forest Scrub (<em>Polished</em>, ₹4,850) or a VĀNA Signature Facial (<em>The Long Evening</em>, ₹5,100). See <a href="/facials-body-care/">facials, scrubs and wraps</a>.</p>
"""),
    faqs=[
        ("How much is a Balinese massage at VĀNA?", "₹2,700 for 60 minutes and ₹3,500 for 90 minutes."),
        ("Is Balinese massage painful?", "It shouldn't be. The pressure is firm and the acupressure points can feel intense for a moment, but your therapist will adjust to you. Say so if it's too much."),
        ("Balinese or deep tissue?", "Balinese covers the whole body with firm, flowing pressure. <a href=\"/deep-tissue-massage-kakkanad/\">Deep tissue</a> is slower and concentrates on a few problem areas."),
    ],
    related=["swedish-massage-kakkanad", "deep-tissue-massage-kakkanad", "facials-body-care"],
    book_msg="Hi, I'd like to book a Balinese massage at VĀNA.",
))

PAGES.append(dict(
    slug="sports-massage-kakkanad",
    title="Sports Massage in Kakkanad — VĀNA Wellness Spa, near Infopark",
    description="Sports massage in Kakkanad, Kochi: VĀNA's Sports Recovery for runners, gym regulars and weekend athletes — warm-up, release, recover. 60 min ₹3,000, 90 min ₹3,500, with complimentary steam & shower.",
    crumb="Sports massage", crumbs=[("Massage", SITE + "/massage-kakkanad/")],
    card_title="Sports massage", card_text="For runners, gym regulars and weekend athletes.", card_price=price_range("sports"),
    eyebrow="Sports Recovery · Sports massage",
    h1="Sports massage in Kakkanad",
    lede="Sports Recovery is targeted work for overused muscles — warm-up, release, recover. For runners, gym regulars, cyclists, footballers and anyone whose training has started to talk back.",
    facts=[(inr(3000), "60 minutes"), (inr(3500), "90 minutes"), ("Included", "10-min steam &amp; shower")],
    image="/assets/img/treatment-room.jpg", alt="A private treatment room at VĀNA Wellness Spa prepared for a sports massage",
    service=dict(name="Sports Recovery — sports massage", type="Sports massage", keys=["sports"]),
    body=section("""
<h2>What sports massage is</h2>
<p>Sports massage is organised around how you train. Your therapist warms the tissue first, then works into the muscles you load most — calves, hamstrings and hips for runners; shoulders, lats and forearms for lifters and racquet players — and finishes with work that helps you move freely again.</p>
<p>Tell us in the WhatsApp intake the day before what you do, what's tight and whether you have an event coming up. That shapes the whole session.</p>
<h2>Price and duration</h2>
""" + prices(row("sports")) + """
<h2>Timing it around training</h2>
<ul>
<li><strong>After a hard session or race:</strong> give it a day or so, then book a full recovery massage.</li>
<li><strong>In a training block:</strong> every two to four weeks helps many people stay ahead of tightness.</li>
<li><strong>Before an event:</strong> keep it lighter and a few days out — not deep work the day before.</li>
</ul>
<p class="note">Sports massage is not treatment for an injury. A sudden pain, swelling, or anything that stops you training should be seen by a doctor or physiotherapist first.</p>
<h2>What happens in your session</h2>
""" + HOW_IT_WORKS + """
<h2>Sports massage or deep tissue?</h2>
<p>Both are firm. <a href="/deep-tissue-massage-kakkanad/">Deep Tissue Release</a> chases chronic tension wherever it sits — often desk-related. Sports Recovery is built around movement and the muscles your sport uses. If you both train and sit at a desk all day, tell us; we'll balance the two.</p>
"""),
    faqs=[
        ("How much does a sports massage cost at VĀNA?", "₹3,000 for 60 minutes and ₹3,500 for 90 minutes, with a complimentary 10-minute steam and shower."),
        ("Is there a membership for regular sports massage?", "Yes. The Monthly Deep (₹2,500 a month) covers one 60-minute Deep Tissue or Sports session every month, with steam included. The Deep Five pack is ₹12,500. See <a href=\"/offers/\">offers and memberships</a>."),
        ("Can I come straight from the gym?", "Yes — every treatment room has a private bath, and your session includes a steam and shower."),
    ],
    related=["deep-tissue-massage-kakkanad", "massage-kakkanad", "offers"],
    book_msg="Hi, I'd like to book a Sports massage at VĀNA.",
))

PAGES.append(dict(
    slug="couples-spa-kakkanad",
    title="Couples Spa & Couples Massage in Kakkanad — VĀNA Wellness Spa",
    description="Couples massage in Kakkanad, Kochi: VĀNA's private couples suite with its own steam and shower. Couples Signature — scrub, massage and steam side by side — 90 min ₹5,700, 120 min ₹6,500. Near Infopark, open every day.",
    crumb="Couples spa",
    card_title="Couples spa", card_text="A private suite with its own steam and shower.", card_price="From ₹5,700 for two",
    eyebrow="The Couples Suite · Kakkanad",
    h1="Couples spa in Kakkanad",
    lede="One private suite for two, with its own steam and shower. The Signature ritual — scrub, massage and a private steam — side by side, for an anniversary, a birthday, or a Tuesday that earned it.",
    facts=[(inr(5700), "90 min, for two"), (inr(6500), "120 min, for two"), ("Private", "Steam &amp; shower in-suite")],
    image="/assets/img/couples-suite.jpg", alt="The couples suite at VĀNA Wellness Spa, Kakkanad — two massage tables in warm light with a private steam and shower",
    service=dict(name="Couples massage — Couples Signature", type="Couples massage", keys=["couples", "fourhands", "signature"]),
    body=section("""
<h2>The couples suite</h2>
<p>VĀNA has two floors and five treatment rooms. The couples suite is on the guest floor, and it's the one room we hold back: two tables side by side, its own private steam and its own shower. Nothing is shared but the calm.</p>
<h2>Couples treatments and prices</h2>
""" + prices(
        row("couples"),
        combo_row("two"),
        row("fourhands", extra="For one guest — two therapists at once."),
        row("signature"),
        note="Prices for two unless shown. The Together pack — three couples sessions in the suite, steam included — is ₹15,500, valid 6 months.") + """
<h2>What happens in the Couples Signature</h2>
<ol class="steps">
<li><span class="n">01</span><div><b>Before you arrive</b>Each of you answers our three WhatsApp questions, so both therapists know your pressure, focus areas and anything to avoid.</div></li>
<li><span class="n">02</span><div><b>A body scrub</b>A full-body exfoliation to wake the skin and warm the muscles.</div></li>
<li><span class="n">03</span><div><b>Side-by-side massage</b>Two therapists, one room. Pressure is set for each of you separately — one firm, one gentle is fine.</div></li>
<li><span class="n">04</span><div><b>A private steam</b>The suite's own steam and shower, just for the two of you.</div></li>
</ol>
<h2>Booking the suite</h2>
<p>There's one couples suite, so evenings and weekends go first. Message us on WhatsApp with two or three possible times and we'll hold the best one. Tell us if it's a special occasion.</p>
<p>Most bookings are partners, but the suite works for any two people who'd like to be treated side by side — friends, siblings, a parent and a grown-up child. Just tell us when you book.</p>
<h3>Giving it as a gift?</h3>
<p>Gift cards are available at face value. See <a href="/offers/">gift cards and prepaid</a>.</p>
"""),
    faqs=[
        ("How much is a couples massage at VĀNA?", "The Couples Signature is ₹5,700 for 90 minutes and ₹6,500 for 120 minutes, for both of you, including the private steam. Two of Us — 90 minutes plus a 30-minute reflexology each — is ₹6,400."),
        ("Can we have different pressures?", "Yes. You each have your own therapist, and each of you answers the intake questions separately."),
        ("Does the couples suite have a steam room?", "Yes, the suite has its own private steam and shower."),
        ("Can I book the couples suite for an anniversary or birthday?", "Of course — tell us when you book so we can prepare the room."),
        ("How far ahead should we book?", "The couples suite is the one room we hold back, and evenings fill first. A few days ahead is safest for Friday to Sunday."),
    ],
    related=["massage-kakkanad", "facials-body-care", "offers"],
    book_msg="Hi, we'd like to book the couples suite at VĀNA.",
    cta_title="Book the couples suite",
))

PAGES.append(dict(
    slug="facials-body-care",
    title="Facials, Body Scrub & Body Wrap in Kakkanad — VĀNA Wellness Spa",
    description="Facials, body scrubs, body wraps and de-tan in Kakkanad, Kochi at VĀNA Wellness Spa. Deep Cleanse, Hydrating and Signature facials from ₹2,300; Forest Scrub and Cocoon Wrap ₹2,200; Scrub & Cocoon ₹3,300.",
    crumb="Facials, scrubs &amp; wraps",
    card_title="Facials, scrubs &amp; wraps", card_text="Three facials, a forest scrub, a cocoon wrap and de-tan.", card_price="From ₹1,200",
    eyebrow="Skin &amp; Body · Kakkanad",
    h1="Facials, body scrubs &amp; wraps in Kakkanad",
    lede="Face, then body. Three facials for three kinds of tired skin, a full-body scrub with natural grains and warm oil, a nourishing cocoon wrap — or both, back to back.",
    facts=[("From ₹2,300", "Facials"), (inr(2200), "Scrub or wrap"), (inr(3300), "Scrub &amp; Cocoon")],
    image="/assets/img/details-oils.jpg", alt="Oils and linens prepared for a body treatment at VĀNA Wellness Spa, Kakkanad",
    service=dict(name="Facials and body treatments", type="Facial and body treatments", keys=["facial_deep", "facial_hyd", "facial_sig", "scrub", "wrap", "scrub_wrap", "detan"]),
    body=section("""
<h2>Facials</h2>
""" + prices(row("facial_deep"), row("facial_hyd"), row("facial_sig")) + """
<p><strong>Which facial?</strong> Oily or congested skin: Deep Cleanse. Dry, tight or dehydrated skin — common after air-conditioned offices: Hydrating. Want the full treatment, including a face massage: VĀNA Signature.</p>
<h2>Body scrub &amp; wrap</h2>
""" + prices(row("scrub"), row("wrap"), row("scrub_wrap"), row("detan")) + """
<h2>Combine with a massage</h2>
""" + prices(combo_row("polished"), combo_row("evening"), combo_row("halfday"), combo_row("afternoon")) + """
<h2>Good to know</h2>
<ul>
<li>Tell us about skin sensitivities, allergies, recent sunburn or recent cosmetic procedures before your treatment.</li>
<li>After a scrub, skip shaving and hot sun for the rest of the day.</li>
<li>Every treatment room has a private bath, so you can shower after a scrub or wrap.</li>
</ul>
"""),
    faqs=[
        ("How much is a facial at VĀNA in Kakkanad?", "The Deep Cleanse Facial (45 min) and Hydrating Facial (60 min) are ₹2,300 each; the VĀNA Signature Facial (60 min) is ₹2,500."),
        ("What is a body wrap?", "A nourishing full-body treatment: the skin is covered and wrapped, then left to rest while it hydrates. Forty-five quiet minutes, and a private bath to shower afterwards."),
        ("Is there a facial pack?", "Yes — Glow Five, five VĀNA Signature Facials for ₹11,000, valid 6 months. See <a href=\"/offers/\">offers and prepaid</a>."),
    ],
    related=["manicure-pedicure-kakkanad", "massage-kakkanad", "couples-spa-kakkanad"],
    book_msg="Hi, I'd like to book a facial / body treatment at VĀNA.",
))

PAGES.append(dict(
    slug="manicure-pedicure-kakkanad",
    title="Manicure & Pedicure in Kakkanad — VĀNA Wellness Spa, Athani",
    description="Manicure and pedicure in Kakkanad, Kochi at VĀNA Wellness Spa. Classic Pedicure ₹1,600, Classic Manicure ₹1,400, Luxury options, and Manicure & Pedicure together (90 min) ₹2,800. Near Infopark, open every day.",
    crumb="Manicure &amp; pedicure",
    card_title="Manicure &amp; pedicure", card_text="Classic and luxury, or both in 90 minutes.", card_price="From ₹1,400",
    eyebrow="Hands &amp; Feet · Kakkanad",
    h1="Manicure &amp; pedicure in Kakkanad",
    lede="Hands and feet, done unhurriedly in a spa rather than a salon chair. Classic for upkeep, Luxury for when they've earned it — or both together in ninety minutes.",
    facts=[(inr(1400), "Classic manicure"), (inr(1600), "Classic pedicure"), (inr(2800), "Both, 90 min")],
    image="/assets/img/balcony-lounge.jpg", alt="The green-view lounge at VĀNA Wellness Spa, Kakkanad",
    service=dict(name="Manicure and pedicure", type="Manicure and pedicure", keys=["mani", "mani_lux", "pedi", "pedi_lux", "mani_pedi"]),
    body=section("""
<h2>Prices</h2>
""" + prices(row("mani"), row("mani_lux"), row("pedi"), row("pedi_lux"), row("mani_pedi"), combo_row("feet"), row("reflexology")) + """
<h2>Classic or Luxury?</h2>
<p>Classic is the 45-minute essential for regular upkeep. Luxury gives you an extra fifteen minutes of care, for hands and feet that need more than a tidy-up. If your feet are carrying a lot, <em>Feet First</em> pairs a 30-minute reflexology with a Classic Pedicure for ₹2,050.</p>
<h2>Regulars</h2>
<p>Hands &amp; Feet Five — five Manicure &amp; Pedicure sessions — is ₹12,500, valid 6 months. See <a href="/offers/">prepaid packs</a>.</p>
"""),
    faqs=[
        ("How much is a manicure and pedicure at VĀNA?", "Classic Manicure ₹1,400, Classic Pedicure ₹1,600, Luxury Manicure ₹2,000, Luxury Pedicure ₹2,300, or Manicure &amp; Pedicure together (90 minutes) for ₹2,800."),
        ("Can I combine a pedicure with a massage?", "Yes. The Whole Afternoon combines a 90-minute massage, scrub, wrap and manicure &amp; pedicure for ₹9,300, or just ask us to book them back to back."),
    ],
    related=["facials-body-care", "massage-kakkanad", "offers"],
    book_msg="Hi, I'd like to book a manicure / pedicure at VĀNA.",
))

PAGES.append(dict(
    slug="spa-near-infopark",
    title="Spa near Infopark, Kochi — Evening Massage in Kakkanad | VĀNA",
    description="A wellness spa a few minutes from Infopark and SmartCity, Kochi. VĀNA in Athani, Kakkanad is open every day until 9–9:30 PM, with 30-minute express resets from ₹700, full massages from ₹2,500 and parking on site.",
    crumb="Spa near Infopark",
    card_title="Spa near Infopark", card_text="After-work massage, open until 9:30 PM.", card_price="From ₹700",
    eyebrow="After work · Near Infopark &amp; SmartCity",
    h1="A spa near Infopark, open into the evening",
    lede="VĀNA is in Athani, Kakkanad — a few minutes from Infopark and SmartCity, with parking on site. We're open every day until 9 PM, and until 9:30 PM Friday to Sunday, so the detour home is short and the evening is still yours.",
    facts=[("Until 9:30 PM", "Fri – Sun"), ("From ₹700", "30-min express"), ("On site", "Parking")],
    image="/assets/img/hero-reception.jpg", alt="The reception at VĀNA Wellness Spa in Athani, Kakkanad, near Infopark",
    service=dict(name="After-work massage near Infopark", type="Massage therapy", keys=["nbs", "head", "reflexology", "deep"]),
    body=section("""
<h2>Built for the Infopark evening</h2>
<p>Most of our guests work in Infopark, SmartCity or around Kakkanad. We shaped the menu around what a day at a desk leaves behind: tight shoulders, a stiff neck, a lower back that aches by six, eyes that need to close.</p>
<h2>30–45 minute resets</h2>
<p>When you have an hour, not an evening.</p>
""" + prices(row("nbs"), row("head"), row("reflexology"), combo_row("desk"), row("fhb"), row("steam")) + """
<h2>When you have the whole evening</h2>
""" + prices(row("deep", "/deep-tissue-massage-kakkanad/"), row("swedish", "/swedish-massage-kakkanad/"), combo_row("evening")) + """
<p>The last session begins 90 minutes before close — so a 90-minute massage can start at 7:30 PM Monday to Thursday, and 8 PM Friday to Sunday.</p>
<h2>Timing tips</h2>
<ul>
<li><strong>Book in the afternoon</strong> on WhatsApp for the same evening; 6–8 PM goes first.</li>
<li><strong>Weekday afternoons are quieter.</strong> The Afternoon membership (₹2,000 a month) is one 60-minute Restore massage on weekdays, 11 AM – 4 PM.</li>
<li><strong>Come straight from work.</strong> Every room has a private bath; steam &amp; shower is included with Deep Tissue and Sports.</li>
</ul>
<p>Read more: <a href="/journal/massage-for-neck-and-shoulder-tension-desk-work/">massage for neck and shoulder tension from desk work</a>.</p>
"""),
    faqs=[
        ("How far is VĀNA from Infopark?", "A few minutes' drive. We're at E Tower, Kollamkudimugal Road, Athani, Kakkanad. <a href=\"" + MAPS_URL + "\" target=\"_blank\" rel=\"noopener\">Open in Google Maps</a> for directions from your building."),
        ("What time do you close?", "9 PM Monday to Thursday and 9:30 PM Friday to Sunday. The last session starts 90 minutes before closing."),
        ("Is there parking?", "Yes, parking is on site."),
        ("Do you offer corporate or team bookings?", "Message us on WhatsApp with what you have in mind and we'll work something out."),
    ],
    related=["deep-tissue-massage-kakkanad", "massage-kakkanad", "offers"],
    book_msg="Hi, I'd like to book an evening session at VĀNA.",
))

PAGES.append(dict(
    slug="offers",
    title="Spa Offers, Memberships & Gift Cards — VĀNA Wellness Spa, Kakkanad",
    description="Opening Month offers at VĀNA Wellness Spa, Kakkanad (18 Sep – 18 Oct 2026), plus monthly massage memberships from ₹2,000, prepaid tiers with up to 43% extra value, treatment packs and gift cards.",
    crumb="Offers &amp; memberships",
    card_title="Offers &amp; memberships", card_text="Opening Month, memberships, prepaid and gift cards.", card_price="From ₹2,000 / month",
    eyebrow="Offers · Memberships · Gift cards",
    h1="Offers, memberships &amp; gift cards",
    lede="Opening Month runs until 18 October 2026. After that, memberships and prepaid tiers are the kindest way to make VĀNA a habit — and gift cards are always at face value.",
    facts=[("18 Oct", "Opening Month ends"), ("₹2,000", "Memberships from / month"), ("Up to 43%", "Extra prepaid value")],
    image="/assets/img/brand-wall.jpg", alt="The VĀNA Wellness Spa name on a sunlit plaster wall",
    cta2="See the offers", cta2_url="#opening-month",
    body=section("""
<h2>Opening Month · 18 September – 18 October 2026</h2>
<p>Say the offer word when you book so we can set it up before you arrive.</p>
<div class="prices">
<div class="price-row"><span class="nm">The Founding Hundred</span><span class="pr">Say "FOUNDING"</span><span class="ds">The first 100 guests of Opening Month become Founding Members for a year: priority on evening slots, Steam &amp; Shower with every massage (already included with Deep Tissue, Sports and the Signature), and once every month, a 60-minute session upgraded to 90 — on us.</span></div>
<div class="price-row"><span class="nm">Come Back in 14 Days</span><span class="pr">Say "RETURN14"</span><span class="ds">Book your second session within 14 days of your first and a Head &amp; Scalp is added to it, complimentary.</span></div>
<div class="price-row"><span class="nm">Bring Someone</span><span class="pr">Say "BRING"</span><span class="ds">Bring a first-time friend to a booking: their Steam &amp; Shower is on us, and your next Express is complimentary.</span></div>
<div class="price-row"><span class="nm">Afternoon Reset</span><span class="pr">Say "AFTERNOON"</span><span class="ds">Weekday afternoons, until 4 PM: any massage includes Steam &amp; Shower, free.</span></div>
<div class="price-row"><span class="nm">Set Aside, Early</span><span class="pr">Say "EARLY"</span><span class="ds">Buy any prepaid tier — Bronze to Platinum — in Opening Month, and your first session is upgraded 60 → 90 minutes, with a Steam &amp; Shower, on us.</span></div>
</div>
<p class="price-note">Offers run 18 September – 18 October 2026 and may be combined with each other, not with other promotions. The Founding Hundred closes at guest 100 or 18 October, whichever comes first; Founding benefits run for one year from your first visit. Complimentary add-ons are subject to room availability on the day.</p>

<h2 id="memberships">Memberships · choose your rhythm</h2>
<div class="prices">
<div class="price-row"><span class="nm">The Monthly</span><span class="pr">₹2,300 / month</span><span class="ds">One 60-minute Restore massage every month — Swedish, Aromatherapy or Balinese. Steam &amp; Shower included, 10% off anything extra that month, priority on evening slots, one month of rollover.</span></div>
<div class="price-row"><span class="nm">The Monthly Deep</span><span class="pr">₹2,500 / month</span><span class="ds">The same rhythm, for Deep Tissue or Sports Recovery.</span></div>
<div class="price-row"><span class="nm">Twice</span><span class="pr">₹4,600 / month</span><span class="ds">Two 60-minute Restore massages a month, for those who'd rather not wait a whole month.</span></div>
<div class="price-row"><span class="nm">The Afternoon</span><span class="pr">₹2,000 / month</span><span class="ds">One 60-minute Restore massage a month, weekdays 11 AM – 4 PM. The quiet hours, kept for you.</span></div>
</div>
<p class="price-note">Six-month term, renewing monthly. Unused sessions roll over one month. Upgrades pay the menu difference.</p>

<h2 id="prepaid">Prepaid · set aside, for later</h2>
<div class="prices">
<div class="price-row"><span class="nm">Bronze</span><span class="pr">Pay ₹10,000</span><span class="ds">Services worth ₹11,750.</span></div>
<div class="price-row"><span class="nm">Silver</span><span class="pr">Pay ₹20,000</span><span class="ds">Services worth ₹25,000.</span></div>
<div class="price-row"><span class="nm">Gold</span><span class="pr">Pay ₹35,000</span><span class="ds">Services worth ₹46,500.</span></div>
<div class="price-row"><span class="nm">Platinum</span><span class="pr">Pay ₹50,000</span><span class="ds">Services worth ₹71,500.</span></div>
<div class="price-row"><span class="nm">Restore Five · Ten</span><span class="pr">₹11,500 · ₹22,500</span><span class="ds">Five or ten 60-minute Restore massages. Five is valid 6 months and shareable with one named person; ten is valid 12 months.</span></div>
<div class="price-row"><span class="nm">Deep Five · Ten</span><span class="pr">₹12,500 · ₹24,500</span><span class="ds">Five or ten Deep Tissue or Sports Recovery sessions, steam included.</span></div>
<div class="price-row"><span class="nm">Reset Pass</span><span class="pr">₹13,500</span><span class="ds">Ten 30-minute Express sessions, for the evenings that need one. Valid 6 months.</span></div>
<div class="price-row"><span class="nm">Together</span><span class="pr">₹15,500</span><span class="ds">Three Couples sessions in the couples suite, steam included. Valid 6 months.</span></div>
<div class="price-row"><span class="nm">Glow Five · Hands &amp; Feet Five</span><span class="pr">₹11,000 · ₹12,500</span><span class="ds">Five Signature Facials, or five Manicure &amp; Pedicure sessions. Valid 6 months.</span></div>
</div>
<p class="price-note">Prepaid value and packs are non-refundable and valid 12 months (packs as shown), redeemable against any treatment. Not combinable with other offers; Founding Member benefits still apply.</p>

<h2 id="gift">Gift cards</h2>
<p>Any amount, any treatment, always at face value. Message us on WhatsApp with the amount and the name to put on it, and we'll arrange it.</p>
""", sid="opening-month"),
    faqs=[
        ("Can I combine Opening Month offers?", "Yes, Opening Month offers can be combined with each other, but not with other promotions."),
        ("Can I share a membership?", "Memberships are personal. The Restore Five pack can be shared with one named person."),
        ("Do you sell gift cards?", "Yes — any amount, at face value. Message us on WhatsApp to arrange one."),
    ],
    related=["massage-kakkanad", "couples-spa-kakkanad", "deep-tissue-massage-kakkanad"],
    book_msg="Hi, I'd like to ask about VĀNA's offers and memberships.",
    cta_title="Ask about an offer",
    cta_text="Message us on WhatsApp with the offer word, or ask us which membership suits how often you'd like to come.",
))

# ── Journal ──────────────────────────────────────────────────────────────────
PAGES.append(dict(
    slug="journal/swedish-vs-deep-tissue-massage",
    title="Swedish vs Deep Tissue Massage: Which Should You Choose? | VĀNA Kakkanad",
    description="Swedish or deep tissue massage? How they differ in pressure, pace and purpose, who each suits, and how to choose — from VĀNA Wellness Spa in Kakkanad, Kochi.",
    crumb="Swedish vs deep tissue", crumbs=[("Journal", SITE + "/journal/")],
    card_title="Swedish vs deep tissue massage", card_text="Which should you choose? Pressure, pace and purpose compared.", card_price="Read the guide",
    eyebrow="Journal · Choosing a massage",
    h1="Swedish vs deep tissue massage: which should you choose?",
    lede="It's the question we hear most on WhatsApp. The short answer: Swedish is for letting go, deep tissue is for a specific knot. Here's the longer one.",
    image="/assets/img/massage.jpg", alt="A massage session at VĀNA Wellness Spa, Kakkanad",
    article="2026-09-25", cta2="Compare side by side", cta2_url="#details",
    body=section("""
<h2>At a glance</h2>
<div class="table-scroll"><table class="compare">
<tr><th></th><th>Swedish massage</th><th>Deep tissue massage</th></tr>
<tr><td>Goal</td><td>Whole-body relaxation, circulation, rest</td><td>Release chronic tension in specific areas</td></tr>
<tr><td>Pressure</td><td>Light to firm — your choice</td><td>Firm, built up slowly</td></tr>
<tr><td>Pace</td><td>Flowing, rhythmic</td><td>Slow, sustained</td></tr>
<tr><td>Coverage</td><td>Whole body, evenly</td><td>Fewer areas, worked longer</td></tr>
<tr><td>Feels like</td><td>Soothing throughout</td><td>Intense in places, never sharp</td></tr>
<tr><td>Next day</td><td>Loose and rested</td><td>Can be a little tender, then easier</td></tr>
<tr><td>At VĀNA</td><td>Swedish Restore · 60 min ₹2,500 · 90 min ₹3,200</td><td>Deep Tissue Release · 60 min ₹2,800 · 90 min ₹3,500, steam included</td></tr>
</table></div>

<h2>What Swedish massage is for</h2>
<p>Swedish massage uses long gliding strokes, kneading and gentle rhythmic movement across the whole body. It's the massage most people picture, and the best place to start if you're new to massage or mostly want to switch off. The pressure can be surprisingly firm if you ask — Swedish doesn't have to mean light.</p>
<p><a href="/swedish-massage-kakkanad/">More about Swedish Restore →</a></p>

<h2>What deep tissue massage is for</h2>
<p>Deep tissue massage slows everything down. The therapist sinks gradually into the deeper layers of muscle using forearms, knuckles and thumbs, and stays on one area long enough for it to let go. It's for the knot under your shoulder blade, the neck that clicks when you turn, the lower back that aches by evening.</p>
<p><a href="/deep-tissue-massage-kakkanad/">More about Deep Tissue Release →</a></p>

<h2>How to choose</h2>
<ul>
<li><strong>Choose Swedish</strong> if it's your first massage, you're stressed or tired rather than sore, or you want to leave feeling light.</li>
<li><strong>Choose deep tissue</strong> if you can point to where it hurts, a lighter massage hasn't lasted, or you spend most of the day at a desk.</li>
<li><strong>Choose neither, yet,</strong> if you have a recent injury, numbness or tingling, or pain that spreads — see a doctor or physiotherapist first.</li>
</ul>
<p>There's a middle path too. <a href="/balinese-massage-kakkanad/">Balinese Harmony</a> is firmer and more active than Swedish but still covers the whole body. And if you train, <a href="/sports-massage-kakkanad/">Sports Recovery</a> is built around the muscles you use.</p>

<h2>Common myths</h2>
<p><strong>"Deep tissue has to hurt to work."</strong> It doesn't. If you're holding your breath or tensing against the pressure, the muscle is fighting back and the session is less effective. Intense is fine; sharp is not.</p>
<p><strong>"Swedish is just a relaxing massage."</strong> Relaxation is the point, but a good Swedish massage still loosens stiff muscles and improves how you feel for days.</p>
<p><strong>"You have to pick one forever."</strong> Many regulars alternate — deep tissue when something's flared up, Swedish when they need rest.</p>

<h2>Still unsure?</h2>
<p>Tell us what's bothering you when you book. The day before, we'll send three short questions on WhatsApp — what hurts, what you're hoping for, what to avoid — and your therapist will shape the session around your answers either way.</p>
"""),
    faqs=[
        ("Is deep tissue massage better than Swedish?", "Neither is better — they do different jobs. Swedish is best for relaxation and general stiffness; deep tissue for specific, long-standing tension."),
        ("Which is better for a first massage?", "Swedish, usually. Your therapist can make it firmer if you'd like."),
        ("Which is better for back pain from sitting?", "Deep tissue, if the tension has built up over weeks or months. For a quick reset, try a 30 or 45-minute Neck, Back &amp; Shoulders session."),
    ],
    related=["deep-tissue-massage-kakkanad", "swedish-massage-kakkanad", "journal/massage-for-neck-and-shoulder-tension-desk-work"],
    book_msg="Hi, I'd like help choosing a massage at VĀNA.",
))

PAGES.append(dict(
    slug="journal/massage-for-neck-and-shoulder-tension-desk-work",
    title="Massage for Neck & Shoulder Tension from Desk Work | VĀNA, near Infopark",
    description="Why desk work tightens your neck, shoulders and upper back, which massage helps, how often to come, and three small habits between sessions — from VĀNA Wellness Spa, a few minutes from Infopark, Kochi.",
    crumb="Desk tension", crumbs=[("Journal", SITE + "/journal/")],
    card_title="Massage for desk tension", card_text="Neck, shoulders and upper back — what helps and how often.", card_price="Read the guide",
    eyebrow="Journal · Desk shoulders",
    h1="Massage for neck and shoulder tension from desk work",
    lede="Laptop neck, Infopark shoulders, the ache between your shoulder blades by six o'clock. Here's why it happens, what massage can do about it, and what it can't.",
    image="/assets/img/treatment-room.jpg", alt="A private treatment room at VĀNA Wellness Spa, near Infopark, Kakkanad",
    article="2026-09-25", cta2="What helps", cta2_url="#details",
    body=section("""
<h2>Why desks do this</h2>
<p>Hours at a screen pull the head forward and round the shoulders. The muscles at the back of the neck and between the shoulder blades hold that position all day, while the chest muscles shorten. By evening, the overworked muscles feel tight and tender — and some develop the familiar knots you can press on and feel.</p>
<p>A long commute, a heavy laptop bag and a phone checked with your chin down don't help.</p>

<h2>What massage can do</h2>
<p>Massage can ease muscle tension, help you notice and drop the shoulders you've been holding up, and make it easier to move and sit well afterwards. Most people also sleep better that night. It works best as part of a rhythm, not a one-off rescue.</p>

<h2>Which session to book</h2>
<ul>
<li><strong>A quick reset after work:</strong> <em>Neck, Back &amp; Shoulders</em>, 30 min ₹1,500 or 45 min ₹1,800.</li>
<li><strong>Tension and a headache-y head:</strong> <em>Desk Rescue</em> — Neck, Back &amp; Shoulders 45 + Head &amp; Scalp — ₹2,500.</li>
<li><strong>Long-standing knots:</strong> <a href="/deep-tissue-massage-kakkanad/">Deep Tissue Release</a>, 60 min ₹2,800 or 90 min ₹3,500, with steam and shower.</li>
<li><strong>Tired all over, not just sore:</strong> <a href="/swedish-massage-kakkanad/">Swedish Restore</a>.</li>
</ul>

<h2>How often?</h2>
<p>If the tension has built over months, two sessions a couple of weeks apart, then every three to four weeks, is a sensible rhythm for many people. The Monthly Deep membership (₹2,500 a month) and the Reset Pass (ten 30-minute Express sessions, ₹13,500) are made for exactly this — see <a href="/offers/">memberships</a>.</p>

<h2>Three small habits between sessions</h2>
<ol>
<li><strong>Raise the screen.</strong> The top of the screen at about eye level, so your head sits over your shoulders.</li>
<li><strong>Move every 45 minutes.</strong> Stand, roll the shoulders back and down five times, look out of a window.</li>
<li><strong>Chin tucks.</strong> Gently draw the chin back — making a double chin — hold for five seconds, ten times. It undoes the forward-head position.</li>
</ol>
<p>Your follow-up note after each VĀNA session will suggest what to carry forward for your own body.</p>

<h2>When to see a doctor first</h2>
<p>Massage is not a substitute for medical care. Numbness, tingling or weakness in the arms or hands, pain that spreads, headaches that are new or severe, or pain after a fall or accident should be checked by a doctor or physiotherapist before you book a massage.</p>

<h2>A few minutes from Infopark</h2>
<p>VĀNA is at E Tower, Athani, Kakkanad, open until 9 PM on weekdays and 9:30 PM Friday to Sunday. See <a href="/spa-near-infopark/">evening sessions near Infopark</a>.</p>
"""),
    faqs=[
        ("What's the best massage for neck and shoulder pain from sitting?", "For long-standing tension, deep tissue. For a quick after-work reset, a 30 or 45-minute Neck, Back &amp; Shoulders session."),
        ("How often should I get a massage for desk tension?", "Many people find every three to four weeks keeps it manageable once the first knots have eased."),
    ],
    related=["deep-tissue-massage-kakkanad", "spa-near-infopark", "journal/swedish-vs-deep-tissue-massage"],
    book_msg="Hi, I'd like to book a session for neck and shoulder tension at VĀNA.",
))

JOURNAL_POSTS = ["journal/swedish-vs-deep-tissue-massage", "journal/massage-for-neck-and-shoulder-tension-desk-work"]

PAGE_INDEX = {p["slug"]: p for p in PAGES}


def build_journal_index():
    items = "".join('<a href="/{}/"><b>{}</b><span>{}</span></a>'.format(s, PAGE_INDEX[s]["card_title"], PAGE_INDEX[s]["description"]) for s in JOURNAL_POSTS)
    p = dict(
        slug="journal",
        title="Journal — Massage & Wellness Notes | VĀNA Wellness Spa, Kakkanad",
        description="Plain-spoken notes on massage and wellness from VĀNA Wellness Spa in Kakkanad, Kochi: choosing a massage, desk tension and more.",
        crumb="Journal",
        eyebrow="Journal",
        h1="Notes from VĀNA",
        lede="Plain-spoken guides to choosing a massage and looking after yourself between sessions — written by the people who run the spa.",
        image="/assets/img/brand-wall.jpg", alt="The VĀNA Wellness Spa name on a sunlit wall",
        cta2="Read the notes", cta2_url="#details",
        body=section('<h2>Latest</h2><div class="posts">{}</div>'.format(items)),
    )
    return p


def main():
    pages = PAGES + [build_journal_index()]
    for p in pages:
        out_dir = os.path.join(ROOT, p["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render(p))
        print("wrote /{}/".format(p["slug"]))

    urls = [("/", "1.0", "weekly")] + [("/{}/".format(p["slug"]), "0.6" if p["slug"].startswith("journal") else "0.8", "monthly") for p in pages]
    body = "".join("  <url>\n    <loc>{}{}</loc>\n    <lastmod>{}</lastmod>\n    <changefreq>{}</changefreq>\n    <priority>{}</priority>\n  </url>\n".format(SITE, u, TODAY, c, pr) for u, pr, c in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
    print("wrote sitemap.xml ({} urls)".format(len(urls)))


if __name__ == "__main__":
    main()
