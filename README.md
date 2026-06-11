# American Barber Institute — Website Rebuild

A ground-up, modern rebuild of **[abi.edu](https://www.abi.edu)** — the American Barber Institute, New York City's only dedicated barber school (est. 1996) — preserving **all original content, pricing, programs, reviews, and photography**, repackaged as a fast, animated, multi-theme static site.

---

## What this is

The original abi.edu is a WordPress site (custom theme, Contact Form 7, NextGEN Gallery). The live site sits behind a bot-protection checkpoint, so the entire site was recovered from the **Wayback Machine**: 78 unique pages (English + Spanish), every archived image (471 photos), all program data, tuition tables, schedules, FAQs, Google reviews, blog articles, and YouTube videos. That content was then rebuilt into this site with a premium barbershop aesthetic informed by research across the best US barber-school and barbershop websites (Tricoci, Premier Barber Institute, Fellow Barber, Blind Barber, Scissors & Scotch).

## Highlights

### 🎨 Four switchable themes
Pick via the dots in the top bar — persisted in `localStorage`, no flash on reload:

| Theme | Personality | Palette |
|---|---|---|
| **Midnight Gold** (default) | Premium NYC barbershop | Charcoal `#101316` · Gold `#c9a227` · Cream |
| **Classic Americana** | Vintage barber pole | Navy `#1a2433` · Barber Red `#b3322e` · Cream |
| **Emerald Lounge** | Gentleman's club | Deep Green `#0e1f19` · Brass `#ab883a` |
| **Crimson Noir** | Modern monochrome | Black `#0b0b0c` · Crimson `#d6203c` |

The entire design system flows through CSS custom properties, so every component re-skins instantly (`html[data-theme]` overrides + `color-mix()` for tinted surfaces).

### ✨ Motion layer ("the site feels alive")
- **Hero**: Ken Burns drift on the photography, drifting gold particle canvas, staggered entrance choreography, shimmer sweep on the headline, floating barber-tool illustrations, bobbing scroll cue
- **Skills marquee** — infinite scrolling ticker of every cut taught (pauses on hover)
- **3D tilt cards** with cursor-tracking glare (pointer devices only)
- **Magnetic buttons** with click ripples and a looping sheen sweep on gold CTAs
- **Parallax** on hero background and split-section imagery
- **Scroll progress bar**, shrinking sticky header, animated barber-pole divider
- **Live countdown** to the next class start (always computes the *true* first Monday of next month — never stale), with a pulse on every tick
- Section headings mask-reveal, kicker lines draw in, staggered card reveals

All motion is transform/opacity only (GPU-friendly), gated behind a `js` class (full content without JavaScript), and **fully disabled under `prefers-reduced-motion`**.

### 📄 Complete content (31 pages)
- **Home** — hero, countdown, 6 program cards, about, skills, requirements, financial aid, $3 menu, Google reviews, gallery, videos, contact form
- **Programs** — hub + detail pages: 500-Hour Master Barber ($4,600–$5,600, 3 schedules with weekly payment plans), 200-Hour Fundamentals ($3,600), 50-Hour Refresher ($1,500), 50-Hour Scalp Micro-Pigmentation ($3,500 w/ tool kit), 3-Hour Contagious Diseases home-study ($100), License Transfer service
- **Financial Aid** + dedicated **Veterans (GI Bill®)** and **ACCESS-VR** pages
- **Admissions** — requirements, 4-step enrollment, schedules, holiday calendar
- **$3 Haircuts** — public services menu + free-haircut coupon form
- **Jobs** — placement office + barbershop owner registration form
- **Gallery** — 229 archived photos with keyboard-navigable lightbox
- **FAQ** (with `FAQPage` schema) · **Contact** (map, subway/bus directions) · **Resources** (state licensing boards) · **Privacy** · **Blog** (9 original articles) · **Spanish landing page** (`/es/`)

### 🔍 SEO & accessibility
`TradeSchool`/`LocalBusiness` + per-program `Course` + `FAQPage` JSON-LD · canonical/OG tags · sitemap.xml · robots.txt · semantic HTML, skip links, focus states, labeled forms, alt text everywhere · sticky mobile Call/Tour bar.

## Stack — zero dependencies

No framework, no npm, no build chain. Hand-written HTML/CSS/JS assembled by a ~200-line Python script. Deploys to any static host as-is.

```
abi-website/
├── build.py              # merges src/pages/* into the base template; emits sitemap + robots
├── vercel.json           # clean URLs, immutable asset caching, security headers
├── index.html …          # 31 generated pages (repo root = deploy root)
├── programs/ blog/ es/   # generated sub-pages
├── assets/
│   ├── css/style.css     # design system + 4 themes (CSS custom properties)
│   ├── css/effects.css   # motion & effects layer
│   ├── js/main.js        # nav, themes, countdown, lightbox, reveals, forms
│   ├── js/effects.js     # particles, tilt, parallax, ripples, progress bar
│   └── img/              # 248 optimized originals from the archived site
└── src/
    ├── pages/            # per-page content partials (edit these, then rebuild)
    ├── make_blog.py      # regenerates blog partials from the site archive
    ├── make_gallery.py   # syncs curated images + regenerates the gallery page
    └── blog_manifest.json
```

## Develop

```bash
python3 build.py                # regenerate all pages after editing src/pages/*
python3 -m http.server 8642     # preview at http://localhost:8642
```

## Deploy

Static output at repo root. On **Vercel**: import the repo, no build command, output directory `.` — `vercel.json` handles clean URLs, caching, and security headers.

## Content provenance

All copy, prices, schedules, requirements, reviews, photos and video links were extracted from archived captures (2023–2025) of the original abi.edu. The raw archive (pages, text extracts, full image set, content inventory) lives outside this repo in `~/Websites/abi-archive/`.

**Contact (ABI):** 48 West 39th Street, NYC 10018 · 121 Westchester Square, Bronx, NY 10461 · (212) 290-2289 EN · (212) 290-0278 ES · admission@abi.edu

---

*GI BILL® is a registered trademark of the U.S. Department of Veterans Affairs (VA).*
