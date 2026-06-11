#!/usr/bin/env python3
"""Static site builder for the American Barber Institute website.
Merges src/pages/*.html content partials into the base template.
Usage: python3 build.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src', 'pages')
SITE_URL = 'https://www.abi.edu'

# ---------------------------------------------------------------- template
TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site}/assets/img/og-cover.jpg">
<meta name="theme-color" content="#101316">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css">
<link rel="stylesheet" href="{root}assets/css/effects.css">
<script>try{{var t=localStorage.getItem('abi-theme');if(t&&t!=='midnight')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
{schema}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<div class="topbar">
  <div class="wrap">
    <div>Schedule your tour today! <a href="tel:+12122902289">(212) 290-2289</a> English · <a href="tel:+12122900278">(212) 290-0278</a> Español</div>
    <div style="display:flex;align-items:center;gap:22px">
      <div class="theme-picker" role="group" aria-label="Color theme">
        <span class="tp-label">Theme</span>
        <button class="theme-dot t-midnight" data-theme="midnight" aria-pressed="true" aria-label="Midnight Gold theme" title="Midnight Gold"></button>
        <button class="theme-dot t-classic" data-theme="classic" aria-pressed="false" aria-label="Classic Americana theme" title="Classic Americana"></button>
        <button class="theme-dot t-emerald" data-theme="emerald" aria-pressed="false" aria-label="Emerald Lounge theme" title="Emerald Lounge"></button>
        <button class="theme-dot t-noir" data-theme="noir" aria-pressed="false" aria-label="Crimson Noir theme" title="Crimson Noir"></button>
      </div>
      <div class="langs"><a href="{root}index.html" {en_cur}>EN</a>&nbsp;|&nbsp;<a href="{root}es/index.html" {es_cur}>ES</a></div>
    </div>
  </div>
</div>

<header class="site-head">
  <div class="wrap">
    <a class="brand" href="{root}index.html" aria-label="American Barber Institute home">
      <svg width="40" height="40" viewBox="0 0 48 48" fill="none" aria-hidden="true">
        <rect x="2" y="2" width="44" height="44" rx="8" fill="#c9a227"/>
        <rect x="19" y="6" width="10" height="36" rx="5" fill="#101316"/>
        <path d="M19 12 L29 18 M19 22 L29 28 M19 32 L29 38" stroke="#c9a227" stroke-width="3.4" stroke-linecap="round"/>
        <circle cx="24" cy="6.5" r="3.2" fill="#101316"/>
      </svg>
      <span><b>American Barber<br>Institute</b><small>NYC · Est. 1996</small></span>
    </a>
    <nav class="nav" aria-label="Main">
      <div class="has-sub">
        <a href="{root}about.html">About</a>
        <div class="sub">
          <a href="{root}about.html">About ABI &amp; Mission</a>
          <a href="{root}about.html#instructors">Our Instructors</a>
          <a href="{root}about.html#skills">Skills &amp; Techniques</a>
          <a href="{root}about.html#tour">Virtual Tour</a>
        </div>
      </div>
      <div class="has-sub">
        <a href="{root}programs/index.html">Programs</a>
        <div class="sub">
          <a href="{root}programs/500-hour-master-barber.html">500-Hour Master Barber (4 Months)</a>
          <a href="{root}programs/200-hour-barber-fundamentals.html">200-Hour Barber Fundamentals</a>
          <a href="{root}programs/50-hour-barber-refresher.html">50-Hour Barber Refresher</a>
          <a href="{root}programs/scalp-micro-pigmentation.html">50-Hour Scalp Micro-Pigmentation</a>
          <a href="{root}programs/contagious-diseases.html">3-Hour Contagious Diseases</a>
          <a href="{root}programs/license-transfer.html">License Transfer</a>
        </div>
      </div>
      <div class="has-sub">
        <a href="{root}financial-aid.html">Financial Aid</a>
        <div class="sub">
          <a href="{root}financial-aid.html">Financial Aid Options</a>
          <a href="{root}veterans.html">Veterans · GI Bill®</a>
          <a href="{root}access-vr.html">ACCESS-VR Program</a>
        </div>
      </div>
      <a href="{root}admissions.html">Admissions</a>
      <a href="{root}haircuts.html">$3 Haircuts</a>
      <div class="has-sub">
        <a href="{root}jobs.html">Jobs</a>
        <div class="sub">
          <a href="{root}jobs.html">Job Placement</a>
          <a href="{root}jobs.html#shops">Shop Registration</a>
        </div>
      </div>
      <a href="{root}gallery.html">Gallery</a>
      <a href="{root}faq.html">FAQs</a>
      <a href="{root}contact.html">Contact</a>
    </nav>
    <a class="btn btn-gold head-cta" href="{root}contact.html">Book a Tour</a>
    <button class="menu-btn" aria-label="Open menu" aria-expanded="false">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
  </div>
</header>

<main id="main">
{body}
</main>

<section class="cta-band">
  <div class="wrap">
    <p class="kicker" style="justify-content:center">Classes begin the first Monday of each month</p>
    <h2>Next class starts <span data-start-date>soon</span></h2>
    <p>Seats fill fast. Call us, book a tour, or apply today — our admissions team will guide you every step of the way, in English or Spanish.</p>
    <div class="hero-ctas">
      <a class="btn btn-gold btn-lg" href="{root}contact.html">Get More Info</a>
      <a class="btn btn-ghost btn-lg" href="tel:+12122902289">Call (212) 290-2289</a>
    </div>
  </div>
</section>

<footer class="site">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>American Barber Institute</h4>
        <p>New York's only dedicated barber school — changing lives for over 30 years. Licensed by the New York State Department of Education. Est. 1996.</p>
        <div class="socials">
          <a href="https://www.facebook.com/Abi.Education/" aria-label="Facebook"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.2-1.5 1.5-1.5h1.4V5.1C16.1 5 15.2 5 14.2 5c-2.2 0-3.7 1.3-3.7 3.8V11H8v3h2.5v7h3z"/></svg></a>
          <a href="https://www.instagram.com/americanbarberinstitute/" aria-label="Instagram"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></svg></a>
          <a href="https://twitter.com/amerbarberedu" aria-label="Twitter / X"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M17.8 3h3l-6.6 7.6L22 21h-6.1l-4.8-6.3L5.6 21h-3l7.1-8.1L2 3h6.3l4.3 5.7L17.8 3zm-1 16.2h1.7L7.3 4.7H5.5l11.3 14.5z"/></svg></a>
        </div>
      </div>
      <div>
        <h4>Programs</h4>
        <ul>
          <li><a href="{root}programs/500-hour-master-barber.html">500-Hour Master Barber</a></li>
          <li><a href="{root}programs/200-hour-barber-fundamentals.html">200-Hour Fundamentals</a></li>
          <li><a href="{root}programs/50-hour-barber-refresher.html">50-Hour Refresher</a></li>
          <li><a href="{root}programs/scalp-micro-pigmentation.html">Scalp Micro-Pigmentation</a></li>
          <li><a href="{root}programs/contagious-diseases.html">Contagious Diseases Course</a></li>
          <li><a href="{root}programs/license-transfer.html">License Transfer</a></li>
        </ul>
      </div>
      <div>
        <h4>Quick Links</h4>
        <ul>
          <li><a href="{root}admissions.html">Admissions &amp; Schedule</a></li>
          <li><a href="{root}financial-aid.html">Financial Aid</a></li>
          <li><a href="{root}veterans.html">Veterans · GI Bill®</a></li>
          <li><a href="{root}access-vr.html">ACCESS-VR</a></li>
          <li><a href="{root}haircuts.html">$3 Haircut Menu</a></li>
          <li><a href="{root}resources.html">Resources</a></li>
          <li><a href="{root}blog/index.html">Blog</a></li>
        </ul>
      </div>
      <div>
        <h4>Visit Us</h4>
        <ul>
          <li><a href="https://maps.google.com/?q=48+West+39th+Street,+New+York,+NY+10018">48 West 39th Street<br>New York, NY 10018</a></li>
          <li><a href="https://maps.google.com/?q=121+Westchester+Square,+Bronx,+NY+10461">121 Westchester Square<br>Bronx, NY 10461</a></li>
          <li><a href="tel:+12122902289">(212) 290-2289 (English)</a></li>
          <li><a href="tel:+12122900278">(212) 290-0278 (Español)</a></li>
          <li><a href="mailto:admission@abi.edu">admission@abi.edu</a></li>
          <li>Mon–Fri · 8:00 AM – 8:00 PM</li>
        </ul>
      </div>
    </div>
  </div>
  <div class="foot-legal">
    <div class="wrap">
      <div>© <span id="yr"></span> American Barber Institute (ABI). All rights reserved. · <a href="{root}privacy.html">Privacy Policy</a></div>
      <div>GI BILL® is a registered trademark of the U.S. Department of Veterans Affairs (VA). Info: <a href="https://www.benefits.va.gov/gibill" rel="noopener">benefits.va.gov/gibill</a></div>
    </div>
  </div>
</footer>

<div class="mobile-cta">
  <a class="call" href="tel:+12122902289">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.8 21 3 13.2 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
    Call Now
  </a>
  <a class="apply" href="{root}contact.html">Book a Tour</a>
</div>

<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
<script src="{root}assets/js/main.js" defer></script>
<script src="{root}assets/js/effects.js" defer></script>
</body>
</html>
"""

