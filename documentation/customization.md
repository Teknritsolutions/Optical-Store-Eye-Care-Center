# Customization

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
