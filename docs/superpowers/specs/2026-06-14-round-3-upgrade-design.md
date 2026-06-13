# ABI Website — Round 3 Upgrade (Design Spec)

**Date:** 2026-06-14 · **Branch:** `round-3-upgrade` · **Stack:** static HTML built by `build.py` from `src/pages/*.html` + `assets/`.

## Context
Rounds 1–2 already shipped: 23-photo curated gallery, continuously-rolling SVG logo,
Google Maps links for both campuses, glassmorphism, lighter overlays, instructors + jobs pages.
This round is a **refinement pass**, not a rebuild. Source of truth for content =
`abi-reference-knowledge.md` + verbatim copy scanned from abi.edu (2026-06-14).

## Hard guardrails (audit-safe)
- WCAG AA contrast preserved on all text-over-image and glass surfaces.
- Every animation gated by `prefers-reduced-motion: reduce`.
- Net image weight must **decrease** (audit P1). Convert PNG photo → JPG.
- No broken links; keep round-3 security headers.
- Do NOT touch: lead-form endpoint (needs client Formspree) or analytics (needs GA4 ID). Flag only.

## Decisions (user-approved 2026-06-14)
- Imagery: real `sips` + CSS processing only (no generative AI — no API keys present).
- Instructors: polished no-face monogram cards (real photos drop in later).
- Logo: crisp **animated SVG recreation** of `New-ABI-logo.jpg` (ruler + rolling pole + wordmark).
- Delivery: all 8 workstreams on a branch → user review → push + deploy to Vercel.

## Workstreams
1. **Logo** — replace header SVG in `build.py` TEMPLATE: vertical ruler bar + rolling barber
   pole + bold "ABI" + "AMERICAN BARBER INSTITUTE". Continuous roll, hover speed-up + glow,
   reduced-motion safe. Sharp at all sizes.
2. **Gallery** — curate 23 -> best ~15-18; `sips`-process keepers (auto-lighten, +saturation,
   sharpen, resize <=1600px, recompress, PNG->JPG); refined grid + hover glow; keep lightbox.
3. **Instructors** — keep existing 9 bios; upgrade UI to monogram cards (gradient initials,
   credential chips, specialty tags, campus badges, glass + 3D tilt/glow); add
   "Every Employee, a Graduate" intro. Fix `instructors.html` bg off the heavy PNG.
4. **Jobs** — two-track layout: Barbers (Job Placement + 4 benefit blocks: Four Months Training,
   High Income Potential, Be Your Own Boss, Strong Job Availability) and Shop Owners
   (Shop Registration form, mailto fallback).
5. **Backgrounds** — one lighter people/barber photo per page + soft light scrim so images are
   visible but text stays AA. `sips`-optimized. Clean, not cluttered.
6. **Virtual tour** — embedded tour (replaces link-outs): Manhattan real Street View 360 pano
   (lat 40.75240723, lng -73.98453582, heading 215.05deg); Bronx Street View/map from
   121 Westchester Square; keep 3 YouTube tour videos; glass card + campus tabs.
7. **Interactivity polish** — more glassmorphism, 3D tilt, glow, micro-motion; reduced-motion gated.
8. **Knowledge + ship** — update `abi-reference-knowledge.md`; build; verify in preview;
   bump CSS `?v=19`; push + deploy on approval.

## Verification
- `python3 build.py` succeeds, page count unchanged (~52).
- Preview server: no console errors, logo animates, gallery lightbox works, tour embeds load,
  instructor cards render, jobs two-track renders, backgrounds visible + text readable.
- `assets/img` total weight lower than before.
