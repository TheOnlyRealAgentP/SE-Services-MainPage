# TODO: missing facts, photos and checks

Everything here shows on the site as a yellow **TODO** marker until it's
dealt with. Nothing was guessed. Fill in what you know, delete the marker,
and run `python3 scripts/check_site.py` to see how many are left.

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

## 5. Optional

- [ ] **Logo source file.** The logo was rebuilt as a vector from the
      low-resolution image on se.services: the gear and compass redrawn,
      the lettering traced. If the original design file exists (AI, EPS,
      SVG or PDF), swap it into `assets/img/logo.svg` and `logo-reversed.svg`.
- [ ] **Testimonial town.** The Ibarra family review has no town listed. Add
      one only if it's known.
