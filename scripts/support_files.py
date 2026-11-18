from page_paths import write_page, page_path
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'scripts/page-manifest.json').read_text())
doc=ROOT/'documentation';doc.mkdir(exist_ok=True)
files={
'installation.md':'''# Installation

Open `index.html` directly in a current browser. For a local server, run from the project directory:

```sh
python3 -m http.server 8765
```

Then visit http://localhost:8765. No npm, framework, compilation, external CDN or API key is required. Keep the HTML pages and `assets/` directory together when uploading to any static web host. Configure the host's missing-page handler to serve `404.html`.

All 14 requested pages are at the project root so the opening page works without redirects. Supporting documentation and a human-readable sitemap are additional utility pages. No dashboard, account, cart or checkout is included.

The development-only Python scripts in `scripts/` regenerate the supplied static HTML. End users do not need Python unless using the optional local server.
''',
'customization.md':'''# Customization

## Brand and theme

Edit `assets/css/styles.css`. The `:root` block contains the exact brand colours (#173B45 and #C5A47E), light surfaces, neutral text, borders, spacing and the 1200px container limit. The `[data-theme=dark]` block contains dark colours. The local variable Manrope font supports weights 200–800. It is licensed under SIL OFL; retain `assets/fonts/OFL.txt`.

`assets/images/logo-light.svg`, `logo-dark.svg`, `favicon.svg`, `favicon.ico` and `apple-touch-icon.png` provide the original eye/lens mark. The header uses an inline version for reliable theme colour inheritance. Brand text is editable SVG text. Keep the logo consistent in the header, footer and brand files.

## Content and navigation

Edit any supplied HTML file directly. Shared component source is also provided in `scripts/build.py`. To regenerate pages after changing that source, run `python3 scripts/build.py`. Reapply source formatting with the optional development tools. Do not regenerate from Python after making HTML-only customizations unless you have ported those changes to the generator.

Product and article data are in `assets/js/data.js`; the matching initial static cards are in the HTML and generator. Update both the data and corresponding static content, or update the Python source and regenerate. Product routes use `product-details.html?id=ellis`; article routes use `blog-details.html?id=lens-guide`. Unknown IDs fall back to the default page. The three-view gallery is available for the default Harper; other products show their own single image and overview. Cross-product size values remain demo specifications and require replacement.

## Local images

All production images have a main WebP and a 480px derivative. Replace both files with the same subject and retain useful alt text. Product photography uses contain; lifestyle photography uses cover. No third-party remote image URL is needed at runtime. Original generation manifests and prompts are included for traceability; paths in manifests point to the development machine and are not production dependencies.

## Direction and accessibility

The direction icon sets `dir=rtl`, and layout uses logical properties. A short Arabic demonstration appears on the booking page. The interface remains English: RTL support is a layout demonstration, not a full Arabic translation. Translate content, labels, validation strings and local data for an Arabic launch. Theme and direction preferences use localStorage when available, with safe in-memory fallback.

The home dropdown opens with click, touch, Enter, Space or Arrow Down. Escape closes it. Mobile navigation exposes its expanded state. FAQs use native details/summary. Testimonials advance manually and never auto-rotate. Reduced-motion preferences disable animation. All form controls have labels and inline errors.

## Before using a real business identity

Replace fictional brand labels, team members, testimonials, prices, specifications, hours and example email. Add verified credentials and business contact details. The contact map is intentionally labelled as a demo location. The `.example` email domain is reserved and not deliverable. Coming-soon social enquiries currently lead to the contact page; replace them with your verified social profile URLs when available. No launch date is claimed.
''',
'integrations.md':'''# Integration boundaries

No endpoint is connected by default. Booking, contact and newsletter submissions validate in the browser and return an explicitly labelled demo preview. Their data is not sent or saved. localStorage is used only for theme and direction preferences. No cookies or analytics are installed.

After `main.js` is loaded, attach an asynchronous adapter:

```js
window.OculisForms.booking = async function (fields) {
  const response = await fetch('/api/appointment-enquiries', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(fields)
  });
  if (!response.ok) throw new Error('Request failed');
  return { message: 'Your enquiry was received. The practice will confirm your appointment.' };
};
```

Use the same contract for `OculisForms.contact` and `OculisForms.newsletter`. Do not put secrets into client JavaScript. Adapters receive validated values, return a user-safe message, and may throw for failure. The submit button is disabled while an adapter is pending. Add appropriate server validation, spam controls, delivery handling and consent for your actual deployment.

Demo appointment times are not live inventory. Replace them with server-provided availability and validate date/time on the server. A request acknowledgement must not imply a confirmed appointment unless the booking backend actually confirms it. The demo avoids collecting medical history.

Replace `.demo-map` in contact.html with an accessible iframe or your map provider's component after verifying your store location. Provide a meaningful title, responsive dimensions and a text address alternative.

`sitemap.xml` uses https://oculis.example as a clearly fictional origin. Replace that origin and set the Sitemap directive in robots.txt to your real deployment URL. The shipped robots.txt blocks indexing to prevent accidental publication of fictional business content; change it deliberately when launching a verified production site.
''',
'image-credits.md':'''# Image and asset credits

All raster content photography in `assets/images/` was created for this project using the built-in OpenAI image generation tool. No reference-site photography, branding, text or source code was copied. The images show fictional people, products and premises, not a real clinical practice.

There are 72 original generated images, each optimized to a local WebP plus a 480px responsive derivative. A small set of unused originals remains as an optional asset library. Images used in different content sections use separate original generations; gallery thumbnails intentionally refer to the same product views as their main image. The same product photo can appear when navigating to that product's own detail route.

Generation names, original development paths and prompt sets are in `scripts/generated-assets*.json` and `documentation/image-prompts.json`. Original PNGs remain in the development environment and are not required by this template. Main assets are capped at 1200px wide. Photographic content is illustrative and should not be used as evidence of actual equipment, staff, medical services or product specifications.

The logo, favicon, face-shape guides, measurement diagram, demo map and 404 illustration are original vector/code assets. Lucide icons are stored locally under `assets/icons/` with their ISC license. Manrope is stored locally under `assets/fonts/` with its SIL Open Font License.

Source links for dependencies:
- Manrope: https://github.com/google/fonts/tree/main/ofl/manrope
- Lucide: https://github.com/lucide-icons/lucide

AI-generated eyewear views are illustrative, not manufacturing renders. Verify product shapes, colour, dimensions and gallery-view consistency before presenting a real catalogue. No marketplace acceptance or exclusivity guarantee is made.
''',
'design-system.md':'''# Design system and reference study

Oculis uses a quiet independent-boutique identity: deep teal #173B45, muted champagne #C5A47E, neutral surfaces, one Manrope font family, a 1200px container and an 8px-based spacing scale. Desktop/tablet/mobile H1 sizes are 52/42/34px; H2 sizes are 38/32/28px. Main section spacing is 80/64/48px. Standard button targets are at least 44px; primary actions are 48px high. Reusable cards use grid and flex layouts to align actions.

The initial web reader failed to access all five supplied URLs. Direct HTTP and Chrome subsequently accessed all five. Their home/menu structures and navigation were reviewed, as were available linked About, Products or Services pages. Desktop 1440px, tablet 820px and mobile 390px reference screenshots and review results are retained in tests/artifacts/references.

- Farm / CSA: consistent containers, alternating information bands, step-by-step membership flow and restrained section spacing.
- Event planning: premium image presentation, clear hierarchy, balanced service grids and calm white space.
- Indie bookstore: legible product metadata, consistent collection grids and straightforward navigation.
- Food truck: visible category filtering and predictable menu-card structure.
- Yarn atelier: editorial product photography, material-focused copy and organized collection storytelling.

Only general layout principles informed this original design. Their logos, images, copy, code and exact page compositions were not reused.

The first homepage follows retail discovery, care, collection, confidence and visit planning. The second uses an editorial headline, wide campaign image, numbered collection rows and an asymmetric product spotlight. Content pages use timelines, a brand directory, form panels, measurement diagrams, a reading sidebar, FAQs and service layouts according to their purpose.
''',
'changelog.md':'''# Changelog

## 1.0.0 — 2026-11-11

- Created all 14 requested static HTML pages with exact main-section counts.
- Added original Oculis branding, local Manrope, Lucide icons and generated local WebP imagery.
- Implemented catalogue search/filter/sort, product routes/gallery, brand directory, article routes/search/categories/load-more, manual testimonials and accessible FAQs.
- Added demo form validation and asynchronous integration adapters.
- Added persistent theme and RTL preferences, Arabic sample content, responsive navigation, reduced-motion handling and skip navigation.
- Added documentation, source generator, sitemap, robots.txt and automated browser QA.
'''
}
for name,text in files.items():(doc/name).write_text(text)
page_table='\n'.join('| '+f+' | '+str(m['sections'])+' |' for f,m in manifest.items())
(doc/'page-structure.md').write_text('# Page structure\n\nThe counts below include only direct main-content sections. Headers, footers and breadcrumbs do not count.\n\n| Page | Main sections |\n|---|---:|\n'+page_table+'\n\n404 and coming-soon use one custom composition each.\n')
readme='''# Oculis — Optical Store & Eye Care Center

A complete traditional HTML5/CSS3/ES6 multipage template. No framework, server integration, npm install or build is required.

Open **index.html**, or run:

```sh
python3 -m http.server 8765
```

Visit **http://localhost:8765**.

## Included

- All 14 requested pages; homepages have exactly 10 main sections each, other content pages exactly 5 or 6.
- Original eye/lens logo, favicon set, Manrope variable font and locally licensed Lucide SVG icons.
- 72 original generated photographs with local responsive WebP files.
- Product filters, search and sorting; detail routes and gallery; searchable brand directory; journal filters, search and load-more; manual testimonial carousel; native FAQ accordions.
- Validated booking, enquiry and newsletter demos with documented API adapters.
- Persistent light/dark mode, LTR/RTL layouts, Arabic sample, mobile navigation, keyboard controls and reduced-motion support.
- Documentation, sitemap, robots.txt, development source generator and browser audit artifacts.

## Pages and counts

| Page | Main sections |
|---|---:|
'''+page_table+'''

## Documentation

Start with [documentation/index.html](documentation/index.html), [installation](documentation/installation.md), [customization](documentation/customization.md), [integrations](documentation/integrations.md), [asset credits](documentation/image-credits.md) and [QA report](documentation/qa-report.md).

## Scope

Oculis, its labels, people, testimonials, products, prices, premises and hours are fictional demonstration content. No actual appointment, enquiry or subscription is submitted. There is no cart, checkout, dashboard or authentication. Contact details, the map and the sitemap origin must be replaced for production. RTL is layout support with sample Arabic, not a full translation. Chrome testing and available browser limits are recorded in the QA report. Marketplace publication requires your own final review and content verification.

## Development checks

The supplied site works without development dependencies. To rerun the optional audits, install `playwright`, `pillow`, `beautifulsoup4`, `html5lib`, and `tinycss2` in your Python environment, start the local server, and run `python3 tests/visual_qa.py` and `python3 tests/static_audit.py`. The browser script points to the macOS Google Chrome executable; adjust it for your machine.

To regenerate HTML, edit `scripts/build.py` and run `python3 scripts/build.py`. Keep direct HTML edits in sync before regenerating. See the source-formatting script for optional formatting dependencies.
'''
(ROOT/'README.md').write_text(readme)
links=''.join(f'<li><a href="{f}">{html.escape(m["title"])}</a> <span>— {f}</span></li>' for f,m in manifest.items())
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>https://oculis.example/{page_path(f)}</loc></url>\n' for f in manifest if f not in ['404.html','coming-soon.html'])+'</urlset>\n')
(ROOT/'robots.txt').write_text('# Demonstration template. Replace fictional content and origin before enabling indexing.\nUser-agent: *\nDisallow: /\n# Production example: Sitemap: https://your-domain.example/sitemap.xml\n')
items=''.join('<li><a href="'+name+'">'+name.replace('.md','').replace('-',' ').title()+'</a></li>' for name in files)
(doc/'index.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Oculis documentation</title><link rel="stylesheet" href="../assets/css/styles.css"><link rel="icon" href="../assets/images/favicon.svg"></head><body><main class="container section"><p class="eyebrow">OCULIS / TEMPLATE GUIDE</p><h1>A clearer starting point.</h1><p class="lead" style="margin-block:24px">A complete, buildless optical store HTML template. Open the guides below as text, or in a Markdown viewer.</p><ul>'+items+'<li><a href="page-structure.md">Page structure</a></li><li><a href="qa-report.md">Quality audit</a></li></ul><a class="button" href="../index.html">Explore the website →</a></main></body></html>')
print('Wrote README, documentation, sitemap and robots.txt.')
