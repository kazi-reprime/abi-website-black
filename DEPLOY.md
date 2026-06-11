# Publishing

**Status: published.**
- Private repo: https://github.com/kazi-reprime/abi-website
- Production: https://abi-website-black.vercel.app (project `abi-website` on kazi-reprime's Vercel)

## Redeploy after changes

```bash
python3 build.py                                   # regenerate pages
git add -A && git commit -m "..." && git push      # update the private repo
VERCEL_TOKEN=<token> TEAM_ID=team_r7ntBJYf1JjAgTA6CPs7hWsQ python3 src/deploy_vercel.py
```

`src/deploy_vercel.py` uploads the site files and creates a production deployment through the Vercel REST API — no Node/CLI required.

Optional: connect the GitHub repo to the Vercel project (vercel.com → abi-website → Settings → Git) so every `git push` auto-deploys instead.

> Security note: never commit tokens. The deploy script only reads them from environment variables. Rotate any token that has been shared in plain text.
