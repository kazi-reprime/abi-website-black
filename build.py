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
<meta property="og:site_name" content="American Barber Institute">
<meta property="og:locale" content="{oglocale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/assets/img/og-cover.jpg">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="author" content="American Barber Institute">
<meta name="geo.region" content="US-NY">
<meta name="geo.placename" content="New York">
<meta name="theme-color" content="#101316">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/css/style.css?v=22">
<link rel="stylesheet" href="{root}assets/css/brand.css?v=22">
<link rel="stylesheet" href="{root}assets/css/landing.css?v=22">
<script>(function(){{try{{if(!localStorage.getItem('abi-theme-user')){{localStorage.removeItem('abi-theme');}}var t=localStorage.getItem('abi-theme');if(t&&t!=='blue')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{root}assets/css/effects.css?v=22">
<script>try{{var t=localStorage.getItem('abi-theme');if(t&&t!=='midnight')document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}</script>
{schema}
</head>
<body style="--page-bg:url('{root}assets/img/{pagebg}')">
<a class="skip" href="#main">Skip to content</a>

<div class="topbar">Start your barber journey today for only $150 per week*<span class="theme-dots" role="group" aria-label="Color theme"><button class="tdot tdot-blue" data-set-theme="blue" aria-label="Blue theme" title="Blue"></button><button class="tdot tdot-midnight" data-set-theme="midnight" aria-label="Midnight theme" title="Midnight"></button><button class="tdot tdot-classic" data-set-theme="classic" aria-label="Classic theme" title="Classic"></button><button class="tdot tdot-emerald" data-set-theme="emerald" aria-label="Emerald theme" title="Emerald"></button><button class="tdot tdot-noir" data-set-theme="noir" aria-label="Noir theme" title="Noir"></button></span></div>
<header class="hdr">
  <div class="hdr-in">
    <a class="logo" href="{root}index.html" aria-label="American Barber Institute — home" title="American Barber Institute">
      <svg class="logo-mark" width="44" height="50" viewBox="0 0 44 50" fill="none" aria-hidden="true" focusable="false">
        <!-- ruler / barber comb-guard -->
        <g class="logo-ruler">
          <rect x="3" y="4" width="9" height="42" rx="2" fill="#0f1116"/>
          <g stroke="#f4c44a" stroke-width="1.1" stroke-linecap="round">
            <line x1="4.6" y1="10" x2="10.4" y2="10"/><line x1="6.4" y1="14" x2="10.4" y2="14"/>
            <line x1="4.6" y1="18" x2="10.4" y2="18"/><line x1="6.4" y1="22" x2="10.4" y2="22"/>
            <line x1="4.6" y1="26" x2="10.4" y2="26"/><line x1="6.4" y1="30" x2="10.4" y2="30"/>
            <line x1="4.6" y1="34" x2="10.4" y2="34"/><line x1="6.4" y1="38" x2="10.4" y2="38"/>
          </g>
        </g>
        <!-- barber pole (continuously rolling) -->
        <defs><clipPath id="abipole"><rect x="24" y="7" width="14" height="36" rx="7"/></clipPath></defs>
        <rect x="24" y="7" width="14" height="36" rx="7" fill="#fff"/>
        <g class="logo-stripes" clip-path="url(#abipole)" stroke-width="5">
          <path d="M14 18 L38 -6" stroke="#e11d2a"/><path d="M14 30 L42 2" stroke="#1b3fd9"/>
          <path d="M14 42 L46 10" stroke="#e11d2a"/><path d="M18 52 L50 20" stroke="#1b3fd9"/>
          <path d="M26 56 L54 28" stroke="#e11d2a"/>
        </g>
        <rect x="24" y="7" width="14" height="36" rx="7" fill="none" stroke="#aab2c0" stroke-width="1.2"/>
        <rect x="22" y="4" width="18" height="5" rx="2.5" fill="#c0c7d2"/>
        <rect x="22" y="41" width="18" height="5" rx="2.5" fill="#c0c7d2"/>
      </svg>
      <span class="logo-text">
        <span class="logo-abi">ABI</span>
        <span class="logo-words">American Barber Institute<sup>&reg;</sup></span>
      </span>
    </a>
    <div class="hdr-phones">
      <a class="phone-pill" href="tel:+12122902289"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span><span class="lbl">English:&nbsp;</span>(212)&nbsp;290-2289</span></a>
      <a class="phone-pill" href="tel:+12122900278"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.08 4.18 2 2 0 0 1 4.06 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.22a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg><span><span class="lbl">Spanish:&nbsp;</span>(212)&nbsp;290-0278</span></a>
    </div>
    <button class="hamburger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
  <nav class="mainnav" aria-label="Main"><a href="{root}about.html">About</a><a href="{root}instructors.html">Instructors</a><a href="{root}programs/index.html">Programs</a><a href="{root}admissions.html">Admissions</a><a href="{root}haircuts.html">$3 Haircuts</a><a href="{root}jobs.html">Jobs</a><a href="{root}gallery.html">Gallery</a><a href="{root}faq.html">FAQs</a><a href="{root}contact.html">Contact</a>
    <span class="mn-lang"><a href="{root}index.html" style="color:var(--blue)">EN</a> | <a href="{root}es/index.html">ES</a></span>
  </nav>
  <nav class="nav-drawer"><div class="container"><a href="{root}index.html">Home</a><a href="{root}about.html">About</a><a href="{root}instructors.html">Instructors</a><a href="{root}programs/index.html">Programs</a><a href="{root}admissions.html">Admissions</a><a href="{root}haircuts.html">$3 Haircuts</a><a href="{root}jobs.html">Jobs</a><a href="{root}gallery.html">Gallery</a><a href="{root}faq.html">FAQs</a><a href="{root}contact.html">Contact</a><a href="{root}es/index.html"><b>Español</b></a></div></nav>
</header>

<main id="main">
{body}
</main>

<section class="trust-strip" aria-label="Why choose ABI">
  <div class="wrap">
    <div class="trust-item"><strong data-count="30" data-suffix="+">30+</strong><span>Years of Experience</span></div>
    <div class="trust-item"><strong data-count="10000" data-suffix="+">10,000+</strong><span>Graduates Trained</span></div>
    <div class="trust-item"><strong>NYS</strong><span>Licensed Barber Program</span></div>
    <div class="trust-item"><strong data-count="100" data-suffix="%">100%</strong><span>Hands-On Training</span></div>
    <div class="trust-item"><strong>2</strong><span>Manhattan &amp; Bronx Campuses</span></div>
    <div class="trust-item"><strong>$150/wk</strong><span>Flexible Payment Plans</span></div>
  </div>
</section>

<section class="cta-band">
  <div class="wrap">
    <p class="kicker" style="justify-content:center">Classes begin the first Monday of each month</p>
    <h2>Ready to Become a Licensed Barber?</h2>
    <p>Next class starts <span data-start-date>soon</span>. Seats fill fast — start your barber school enrollment, request a call, or speak with admissions in English or Spanish.</p>
    <div class="hero-ctas">
      <a class="btn btn-gold btn-lg" href="{root}contact.html">Start Barber School</a>
      <a class="btn btn-ghost btn-lg" href="{root}contact.html">Speak With Admissions</a>
    </div>
  </div>
</section>

<footer class="site">
  <div class="foot-cta">
    <div class="wrap">
      <h3>Start Barber School Today</h3>
      <p>Your new career is one phone call away. Talk to admissions in English or Spanish.</p>
      <div class="foot-cta-btns">
        <a class="btn btn-gold btn-lg" href="{root}contact.html">Request a Call</a>
        <a class="btn btn-blue btn-lg" href="{root}contact.html">Apply Now</a>
        <a class="btn btn-ghost btn-lg" href="tel:+12122902289">Call (212) 290-2289</a>
      </div>
    </div>
  </div>
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h4>American Barber Institute</h4>
        <p>New York's only dedicated barber school — changing lives for over 30 years. Licensed by the New York State Department of Education. Est. 1996.</p>
        <div class="socials">
          <a href="https://www.facebook.com/Abi.Education/" aria-label="Facebook"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-3h-2.8V9.2c0-.9.2-1.5 1.5-1.5h1.4V5.1C16.1 5 15.2 5 14.2 5c-2.2 0-3.7 1.3-3.7 3.8V11H8v3h2.5v7h3z"/></svg></a>
          <a href="https://www.instagram.com/americanbarberinstitute/" aria-label="Instagram"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor" stroke="none"/></svg></a>
          <a href="https://twitter.com/amerbarberedu" aria-label="Twitter / X"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M17.8 3h3l-6.6 7.6L22 21h-6.1l-4.8-6.3L5.6 21h-3l7.1-8.1L2 3h6.3l4.3 5.7L17.8 3zm-1 16.2h1.7L7.3 4.7H5.5l11.3 14.5z"/></svg></a><a href="https://www.youtube.com/channel/UCy_pQUDfk2ldEp6_zyaIMhQ" aria-label="YouTube"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.5 12 4.5 12 4.5s-7 0-8.9.6A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.6 8.9.6 8.9.6s7 0 8.9-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 23.5 12 31 31 0 0 0 23 7.2zM9.8 15.3V8.7L15.9 12l-6.1 3.3z"/></svg></a><a href="https://www.pinterest.com/alexzholendz/american-barber-institute/" aria-label="Pinterest"><svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-3.6 19.3c-.1-.8-.2-2 0-2.9l1.3-5.4s-.3-.7-.3-1.6c0-1.5.9-2.6 2-2.6.9 0 1.4.7 1.4 1.5 0 .9-.6 2.3-.9 3.6-.3 1.1.5 2 1.6 2 1.9 0 3.4-2 3.4-4.9 0-2.6-1.9-4.4-4.5-4.4a4.7 4.7 0 0 0-4.9 4.7c0 .9.4 1.9.8 2.5l-.3 1.1c-.1.4-.3.5-.7.3-1.2-.6-2-2.4-2-3.9 0-3.2 2.3-6.1 6.7-6.1 3.5 0 6.2 2.5 6.2 5.8 0 3.5-2.2 6.3-5.2 6.3-1 0-2-.5-2.3-1.1l-.6 2.4c-.2.9-.8 1.9-1.2 2.6A10 10 0 1 0 12 2z"/></svg></a>
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
        </ul>
      </div>
      <div>
        <h4>Get Started</h4>
        <ul>
          <li><a href="{root}contact.html">Start Barber School</a></li>
          <li><a href="{root}contact.html">Request a Call</a></li>
          <li><a href="{root}admissions.html">Check Class Availability</a></li>
          <li><a href="{root}contact.html">Schedule a Tour</a></li>
          <li><a href="{root}instructors.html">Meet Our Instructors</a></li>
          <li><a href="{root}programs/license-transfer.html">License Transfer</a></li>
        </ul>
      </div>
      <div>
        <h4>Quick Links</h4>
        <ul>
          <li><a href="{root}admissions.html">Admissions &amp; Schedule</a></li>
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
          <li><a href="https://maps.google.com/?q=48+West+39th+Street,+New+York,+NY+10018">Manhattan · 48 West 39th Street<br>New York, NY 10018</a></li>
          <li><a href="tel:+12122902289">(212) 290-2289 (English)</a> · <a href="tel:+12122900278">(212) 290-0278 (Español)</a></li>
          <li><a href="https://maps.google.com/?q=121+Westchester+Square,+Bronx,+NY+10461">Bronx · 121 Westchester Square<br>Bronx, NY 10461</a></li>
          <li><a href="tel:+17186760640">(718) 676-0640 (Bronx)</a></li>
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

<a class="desk-cta" href="{root}contact.html" aria-label="Request a call from admissions">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.8 21 3 13.2 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
  Request a Call
</a>
<button class="to-top" aria-label="Back to top" title="Back to top"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>

<div class="mobile-cta">
  <a class="call" href="tel:+12122902289">
    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.8 21 3 13.2 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
    Call Now
  </a>
  <a class="apply" href="{root}contact.html">Apply Now</a>
</div>

<script>document.getElementById('yr').textContent = new Date().getFullYear();</script>
<script src="{root}assets/js/main.js?v=22" defer></script>
<script src="{root}assets/js/effects.js?v=22" defer></script>
<script src="{root}assets/js/landing.js?v=22" defer></script>
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
    ],
    "areaServed": ["New York City", "Manhattan", "Bronx", "Queens", "Brooklyn", "Westchester", "New Jersey", "Connecticut"],
    "knowsLanguage": ["en", "es"],
    "priceRange": "$$",
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.3", "reviewCount": "100", "bestRating": "5"}
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
def _person(name, role, campus):
    return {"@type": "Person", "name": name, "jobTitle": role,
            "worksFor": {"@type": "EducationalOrganization", "name": "American Barber Institute"},
            "workLocation": campus}
INSTRUCTORS_SCHEMA = {"@context": "https://schema.org", "@type": "ItemList",
    "name": "American Barber Institute Instructors", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": _person(n, r, c)}
        for i, (n, r, c) in enumerate([
            ("David Ayeoribe", "Lead Senior Instructor & Director", "Manhattan, NY"),
            ("Harold \"Barkim\" Brown", "Lead Instructor", "Manhattan, NY"),
            ("Barry Brown", "Instructor", "Manhattan, NY"),
            ("Freddie Liciaga", "Bilingual Instructor", "Manhattan, NY"),
            ("Benny Santamaria", "Bilingual Instructor", "Manhattan, NY"),
            ("Richard Cancel", "Bilingual Instructor", "Manhattan, NY"),
            ("Truth \"The Barber Artist\" Quinones", "Founding Director, ABI Bronx", "Bronx, NY"),
            ("Osvaldy \"Mr. O\" Rodriguez", "Instructor", "Bronx, NY"),
            ("Noah Vera", "Bilingual Instructor", "Bronx, NY"),
        ])]}

PAGES = [
    # (output, partial, title, description, lang, extra_schema)
    ("classic-home.html", "home.html",
     "Barber School NYC | American Barber Institute — 500-Hour Master Barber Program",
     "NYC's only dedicated barber school, est. 1996. NYS-licensed 500-hour Master Barber program, financial aid, veterans GI Bill®, ACCESS-VR & job placement. New classes monthly.",
     "en", [ORG_SCHEMA]),
    ("about.html", "about.html",
     "About Us | American Barber Institute — NYC Barber School Since 1996",
     "Learn about ABI: 3,000 sq ft Midtown Manhattan campus, NYS-licensed curriculum, expert instructors who are all ABI graduates, and our mission to build lifetime barbering careers.",
     "en", []),
    ("instructors.html", "instructors.html",
     "Our Instructors | Master Barber Teachers in NYC | American Barber Institute",
     "Meet ABI's master instructors — including King David Ayeoribe and Emmy-featured Harold \"Barkim\" Brown — with 50+ years of combined experience across our Manhattan and Bronx campuses.",
     "en", [INSTRUCTORS_SCHEMA]),
    ("admissions.html", "admissions.html",
     "Admissions, Requirements & Schedule | American Barber Institute",
     "How to get started at ABI: entrance requirements, class schedules (morning, afternoon, weekend), holiday calendar, and the 4 simple steps to enroll. Classes start monthly.",
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
    ("404.html", "404.html",
     "Page Not Found | American Barber Institute",
     "The page you're looking for doesn't exist. Return to American Barber Institute's homepage or browse our barber programs.",
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
    ("es/classic-home.html", "es-home.html",
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

PAGE_BG = {
    'classic-home.html': 'abi-nyc-003.jpg', 'about.html': 'abi-nyc-007.jpg',
    'instructors.html': 'abi-nyc-008.jpg', 'admissions.html': 'abi-nyc-014.jpg',
    'veterans.html': 'abi-nyc-021.jpeg',
    'access-vr.html': 'abi-nyc-022.jpg', 'haircuts.html': 'abi-nyc-031.jpg',
    'jobs.html': 'abi-nyc-018.jpg', 'gallery.html': 'abi-nyc-035.jpg',
    'faq.html': 'abi-nyc-036.jpg', 'contact.html': 'abi-nyc-037.jpg',
    'resources.html': 'abi-nyc-038.jpg', 'privacy.html': 'abi-nyc-004.jpg',
    'programs/index.html': 'abi-nyc-005.jpg', 'programs/500-hour-master-barber.html': 'abi-nyc-006.jpg',
    'programs/200-hour-barber-fundamentals.html': 'abi-nyc-008.jpg', 'programs/50-hour-barber-refresher.html': 'abi-nyc-009.jpg',
    'programs/scalp-micro-pigmentation.html': 'abi-nyc-010.jpg', 'programs/contagious-diseases.html': 'abi-nyc-013.jpg',
    'programs/license-transfer.html': 'abi-nyc-015.jpg', 'blog/index.html': 'abi-nyc-016.jpg',
}
_DEFAULT_BG = 'abi-nyc-001.jpg'

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
        # BreadcrumbList for every page (entity clarity for AI/answer engines)
        crumb_items = [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"}]
        is_home = out in ('classic-home.html', 'index.html', 'es/classic-home.html')
        if not is_home:
            short = re.sub(r'\s*[|—].*$', '', title).strip()
            crumb_items.append({"@type": "ListItem", "position": 2, "name": short, "item": canonical})
        resolved.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                         "itemListElement": crumb_items})
        schema_tags = '\n'.join(
            f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
            for s in resolved)
        html = TEMPLATE.format(
            lang=lang, title=title, desc=desc, canonical=canonical, site=SITE_URL,
            oglocale='es_ES' if lang == 'es' else 'en_US',
            pagebg=PAGE_BG.get(out.replace('es/', ''), _DEFAULT_BG),
            root=root, body=body, schema=schema_tags,
            lp=root + ('es/' if lang == 'es' else '') + '500-hours-master-barber-program-landing-page/',
            en_cur='aria-current="true"' if lang == 'en' else '',
            es_cur='aria-current="true"' if lang == 'es' else '')
        dest = os.path.join(ROOT, out)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, 'w', encoding='utf-8').write(html)
        if out != '404.html':  # keep the error page out of the sitemap
            written.append(out)
    # sitemap
    written += ['index.html', 'es/index.html', '500-hours-master-barber-program-landing-page/index.html', 'es/500-hours-master-barber-program-landing-page/index.html', 'master-barber-program-bronx/index.html', 'es/master-barber-program-bronx/index.html', 'splash-page-1/index.html', 'splash-page-2/index.html', 'es/splash-page-1/index.html', 'es/splash-page-2/index.html']
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