ORG_SCHEMA = {
    "@context": "https://schema.org",
    "@type": ["TradeSchool", "LocalBusiness"],
    "name": "American Barber Institute",
    "alternateName": "ABI",
    "url": SITE_URL,
    "logo": SITE_URL + "/assets/img/favicon.svg",
    "foundingDate": "1996",
    "description": "New York's only dedicated barber school. NYS-licensed 500-hour Master Barber program in Midtown Manhattan with financial aid, veterans GI Bill and ACCESS-VR options, and job placement.",
    "telephone": "+1-212-290-2289",
    "email": "admission@abi.edu",
    "address": [{
        "@type": "PostalAddress",
        "streetAddress": "48 West 39th Street",
        "addressLocality": "New York",
        "addressRegion": "NY",
        "postalCode": "10018",
        "addressCountry": "US"
    }, {
        "@type": "PostalAddress",
        "streetAddress": "121 Westchester Square",
        "addressLocality": "Bronx",
        "addressRegion": "NY",
        "postalCode": "10461",
        "addressCountry": "US"
    }],
    "geo": {"@type": "GeoCoordinates", "latitude": 40.7522, "longitude": -73.9849},
    "openingHours": "Mo-Fr 08:00-20:00",
    "sameAs": [
        "https://www.facebook.com/Abi.Education/",
        "https://www.instagram.com/americanbarberinstitute/",
        "https://twitter.com/amerbarberedu"
    ]
}

