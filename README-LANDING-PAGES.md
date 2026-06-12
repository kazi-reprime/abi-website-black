# ABI Landing Pages — Implementation Notes

17 conversion-focused landing pages matching the approved mockup design, generated from one template (`build.py`).

## Pages

| Page | URL path | Language |
|---|---|---|
| Manhattan 500-Hour program | `/500-hours-master-barber-program-landing-page/` | EN |
| Manhattan 500-Hour program | `/es/500-hours-master-barber-program-landing-page/` | ES |
| Bronx Barber Operator program | `/master-barber-program-bronx/` | EN |
| Bronx Barber Operator program | `/es/master-barber-program-bronx/` | ES |
| Splash A ("Your Future. Your Career.") | `/splash-page-1/` | EN + `/es/splash-page-1/` |
| Splash B ("A New Career. In 17 Weeks.") | `/splash-page-2/` | EN + `/es/splash-page-2/` |
| Location SEO pages ×9 | `/barber-school-{queens-ny, brooklyn-new-york, yonkers-new-york, westchester-ny, long-island-ny, mount-vernon-ny, port-chester-ny, connecticut, pennsylvania}/` | EN |

URL paths mirror the live abi.edu structure (canonical + hreflang tags included).

## ⚠️ Two things to do before launch

1. **Lead form endpoint** — open `assets/js/landing.js`, line with `FORM_ENDPOINT`. Create a free form at formspree.io (deliver to admission@abi.edu) and replace `REPLACE_WITH_FORM_ID`. Until then the form shows an error on submit (with the phone number as fallback). Optional: forward Formspree → LeadConnector CRM via webhook/Zapier so leads land in GoHighLevel like the current site.
2. **Hero photos** — drop the approved campus photo at `assets/img/lp-hero.jpg` (and optionally `assets/img/lp-hero-bronx.jpg` for the Bronx pages). Until then pages fall back to `assets/img/about.jpg`, then to the live image on abi-website-black.vercel.app.

## Built-in conversion features

Dynamic "Next Start" date (first Monday of next month, localized EN/ES — fixes the Spanish-date bug on the live site), live countdown timer, sticky mobile Call/CTA bar, chat-style bubble that scrolls to the form, exit-intent popup (desktop, once per session), inline AJAX form with success state + gtag/fbq lead events if analytics are installed, scroll-reveal animations (JS-gated, no-JS safe), JSON-LD TradeSchool schema, full responsive layout.

## Regenerating

Edit copy/data in `build.py`, then: `python3 build.py`

## Research findings worth acting on (from live-site audit)

- Splash pages 1/2 on abi.edu now redirect to the homepage — these rebuilt versions restore them as A/B variants.
- americanbarberinstitute.com shows stale start dates (June 1 / Jan 5, 2026) and its "Spanish" program page is untranslated English.
- On abi.edu, the LeadConnector form appears consent-gated by the cookie banner ("Essential only" → form never loads) — likely losing leads today.
