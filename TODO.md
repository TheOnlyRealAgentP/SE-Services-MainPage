# TODO: missing facts, photos and checks

Nothing on the site was guessed; everything below is either missing or
needs checking.

**The markers are hidden on the live site** (`show_todos: false` in
`_config.yml`). Unfinished items are simply left out. For example, the
footer skips license numbers that are blank, and missing photos show a
navy blueprint panel. To see every yellow TODO marker while you work:

```bash
bundle exec jekyll serve --baseurl "" --config _config.yml,_config.todos.yml
```

Hidden FAQ answers that still need verifying (section 3) **do** show on
the live site as normal text, so check those first.

Most business facts go in **`_data/business.yml`**; once a value is set,
its marker disappears from every page.

## 1. Business facts (`_data/business.yml`)

- [ ] **Domain extension.** The site assumes `stewartengineeringservices.com`.
      Confirm, since it's used for canonical URLs, the sitemap and Google's
      structured data (`url:` in both `_config.yml` and `_data/business.yml`).
- [ ] **License numbers** (`licenses:`). These show in the footer of every
      page, in the trust strip near the top of most pages, and on /about:
  - [ ] TCEQ OSSF installer license #
  - [ ] TCEQ OSSF maintenance provider registration #
  - [ ] Texas Professional Engineer (PE) license #
  - [ ] TBPELS engineering firm registration # (format `F-12345`)
- [ ] **Owner** name and title (`owner:`), shown on /about.
- [ ] **Map pin coordinates** (`geo:`). Right-click the office pin in Google
      Maps and copy the two numbers. Used in Google's structured data.
- [ ] **Contact form endpoint** (`form:`). Create a free form at
      [Formspree](https://formspree.io) or [Web3Forms](https://web3forms.com)
      that emails the office, then paste the endpoint (and the Web3Forms
      access key if you use Web3Forms). Until then the form shows an error
      and asks people to call.
- [ ] **Google Business Profile URL** and **review link** (`social:`).
- [ ] **Rating.** Only once there's a real, linkable rating (`rating:`).

## 2. Page content

- [ ] **/about: founding story.** Who started the company, when, and how
      the septic side and the engineering side came together.
- [ ] **/about: owner bio.** Two or three sentences: background, licenses,
      what they handle personally. (Reviews mention "Mr. Stewart" and "Joe";
      the site doesn't name anyone until you confirm.)
- [ ] **/privacy:** name the form provider once the form is connected.
- [ ] **/maintenance:** does the office also file inspection reports for
      **Chambers County** customers (Mont Belvieu, east Baytown)?
- [ ] **/maintenance:** confirm the inspection checklist in the FAQ matches
      what technicians actually check.
- [ ] **/maintenance:** optional typical contract price or range.
- [ ] **/land-development** and **/platting:** are boundary surveys done
      in-house or by a surveyor you work with?
- [ ] **/wastewater:** scope of "water and sewer service planning". Does it
      include public water and sewer line design, lift stations, package
      plants?
- [ ] **/fireprotect:** scope. Sprinkler and alarm system design, or site
      fire protection plans (fire lanes, hydrants), or both?
- [ ] **/fireprotect:** which fire marshal offices you regularly submit to.

## 3. Regulatory statements to verify

These read correctly to the best of our knowledge but must be checked
against current rules before launch, because rules change and getting them
wrong on a licensed firm's website is a real problem.

- [ ] /maintenance and /faqs: aerobic systems need a maintenance contract on
      file with the county (TCEQ 30 TAC Chapter 285 and Harris County).
- [ ] /faqs: homeowner self-maintenance after training and certification,
      and which counties allow it.
- [ ] /faqs: chlorine tablets. Homeowner keeps the chlorinator stocked; only
      wastewater-rated tablets, not pool tablets.
- [ ] /installation: permitting authority for each county served (Harris,
      Chambers).
- [ ] /wastewater: when Texas OSSF rules require a design by a
      professional engineer.
- [ ] /drainageimp: Harris County / HCFCD detention requirements; SWQMP
      permit and renewal requirements; floodplain development rules.
- [ ] /platting: platting requirements in Harris County, city ETJs and MUDs.
- [ ] /fireprotect: "red tag" description vs. Harris County Fire Marshal's
      Office practice.
- [ ] /firecode: adopted fire code editions for Harris County and the cities
      served; Harris County FMO operational permit categories.

## 4. Photos

Only the business's own photos are used, never stock photos of people. Four
real job-site photos came from aerobicservice.com (septic installs). These
spots still need a real photo:

- [ ] Home page, engineering card: a recent engineering project (site plan,
      subdivision or commercial site)
- [ ] /about: the owner (head-and-shoulders, outdoors or at a job site)
- [ ] /land-development: a site plan or subdivision under construction
- [ ] /drainageimp: a detention pond, outfall or graded site
- [ ] /platting: a recorded plat or platting project (a photo of a plan sheet
      is fine)
- [ ] /fireprotect: a commercial building or fire protection plan set
- [ ] /firecode: a commercial building or code review project
- [ ] Nice to have: crew or truck photo, office exterior, more finished
      aerobic installs

See the README for how to add photos.

## 5. More reviews for the review carousel

The home and About pages rotate through every review in
`_data/testimonials.yml` (the format is explained at the top of that file).
Only three verified reviews are there today. As of November 2026, Google
shows about 15 reviews for "Stewart Engineering" at 16531 Shady Ln. Google
doesn't allow automated copying, so these have to be copied by hand:

- [ ] **Google:** open the Business Profile → Reviews. Copy the good ones word
      for word, with the reviewer's name as shown, the star rating and
      "Google" as the source. While you're there, reply to every review,
      especially the critical ones; future customers read the replies.
- [ ] **Facebook** (facebook.com/StewartAerobic → Reviews/Recommendations).
- [ ] **Yelp** and **HomeAdvisor/Angi:** any reviews beyond the two already used.
- [ ] Add the Google review link to `_data/business.yml`
      (`google_review_link`). A "Leave us a review on Google" link then
      appears under the carousel.

## 6. Optional

- [ ] **Logo source file.** The logo was rebuilt as a vector from the
      low-resolution image on se.services: the gear and compass redrawn,
      the lettering traced. If the original design file exists (AI, EPS,
      SVG or PDF), swap it into `assets/img/logo.svg` and `logo-reversed.svg`.
- [ ] **Testimonial town.** The Ibarra family review has no town listed. Add
      one only if it's known.