def course_schema(name, desc, hours, weeks, price):
    return {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": name,
        "description": desc,
        "provider": {"@type": "TradeSchool", "name": "American Barber Institute", "url": SITE_URL},
        "offers": {"@type": "Offer", "price": str(price), "priceCurrency": "USD", "category": "Tuition"},
        "hasCourseInstance": {
            "@type": "CourseInstance",
            "courseMode": "onsite",
            "courseWorkload": f"PT{hours}H",
            "location": {"@type": "Place", "name": "American Barber Institute",
                         "address": "48 West 39th Street, New York, NY 10018"}
        },
        "totalHistoricalEnrollment": None,
        "timeRequired": f"P{weeks}W"
    }

# ---------------------------------------------------------------- pages
PAGES = [
    # (output, partial, title, description, lang, extra_schema)
    ("index.html", "home.html",
     "Barber School NYC | American Barber Institute — 500-Hour Master Barber Program",
     "NYC's only dedicated barber school, est. 1996. NYS-licensed 500-hour Master Barber program, financial aid, veterans GI Bill®, ACCESS-VR & job placement. New classes monthly.",
     "en", [ORG_SCHEMA]),
    ("about.html", "about.html",
     "About Us | American Barber Institute — NYC Barber School Since 1996",
     "Learn about ABI: 3,000 sq ft Midtown Manhattan campus, NYS-licensed curriculum, expert instructors who are all ABI graduates, and our mission to build lifetime barbering careers.",
     "en", []),
    ("admissions.html", "admissions.html",
     "Admissions, Requirements & Schedule | American Barber Institute",
     "How to get started at ABI: entrance requirements, class schedules (morning, afternoon, weekend), holiday calendar, and the 4 simple steps to enroll. Classes start monthly.",
     "en", []),
    ("financial-aid.html", "financial-aid.html",
     "Financial Aid | NYSDOL Grant, ACCESS-VR & GI Bill® | American Barber Institute",
     "Financial assistance for those who qualify: NYSDOL Grant, ACCESS-VR, Veterans GI Bill®, and weekly payment plans on every program. Pay while you attend school.",
     "en", []),
    ("veterans.html", "veterans.html",
     "Veterans Program — GI Bill® Approved Barber Training | American Barber Institute",
     "VA-approved barber training in NYC under Title 38 USC § 3676. Use your GI Bill® benefits to become a licensed Master Barber. We guide you through every step.",
     "en", []),
    ("access-vr.html", "access-vr.html",
     "ACCESS-VR Program — Tuition Covered Barber Training | American Barber Institute",
     "ACCESS-VR pays tuition, tools and books for qualified New Yorkers with disabilities. Train as a barber at ABI with full vocational rehabilitation support.",
     "en", []),
    ("haircuts.html", "haircuts.html",
     "$3 Haircuts in Manhattan — Services Menu | American Barber Institute",
     "Get a quality $3 haircut by supervised student barbers in Midtown Manhattan: fades, tapers, shape-ups, razor shaves and more. Free haircut coupon available.",
     "en", []),
    ("jobs.html", "jobs.html",
     "Job Placement & Shop Registration | American Barber Institute",
     "ABI maintains a full-time job placement office. Graduates often finish with multiple offers. Barbershop owners: register your shop to hire our trained graduates.",
     "en", []),
    ("gallery.html", "gallery.html",
     "Gallery — Student Work & Campus | American Barber Institute",
     "See our students' haircuts, our 3,000 sq ft Midtown Manhattan campus, and life at New York's only dedicated barber school.",
     "en", []),
    ("faq.html", "faq.html",
     "Frequently Asked Questions | American Barber Institute",
     "Answers about tuition costs, program length, schedules, age requirements, ACCESS-VR, job placement, and why students choose ABI.",
     "en", ["FAQ_SCHEMA"]),
    ("contact.html", "contact.html",
     "Contact & Directions | American Barber Institute — Midtown Manhattan",
     "Visit ABI at 48 West 39th Street, NYC — minutes from Penn Station, Grand Central & Times Square. Call (212) 290-2289 or book your free tour today.",
     "en", [ORG_SCHEMA]),
    ("resources.html", "resources.html",
     "Barbering Resources & State Licensing Boards | American Barber Institute",
     "Regulatory agencies, state-by-state barber and cosmetology licensing boards, education resources and industry associations.",
     "en", []),
    ("privacy.html", "privacy.html",
     "Privacy Policy | American Barber Institute",
     "How American Barber Institute collects, uses, and protects your personal information.",
     "en", []),
    ("programs/index.html", "programs-index.html",
     "Barber Programs in NYC | American Barber Institute",
     "Compare ABI's NYS-licensed programs: 500-hour Master Barber, 200-hour Fundamentals, 50-hour Refresher, Scalp Micro-Pigmentation, Contagious Diseases course & License Transfer.",
     "en", []),
    ("programs/500-hour-master-barber.html", "program-500.html",
     "500-Hour Master Barber Program (4 Months) | American Barber Institute",
     "Become a licensed Master Barber in NY in 4 months. Morning, afternoon or weekend schedules from $4,600 with weekly payment plans. NYS Board Exam prep & job placement.",
     "en", [course_schema("500 Hour Master Barber Program",
        "Four-month NYS-licensed master barber training: theory, practical work on real clients, State Board exam prep and job placement.", 500, 17, 4600)]),
    ("programs/200-hour-barber-fundamentals.html", "program-200.html",
     "200-Hour Barber Fundamentals Program (2 Months) | American Barber Institute",
     "Hands-on 200-hour barbering fundamentals for apprentices and licensed cosmetologists. $3,600 with a weekly payment plan. Monday–Friday afternoons.",
     "en", [course_schema("200 Hour Barber Fundamentals Program",
        "Two-month program training apprentice registrants and licensed cosmetologists in practical and theoretical barbering.", 200, 8, 3600)]),
    ("programs/50-hour-barber-refresher.html", "program-50.html",
     "50-Hour Barber Refresher Program (2 Weeks) | American Barber Institute",
     "Sharpen your skills and prepare for the NY State Board Exam in 2 weeks. For cosmetologists, hairdressers and barber apprentices. $1,500 with split payments.",
     "en", [course_schema("50 Hour Barber Refresher Program",
        "Two-week refresher preparing licensed professionals for the New York State Barbering Licensing Examination.", 50, 2, 1500)]),
    ("programs/scalp-micro-pigmentation.html", "program-smp.html",
     "50-Hour Scalp Micro-Pigmentation Program | American Barber Institute",
     "Weekend SMP certification in NYC: hairline design, pigments, device work and client care. $3,500 including tool kit, over 4 weekends.",
     "en", [course_schema("50 Hour Scalp Micro-Pigmentation Program",
        "Weekend program teaching scalp micro-pigmentation: hairline design, pigment selection, hygiene and client care.", 50, 4, 3500)]),
    ("programs/contagious-diseases.html", "program-cd.html",
     "3-Hour Contagious Diseases Program (Home Study) — $100 | American Barber Institute",
     "NY-required Transmission of Contagious Diseases course for barber operators and apprentices. Complete by mail for $100 — booklet, exam and two certificates.",
     "en", [course_schema("3 Hours Contagious Diseases Program",
        "Home-study course on transmission of contagious diseases, sanitation and sterilization required for NY barber licensure.", 3, 1, 100)]),
    ("programs/license-transfer.html", "program-lt.html",
     "NY Barber & Cosmetology License Transfer Service | American Barber Institute",
     "Working with a license from another state or country? ABI manages your entire NYS licensure or reciprocity application from start to finish.",
     "en", []),
    ("blog/index.html", "blog-index.html",
     "Blog — Barbering Career Advice & News | American Barber Institute",
     "Advice from NYC's only dedicated barber school: licensing, careers, shop ownership, marketing your barbershop, and life after barber school.",
     "en", []),
    ("es/index.html", "es-home.html",
     "Escuela de Barbería en NYC | American Barber Institute",
     "La única escuela dedicada a la barbería en Nueva York, desde 1996. Programa de Master Barber de 500 horas con licencia del Estado de NY, ayuda financiera y colocación laboral. Llame al (212) 290-0278.",
     "es", [ORG_SCHEMA]),
]

