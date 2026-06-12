# American Barber Institute — Website & Landing Page System

Modern, bilingual, multi-theme rebuild of **[abi.edu](https://www.abi.edu)** — American Barber Institute, New York City's only dedicated barber school (est. 1996).

**Live:** https://abi-website-black.vercel.app

---

## What was built

| Area | Delivered |
|---|---|
| **Landing pages** | 28 conversion-focused pages from one generator: Manhattan + Bronx program pages, 2 homepage/splash A/B variants, and 9 location SEO pages (Queens, Brooklyn, Yonkers, Westchester, Long Island, Mount Vernon, Port Chester, Connecticut, Pennsylvania) — every one in **English and Spanish** |
| **Hero** | Approved design on every landing page: *"500 Hours. Barber Program. Start Today."* + approved campus photo (`assets/img/lp-hero.jpg`) |
| **Interior site** | ~30 pages (programs, financial aid, admissions, FAQ, gallery, blog, $3 haircuts…) restyled to the same brand with one unified header, logo and nav |
| **Themes** | 5 visitor-selectable color themes (ABI Blue default, Midnight Gold, Classic Americana, Emerald, Crimson Noir) — picked from the top-bar dots, applied pre-paint (no flicker), persisted via `localStorage('abi-theme')` |
| **Alive UI** | Glassmorphism (frosted header/form/cards), ken-burns hero, skills ticker marquee, count-up stats, glow + pulse accents — all honoring `prefers-reduced-motion` |
| **Conversion** | Above-the-fold lead form, live countdown, next-6 start dates, sticky mobile Call/CTA bar, chat bubble → form, exit-intent popup, click-to-call everywhere |
| **Content parity** | Full audit vs. abi.edu + americanbarberinstitute.com: FAQs, tuition plans A/B/C, $3 menu, YouTube videos, gallery, 5 Google reviews, socials, official map embed — nothing left behind |
| **SEO / AI search** | TradeSchool + Course + FAQPage JSON-LD on every landing page, 59-URL sitemap, canonical + hreflang EN⇄ES, `llms.txt`, versioned assets, answer-first FAQ copy |
| **Responsive** | Verified at 8 viewports (iPhone SE → desktop) × 3 page types — zero horizontal overflow, consistent brand on every device |

## Repository structure

```
├── index.html, es/                  # Generated pages (landing system, EN + ES)
├── 500-hours-…/, master-barber-…/   # Program landing pages
├── barber-school-*/                 # 9 location landing pages (EN; ES under es/)
├── splash-page-1/, splash-page-2/   # A/B homepage variants
├── about.html, programs/, blog/, …  # Interior site pages (generated)
├── classic-home.html                # Archived previous homepage
├── assets/
│   ├── css/style.css                # Interior base styles
│   ├── css/brand.css                # ABI Blue brand + theme palettes
│   ├── css/landing.css              # Landing design system + header + themes + motion
│   ├── js/landing.js                # Form, countdown, themes, ticker, stats, facades
│   ├── js/main.js, effects.js       # Interior behavior
│   └── img/                         # All photography (lp-hero.jpg = approved hero)
├── src/
│   ├── pages/*.html                 # Interior content partials
│   └── deploy_vercel.py             # API-based production deploy (no CLI needed)
├── build.py                         # Interior site generator (partials → pages + sitemap)
├── build_landing_pages.py           # Landing page generator (data → 28 pages)
├── vercel.json                      # cleanUrls, caching, headers
├── llms.txt, robots.txt, sitemap.xml
├── README-LANDING-PAGES.md          # Landing system details & launch checklist
└── DEPLOY.md                        # Publishing steps
```

## How it works

Two small Python generators produce every page from data + partials — no framework, no build dependencies, instant static hosting:

```bash
python3 build.py                  # interior pages + sitemap/robots
python3 build_landing_pages.py    # all 28 landing pages
```

Edit copy in `build_landing_pages.py` (FAQs, tuition, translations, locations) or `src/pages/*.html`, rerun, deploy.

## Deploy

```bash
git push                          # version everything
VERCEL_TOKEN=… TEAM_ID=… python3 src/deploy_vercel.py   # production deploy via API
```

See `DEPLOY.md`.

## Before launch (2 items)

1. **Lead form endpoint** — set `FORM_ENDPOINT` in `assets/js/landing.js` (Formspree or LeadConnector webhook). Until then submits show a call-us fallback.
2. **Analytics** — add GA4 / Meta Pixel snippets; lead events (`generate_lead`, `Lead`) already fire on form success.

## How we got here

1. Audited every page of the two legacy sites (content, prices, FAQs, videos, schedules) — including the Spanish pages.
2. Recovered the full site source from the original Vercel deployment via API.
3. Built the landing system to the approved mockup, then unified the whole site behind one header/logo/brand.
4. Added themes, glassmorphism and motion; fixed theme-flip and stale-cache bugs (versioned assets).
5. Enriched with videos, FAQs, reviews, start dates, schema and llms.txt for AI search.
6. Hardened responsiveness across 8 device sizes; everything verified live in production after each push.
