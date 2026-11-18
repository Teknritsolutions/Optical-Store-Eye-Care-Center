# Oculis — Optical Store & Eye Care Center

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
- Documentation, sitemap, robots.txt, development source generator and compact JSON QA reports.

## Pages and counts

| Page | Main sections |
|---|---:|
| index.html | 10 |
| home-2.html | 10 |
| about.html | 6 |
| products.html | 6 |
| product-details.html | 6 |
| eye-test-booking.html | 6 |
| brands.html | 5 |
| services.html | 6 |
| service-details.html | 5 |
| blog.html | 5 |
| blog-details.html | 5 |
| contact.html | 6 |
| 404.html | 1 |
| coming-soon.html | 1 |

## Documentation

Start with [documentation/index.html](documentation/index.html), [installation](documentation/installation.md), [customization](documentation/customization.md), [integrations](documentation/integrations.md), [asset credits](documentation/image-credits.md) and [QA report](documentation/qa-report.md).

## Scope

Oculis, its labels, people, testimonials, products, prices, premises and hours are fictional demonstration content. No actual appointment, enquiry or subscription is submitted. There is no cart, checkout, dashboard or authentication. Contact details, the map and the sitemap origin must be replaced for production. RTL is layout support with sample Arabic, not a full translation. Chrome testing and available browser limits are recorded in the QA report. Marketplace publication requires your own final review and content verification.

## Development checks

The supplied site works without development dependencies. To rerun the optional audits, install `playwright`, `pillow`, `beautifulsoup4`, `html5lib`, and `tinycss2` in your Python environment, start the local server, and run `python3 tests/visual_qa.py` and `python3 tests/static_audit.py`. The browser script points to the macOS Google Chrome executable; adjust it for your machine.

To regenerate HTML, edit `scripts/build.py` and run `python3 scripts/build.py`. Keep direct HTML edits in sync before regenerating. See the source-formatting script for optional formatting dependencies.

## Project structure

```text
Optical Store & Eye Care Center/
  index.html      Redirect to pages/index.html
  pages/          All website pages, including Homepage 1
  assets/         Styles, JavaScript, images, icons and licensed fonts
  documentation/  Setup, customization, integrations and QA notes
  scripts/        Optional source generation and packaging helpers
  tests/          Audit and browser verification scripts
    artifacts/    Retained JSON QA reports; screenshots are generated locally
  robots.txt
  sitemap.xml
  README.md
```

The duplicate template ZIP, macOS extraction metadata and generated screenshot files have been removed. To create a fresh ZIP when needed, run `python3 scripts/package_template.py`. Browser capture scripts can regenerate screenshots in `tests/artifacts/`.

Secondary page URLs now use `pages/`, for example `pages/about.html`. Configure the host?s missing-page handler to serve `pages/404.html`.

Homepage 1 is `pages/index.html`. The root `index.html` redirects to it and preserves query parameters and fragments.

After regenerating HTML, run `node scripts/refine-heroes.cjs` to reapply the reference-inspired hero layouts and signature logo.
