# Stewart Engineering Services website

The website for **stewartengineeringservices.com**. It replaces the two old
sites, aerobicservice.com (septic and aerobic) and se.services (engineering).
It's a plain [Jekyll](https://jekyllrb.com) site that GitHub Pages builds and
hosts for free.

- Live preview (until the domain is connected): <https://theonlyrealagentp.github.io/SE-Services-MainPage/>
- Going live and forwarding the old domains: `DEPLOY.md` (kept locally, not committed to this public repo)
- After launch: [LAUNCH-CHECKLIST.md](LAUNCH-CHECKLIST.md)
- Missing facts and photos: [TODO.md](TODO.md)

## Change the business details

Phone, email, address, hours, towns served, license numbers, the owner's
name, the contact-form endpoint and social links all live in **one file**:

```
_data/business.yml
```

Edit a value there and it updates the header, footer, contact page,
service-area page and the structured data Google reads, on every page. A
value left as `""` shows on the site as a yellow **TODO** marker until you
fill it in.

Other data files:

| File | What it holds |
| --- | --- |
| `_data/services.yml` | Every service: name, URL, one-line summary, related services. Drives the menus, the /services page and the form's service dropdown labels. |
| `_data/testimonials.yml` | Real customer reviews, word for word. Only add reviews a customer actually wrote. |
| `_data/images.yml` | Photo sizes and alt text (descriptions for screen readers and Google). |

You can edit any of these directly on GitHub (open the file → pencil icon →
**Commit changes**). The site rebuilds in about a minute.

## Edit page text

| Page | File |
| --- | --- |
| Home | `index.html` |
| Service pages | `installation.md`, `maintenance.md`, `services-repairs.md`, `land-development.md`, `drainageimp.md`, `wastewater.md`, `fireprotect.md`, `platting.md`, `firecode.md` |
| Engineering overview | `engineering/index.html` |
| All services | `services.html` |
| Service area (one paragraph per town) | `service-area.html` |
| About, Contact, FAQ | `about.html`, `contact.html`, `faqs.html` |
| Privacy, Terms, 404 | `privacy.md`, `terms.md`, `404.html` |

Service pages are mostly **front matter**, the block between the `---`
lines at the top. It holds the H1, intro, "Who it's for", "What's
included", the process steps, the FAQ and which testimonial to show. The
shared template in `_layouts/service.html` turns that into the page.

Each page also has a `title` (the browser tab and Google headline; keep it
to 29 characters or fewer, because " | Stewart Engineering Services" is added
automatically) and a `description` (the Google snippet; at most 155
characters).

**Don't change `permalink:` lines.** They match the URLs of the old sites,
which keeps existing Google rankings and links working.

## Add a new page

1. Copy a similar page, for example `platting.md` for a new engineering
   service.
2. Change `permalink`, `title`, `description`, `h1` and the content.
3. For a new service, add an entry to `_data/services.yml` with the same
   `id` as the page's `service_id`. It then shows up in the menu, footer
   and /services automatically.
4. Run the checks below.

## Add or replace photos

Photos live in `assets/img/` as `name-480.webp`, `name-480.jpg`,
`name-800.webp`, `name-800.jpg` and so on. To add one:

```bash
# from the repo root, with ImageMagick installed
for w in 480 800 1200; do
  magick original.jpg -auto-orient -strip -resize "${w}x>" -quality 62 assets/img/new-photo-$w.jpg
  magick original.jpg -auto-orient -strip -resize "${w}x>" -quality 52 assets/img/new-photo-$w.webp
done
```

Then add `new-photo` to `_data/images.yml` with its widths, its size and a
real description as `alt`. Use it with
`{% include picture.html name="new-photo" %}`, or on a
service page with `photo: new-photo` in the front matter.

To replace a grey "TODO: real photo" placeholder on a service page, delete
its `placeholder:` line and add `photo: your-photo-name`.

## Run it locally

You need Ruby 3.1–3.3 with development headers. On Fedora that's
`sudo dnf install ruby-devel gcc make`; on macOS, use Homebrew Ruby. Then:

```bash
bundle config set --local path vendor/bundle   # once
bundle install                                 # once
bundle exec jekyll serve --baseurl ""
```

Open <http://localhost:4000>. Pages rebuild when you save. (Ruby 4.0 can't
build the `github-pages` gem yet; use Ruby 3.3.)

## Check before you push

```bash
bundle exec jekyll build --baseurl ""
python3 scripts/check_site.py
```

The checker fails if any internal link is broken, a `href="#"` slipped in, a
page is missing a title, description or H1 (or has two H1s), a title or
description is too long or duplicated, structured data is invalid JSON, or an
image has no alt text. It also counts the TODO markers left on the site.

## Deploy

Push to `main`. GitHub Pages rebuilds and publishes automatically, usually
within a minute. Domain setup is in the local `DEPLOY.md`, which is not committed.

## How it's built

- Jekyll 3.10 via the `github-pages` gem, with only two plugins:
  `jekyll-seo-tag` (titles, descriptions, canonical and Open Graph tags) and
  `jekyll-sitemap` (`/sitemap.xml`).
- Hand-written CSS in `assets/css/main.css` with design tokens at the top
  (colors, type sizes, an 8px spacing scale). No framework.
- About 100 lines of JavaScript in `assets/js/main.js`: the mobile menu and
  the contact form. The site works without it.
- No trackers or analytics, and no external fonts.
- Logo: `assets/img/logo.svg` (and `logo-reversed.svg` for dark
  backgrounds), rebuilt as a vector from the original Stewart Engineering
  logo.