# blog posts generated by src/make_blog.py
_blog_manifest = os.path.join(ROOT, 'src', 'blog_manifest.json')
if os.path.exists(_blog_manifest):
    for _p in json.load(open(_blog_manifest)):
        PAGES.append((
            f"blog/{_p['slug']}.html", _p['partial'],
            f"{_p['title']} | American Barber Institute Blog",
            f"{_p['title']} — career advice and industry insight from NYC's only dedicated barber school.",
            "en", []))

FAQ_SCHEMA_PLACEHOLDER = "FAQ_SCHEMA"

def faq_schema_from(body):
    """Build FAQPage JSON-LD from the faq partial's <summary>/<div class="a"> pairs."""
    qa = re.findall(r'<summary>(.*?)</summary>\s*<div class="a">(.*?)</div>', body, re.S)
    items = []
    for q, a in qa:
        clean_a = re.sub(r'<[^>]+>', ' ', a)
        clean_a = re.sub(r'\s+', ' ', clean_a).strip()
        items.append({"@type": "Question", "name": re.sub(r'<[^>]+>', '', q).strip(),
                      "acceptedAnswer": {"@type": "Answer", "text": clean_a}})
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": items}

def build():
    written = []
    for out, partial, title, desc, lang, schemas in PAGES:
        path = os.path.join(SRC, partial)
        if not os.path.exists(path):
            print(f'  !! missing partial {partial} — skipped')
            continue
        body = open(path, encoding='utf-8').read()
        depth = out.count('/')
        root = '../' * depth
        canonical = f"{SITE_URL}/{out}".replace('/index.html', '/')
        resolved = []
        for s in schemas:
            if s == FAQ_SCHEMA_PLACEHOLDER:
                resolved.append(faq_schema_from(body))
            else:
                resolved.append(s)
        schema_tags = '\n'.join(
            f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
            for s in resolved)
        html = TEMPLATE.format(
            lang=lang, title=title, desc=desc, canonical=canonical, site=SITE_URL,
            root=root, body=body, schema=schema_tags,
            en_cur='aria-current="true"' if lang == 'en' else '',
            es_cur='aria-current="true"' if lang == 'es' else '')
        dest = os.path.join(ROOT, out)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(html)
        written.append(out)
    # sitemap
    urls = '\n'.join(
        f'  <url><loc>{SITE_URL}/{o}</loc></url>'.replace('/index.html', '/')
        for o in written)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(
        f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n')
    print(f'built {len(written)} pages + sitemap.xml + robots.txt')

if __name__ == '__main__':
    build()
