# After Six Engraving — Website v3

Custom laser engraving business site for After Six Engraving in Fredericksburg, VA.  
Dark theme, bold typography, gold accents. Every section funnels to a quote request.

## Files

```
aftersixengraving_site/
  index.html      -- Main page (hero, services, gallery preview, how it works, testimonials, about, contact form)
  gallery.html    -- Full design catalog with category filters, lightbox, and SVG designs
  style.css       -- All styles (dark theme, responsive, animations)
  README.md       -- This file
  images/         -- Create this folder and add your product photos here
```

## Local Preview

Open `index.html` in any browser. No build step, no server required.

## Push to GitHub

```bash
cd /path/to/aftersixengraving_site

git init
git add -A
git commit -m "feat: After Six Engraving site modernization v3"

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
   - **Proxy status:** DNS only (gray cloud) — **Netlify needs direct DNS, not Cloudflare proxy**
4. Add `www` CNAME:
   - **Type:** CNAME
   - **Name:** `www`
   - **Target:** same Netlify subdomain
   - **Proxy status:** DNS only (gray cloud)
5. In Netlify: **Site settings** > **Domain management** > **Add custom domain** > `aftersixengraving.com`
6. Netlify provisions SSL automatically (takes a few minutes)

**Important:** Cloudflare proxy (orange cloud) must be OFF. Use gray cloud / DNS-only mode so Netlify can issue its SSL certificate.

## How to Update Photos

The site uses:
- **SVG designs** from `strong-zuccutto-ecc087.netlify.app` (your actual design catalog) for the gallery
- **Placeholder photos** from Unsplash for hero, services, and about sections

### Replace placeholder photos with your own:

1. Take photos of your best work (at least 1200px wide, JPG or WebP)
2. Create an `images/` folder in this directory
3. In `index.html`, find HTML comments that say `<!-- STEVE: Replace with... -->` and swap the Unsplash URLs:

Change this:
```html
<img src="https://images.unsplash.com/photo-XXXXX?w=800&q=80" alt="...">
```

To this:
```html
<img src="images/my-cutting-board.jpg" alt="Custom engraved cutting board by After Six Engraving">
```

4. Commit and push — Netlify auto-deploys

### Hero background:

In `index.html`, find `.hero__bg` and replace the `background-image` URL:
```html
<div class="hero__bg" style="background-image: url('images/hero-photo.jpg');">
```

Use your most impressive wide product photo. The dark overlay keeps text readable over any image.

### Image tips:
- Resize to ~800-1200px wide (keeps the site fast)
- Use `.jpg` for photos, `.png` for logos with transparency
- Always include descriptive `alt` text for SEO

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
- **Gallery items:** Each card in `gallery.html` has title, description, and category in data attributes
- **Social links:** Find `aria-label="Facebook"` / `aria-label="Instagram"` in footer — replace `#` hrefs with real URLs
- **Categories:** Filter buttons and gallery items use matching `data-filter` / `data-category` values

## Contact

- Phone: (540) 300-2566
- Email: aftersixengraving@gmail.com
- Location: Fredericksburg, VA
