# Pre-Change Git State — ABI Black site

Recorded: 2026-06-18 (UTC), before any upgrade implementation.

| Field | Value |
|---|---|
| Repo path | `/Users/mkazi/ABI/abi-website` |
| GitHub | `kazi-reprime/abi-website-black` |
| Default branch | `main` |
| Upgrade branch | `upgrade/abi-black-mobile-content` |
| Baseline commit | `565aa08 (Final cleanup & restructure)` |
| Vercel project | `abi-website` |
| Git author | kazi-reprime <kazi@reprime.com> |
| Working tree at start | preserved (see notes) |

## Notes
Brand-new GitHub repo created this session; `main` initialized from the current live baseline. Working tree was clean at start.

## Safety rules honored
- Branched off baseline; `main` is not modified.
- No force-push, no reset, no discarded work.
- Secrets are not committed; `.git/config` token scrubbed where present.
- No merge to `main` will occur without explicit user approval.

## Scraped source collection
- Public scrape (85 pages, EN+ES): `/Users/mkazi/website-source-collection/abi-app-123.vercel.app/`
- Authenticated backend data (agent token): `/Users/mkazi/website-source-collection/abi-app-123.vercel.app/authenticated/`
  (courses, jobs(373), gallery_items(75), blog_posts(8), profiles, shop_registrations)
