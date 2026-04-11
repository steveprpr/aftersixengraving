# After Six Engraving — Website

Custom laser engraving business site for After Six Engraving in Fredericksburg, VA.
Dark theme, bold typography, gold accents. Every section funnels to a quote request.

## Files

```
aftersixengraving_site/
  index.html              -- Main page (hero, services, featured work, maps, how it works, testimonials, about, contact)
  gallery.html            -- Full design catalog with category filtering, 426+ designs
  style.css               -- All styles (dark theme, responsive, animations)
  README.md               -- This file
  assets/
    designs/              -- 442 SVG design files organized by category
      Autum/
      Bridal Bachelorette_svgs/
      Charcuterie_svgs/
      Coasters_svgs/
      Golf_svgs/
      Halloween/
      Maps/               -- Empty, ready for map SVGs
      Monograms_family_svgs/
      Wedding/
      cuttingboards_svgs/
      flask_svgs/
      inspirational quotes_svgs/
      sunshine/
      logo.svg
      Live Laugh Love.svg
    gallery_data.js       -- Auto-generated catalog (don't edit manually)
    images/
      products/           -- Processed product photos (800px + 1600px versions)
  tools/
    build_gallery.py      -- Regenerates gallery_data.js from assets/designs/
    process_images.py     -- Processes raw product photos into web-ready JPEGs
```

## Local Preview

Open `index.html` in any browser. No build step, no server required.

## Updating Your Site Content

### Adding new SVG designs

1. Drop SVG files into the appropriate `assets/designs/[Category]/` folder
2. Run `python tools/build_gallery.py` from the project root
3. Gallery page automatically updates — no other changes needed
4. Commit and push to GitHub — Netlify auto-deploys

### Adding new maps

1. Drop map SVGs into `assets/designs/Maps/`
2. Run `python tools/build_gallery.py`
3. The Maps section on the gallery will activate automatically once files are present
4. The Maps tab will show your designs instead of "Coming Soon"

### Adding new product photos

1. Drop photos into `C:\Users\steve\iCloudDrive\Laser\ASE Images\` (or update the source path in the script)
2. Run `python tools/process_images.py`
3. Processed images land in `assets/images/products/`
4. Update `index.html` image src paths as needed
5. Commit and push

## Push to GitHub

```bash
cd /path/to/aftersixengraving_site

git init
git add -A
git commit -m "feat: After Six Engraving site with real assets"

# Create a repo on GitHub (github.com/new), then:
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/aftersixengraving-site.git
git branch -M main
git push -u origin main
```

## Netlify + GitHub Auto-Deploy

1. Log in to [Netlify](https://app.netlify.com)
2. Click **"Add new site"** > **"Import an existing project"**
3. Connect your GitHub account and select the `aftersixengraving-site` repo
4. Build settings:
   - **Build command:** leave blank (no build needed)
   - **Publish directory:** `.` or `/`
5. Click **Deploy site**

Every push to `main` triggers an automatic redeploy.

### Netlify Forms Setup

The quote form uses `data-netlify="true"` which Netlify detects automatically. After first deploy:

1. Go to Netlify dashboard > **Forms** — you should see "quote-request"
2. Set up email notifications: **Site settings** > **Forms** > **Form notifications** > add email to `aftersixengraving@gmail.com`

### Disable Site Password (if previously enabled)

1. **Site settings** > **Access & security** > **Visitor access**
2. Remove the password or set to "Open"

## Cloudflare DNS Setup

To point `aftersixengraving.com` to Netlify:

1. Log in to [Cloudflare](https://dash.cloudflare.com), select `aftersixengraving.com`
2. Go to **DNS** > **Records**
3. Add/update a CNAME record:
   - **Type:** CNAME
   - **Name:** `@`
   - **Target:** `YOUR-NETLIFY-SUBDOMAIN.netlify.app`
   - **Proxy status:** DNS only (gray cloud) — Netlify needs direct DNS, not Cloudflare proxy
4. Add `www` CNAME:
   - **Type:** CNAME
   - **Name:** `www`
   - **Target:** same Netlify subdomain
   - **Proxy status:** DNS only (gray cloud)
5. In Netlify: **Site settings** > **Domain management** > **Add custom domain** > `aftersixengraving.com`
6. Netlify provisions SSL automatically (takes a few minutes)

**Important:** Cloudflare proxy (orange cloud) must be OFF. Use gray cloud / DNS-only mode so Netlify can issue its SSL certificate.

## Design System

| Element | Value |
|---------|-------|
| Background | `#1A1A1A` |
| Alt Background | `#2D2D2D` |
| Surface/Cards | `#2A2A2A` |
| Accent (Gold) | `#C4953A` |
| Text | `#FFFFFF` |
| Text Muted | `#E0DBD5` |
| Headings Font | DM Serif Display (Google Fonts) |
| Body Font | Inter (Google Fonts) |

## Editing Content

- **Phone/email:** Search for `(540) 300-2566` or `aftersixengraving@gmail.com` in both HTML files
- **Testimonials:** Find the `testimonials` section in `index.html` — replace with real Google reviews
- **Gallery:** Run `python tools/build_gallery.py` after adding/removing SVGs
- **Social links:** Find `aria-label="Facebook"` / `aria-label="Instagram"` in footer — replace `#` hrefs with real URLs

## Contact

- Phone: (540) 300-2566
- Email: aftersixengraving@gmail.com
- Location: Fredericksburg, VA
