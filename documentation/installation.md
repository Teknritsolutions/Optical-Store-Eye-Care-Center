# Installation

Open `index.html` directly in a current browser. For a local server, run from the project directory:

```sh
python3 -m http.server 8765
```

Then visit http://localhost:8765. No npm, framework, compilation, external CDN or API key is required. Keep `index.html`, `pages/` and `assets/` together when uploading to any static web host. Configure the host's missing-page handler to serve `pages/404.html`.

All 14 website pages are in `pages/`. The root `index.html` redirects to Homepage 1 at `pages/index.html`, preserving query parameters and fragments. Supporting documentation and a human-readable sitemap are additional utility pages. No dashboard, account, cart or checkout is included.

## GitHub Pages

The workflow in `.github/workflows/deploy-pages.yml` publishes the website when `main` is pushed. In the repository's **Settings > Pages**, select **GitHub Actions** as the source if Pages is not enabled automatically. The deployed root URL opens Homepage 1.

The development-only Python scripts in `scripts/` regenerate the supplied static HTML. End users do not need Python unless using the optional local server.
