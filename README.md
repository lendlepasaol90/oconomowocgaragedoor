# Oconomowoc Garage Door — oconomowocgaragedoor.com

Static website: a homepage plus 14 service pages, served from Cloudflare Workers static assets.

## Structure

- `content/home.json`, `content/services/*.json` — all page copy (homepage ≈3,800 words, each service page 2,200–2,800 words on the page).
- `public/assets/css/site.css` — styles and color palette.
- `public/assets/js/site.js` — motion and interactions.
- `public/images/` — Envato photos, converted to WebP.
- `build.py` — the generator. Site settings are in `SITE` at the top: phone, hours, email, form endpoint, logo and favicon.
- `public/*.html` and `public/*/index.html` are generated. Edit the content or `build.py`, not the HTML.

## Build and deploy

```bash
python3 build.py          # regenerates the HTML in ./public
npx wrangler deploy       # deploys ./public to Cloudflare
```

To preview locally: `cd public && python3 -m http.server 8000`.

## Before going live

1. **Phone**: set `SITE["phone"]` and `SITE["phone_href"]` in `build.py` (currently the placeholder `(262) 000-0000`). Confirm `SITE["hours"]` and `SITE["email"]`.
2. **Quote form**: set `SITE["form_endpoint"]` to a Formspree, Web3Forms or Worker URL. Until then the form validates and shows a thank-you message, but nothing is delivered.
3. **Logo**: put the file in `public/images/` and set `SITE["logo"]` (and optionally a light version in `SITE["logo_footer"]` for the dark footer). Blank = the built-in text wordmark.
4. **Favicon**: add `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192.png`, `icon-512.png` to `public/`, then set `SITE["favicon"] = True`.
5. Run `python3 build.py` after any change.

## Design

New "Lake Country" look, different from the earlier garage door sites: Fraunces serif headlines with italic accents and Manrope body text, arch-shaped photo frames (a nod to the city's lakefront and City Hall architecture), animated lake-wave dividers, glass quote form in the header, low-opacity photo backgrounds on the hero and alternating sections, and one full-width parallax band on the homepage.

Motion: word-by-word headline reveals, arch clip-path image reveals, parallax backgrounds, cursor-follow glow on cards, magnetic buttons, count-up stats, a scroll-linked process timeline, animated ticker, spinning seal, scroll progress bar and a back-to-top progress ring. Everything respects `prefers-reduced-motion`.

## Color palette — soft Oconomowoc "City of Lakes"

Drawn from the blue lake band of the city logo, the water of Lac La Belle and Fowler Lake, the shoreline and the lake sunsets.

| Token | Hex | Use |
|---|---|---|
| Lake blue | `#4a7c94` | Buttons, accents, links |
| Lake hover / text | `#3d6a80` / `#2f566a` | Hover states, small blue text |
| Lake tint / mist | `#e7f0f3` / `#f1f6f8` | Icon chips, tinted sections |
| Deep water | `#1e3442` | Top bar, ticker, dark sections, footer |
| Shoreline sage | `#8fae9c` / `#edf3ef` | Check marks, gradients |
| Beach linen | `#f7f3ec` | Warm alternating sections |
| Lake sunset | `#e2a67e` / `#fbefe6` | Small highlights, badges |
| Ink | `#1b2a33` | Headings |
