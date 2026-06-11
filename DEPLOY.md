# Publishing — 5 minutes, two steps

The repo is fully committed and deploy-ready (`vercel.json` included). Only two things need your login.

## 1 · Private GitHub repository

Go to **https://github.com/new** → name it `abi-website` → select **Private** → Create (do NOT add a README — the repo already has one). Then run:

```bash
cd ~/Websites/abi-website
git remote add origin https://github.com/<YOUR-USERNAME>/abi-website.git
git push -u origin main
```

When git asks for a password, paste a **Personal Access Token** (GitHub → Settings → Developer settings → Tokens → Generate, scope: `repo`).

Repo link will be: `https://github.com/<YOUR-USERNAME>/abi-website`

## 2 · Deploy on Vercel

Go to **https://vercel.com/new** (you're logged in as *kazi-reprime*) → **Import** the `abi-website` repo →
- Framework preset: **Other**
- Build command: **(leave empty)**
- Output directory: **(leave empty / default)**

→ **Deploy**. Done — Vercel reads `vercel.json` automatically (clean URLs like `/about`, immutable asset caching, security headers).

Live link will be: `https://abi-website-<hash>-kazi-reprimes-projects.vercel.app` (plus a stable `abi-website.vercel.app`-style domain shown on the project page).

Every future `git push` auto-deploys.

## Alternative (no GitHub)

```bash
# install Node from https://nodejs.org, then:
cd ~/Websites/abi-website
npx vercel login
npx vercel --prod
```
