# Knit & Denim Sourcing: MVP website

Static, dependency-free multi-page site (HTML + CSS + vanilla JS). No build step is needed to host it.

## Structure
- `site/`: deployable site (8 pages, `assets/`, `sitemap.xml`, `robots.txt`)
- `build.py`: optional generator. Edit copy there and run `python3 build.py site` to regenerate the pages.
- Design system: `site/assets/css/styles.css` (tokens at the top: ivory, charcoal, indigo, taupe, white; Cormorant Garamond + DM Sans)
- Behaviour: `site/assets/js/main.js` (mobile nav, scroll reveals, form validation). Animations honour `prefers-reduced-motion`.

## Deploy
1. Upload the contents of `site/` to any static host (Netlify, Vercel static, Cloudflare Pages, GitHub Pages, cPanel) and point knitanddenimsourcing.com at it.
2. Replace the placeholder email `hello@knitanddenimsourcing.com` (set in `build.py`, then rebuild).
3. Connect the form (below) and submit `sitemap.xml` to Google Search Console.

## Connect the inquiry form
The form currently validates and shows a success message only (prototype); nothing is sent. Options:
- **Formspree / Basin / Web3Forms (fastest):** set `action` on `#inquiry-form` to the endpoint URL. In `main.js`, replace the block marked `PROTOTYPE` with the commented `fetch(...)` call. These services also accept file uploads on paid tiers.
- **Netlify Forms:** add `data-netlify="true"` and `name="inquiry"` to the form (hidden `form-name` input) and keep a native POST.
- **CRM (HubSpot, Zoho, Pipedrive):** POST the `FormData` to their forms API from a small serverless function.
Keep the hidden `website` honeypot field and consider adding reCAPTCHA/hCaptcha.

## Images
Visuals are original SVG textile artwork (denim twill, knit rib, swatches, stitch, fabric rolls), consistent with the palette. For launch, replace with real photography (Unsplash/Pexels or your own factory/sample photos): swap the `.tx-*` background images in `styles.css` or the `.layer` elements, and add descriptive `alt`/`aria-label` text.

## Business claims requiring verification
Nothing below is asserted as fact on the site; wording is deliberately cautious. Confirm or edit before launch:
- Organic cotton knitwear and selvedge denim capability (shown as "subject to verified capability")
- Whether you own/operate factories or work through partner manufacturers (copy says "coordinate"; "manufacturing partners")
- Production capacities, minimum order quantities and lead times (none stated)
- Export markets and export coordination (stated as "where supported")
- Certifications and compliance standards (none claimed)
- Testing coordination with accredited labs
- In-line / final inspection stages and reporting described on the Quality page
- Wash and finishing options available (depends on partner)
- Contact email, phone, address, and response-time promise (placeholders only)
- Sourcing "one accountable contact" and "single point of ownership" statements

## Remaining recommendations
- Add real photography, a logo mark, and favicon / social share image (`og:image`).
- Add privacy policy and terms pages once the form collects data.
- Add analytics and conversion tracking on form submission.
