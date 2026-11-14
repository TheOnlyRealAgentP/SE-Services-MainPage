# Launch checklist

Do these once the new domain is live and the old domains are redirecting
(see the deployment guide, `DEPLOY.md`, kept locally). The NAP (name, address, phone) must match the
website **exactly**, everywhere:

> **Stewart Engineering Services**
> 16531 Shady Lane, Channelview, TX 77530
> (281) 862-9769
> https://stewartengineeringservices.com

## Before announcing it

- [ ] Fill in the TODOs in [TODO.md](TODO.md), at least the license numbers,
      the form endpoint and the regulatory "verify" items.
- [ ] Connect the contact form, send a test request, and confirm the email
      arrives at the right inbox.
- [ ] On a phone: tap the phone number, tap **Get a Quote**, submit the form,
      and open the menu.
- [ ] Spot-check old URLs, which should land on the matching new page:
      - `aerobicservice.com/maintenance`
      - `aerobicservice.com/faqs`
      - `se.services/platting`
      - `se.services/fireprotect`
      - `se.services/blog`
      - one old blog post, e.g. `se.services/blogs/the-role-of-fire-prevention-plans-in-reducing-property-damage`
- [ ] Send a test email to and from `info@aerobicservice.com` and
      `info@se.services`.

## Google Search Console

- [ ] Add and verify **stewartengineeringservices.com** as a *Domain*
      property. It uses a TXT record at Porkbun.
- [ ] Add and verify **aerobicservice.com** and **se.services** as well.
      They need to be verified properties for the next step.
- [ ] Submit `https://stewartengineeringservices.com/sitemap.xml` under
      **Sitemaps**.
- [ ] Once the 301 redirects are live, open each old property → **Settings →
      Change of address** → choose stewartengineeringservices.com → run the
      checks → **Submit**. Do this for both old domains.
- [ ] After about a week: **Pages** report for the new domain. Most pages
      should be indexed, and old URLs should show as "Page with redirect" on
      the old properties. Use **URL Inspection → Request indexing** on the
      home page and the maintenance page if they're slow.
- [ ] After a month, check **Performance** for which searches bring
      visitors, and compare against the old properties.

## Google Business Profile

- [ ] Search Google Maps for "Stewart Engineering", "Stewart Aerobic",
      "AIMS" and "Aerobic Installation and Maintenance" near Channelview. Claim
      every listing that's yours.
- [ ] If there are duplicates for the same address, keep one and ask Google
      to merge or remove the others (Business Profile → **Support** → "Request
      to remove or merge duplicate").
- [ ] Business name: **Stewart Engineering Services**. Use the name only, with
      no keywords added, or Google may suspend the listing.
- [ ] Primary category **Septic system service**; add **Civil engineer**
      (plus *Civil engineering company* if offered).
- [ ] Address, phone and hours exactly as on the website. Add the service
      area towns: Channelview, Baytown, Crosby, Highlands, Huffman, Mont
      Belvieu, Deer Park, La Porte, Pasadena.
- [ ] **Website:** `https://stewartengineeringservices.com`
- [ ] **Services:** add every service with a one-line description. Copy the
      summaries from `_data/services.yml`.
- [ ] **Photos:** logo, office or truck, crew at work, finished installs,
      and an engineering project. Add a few new ones every month.
- [ ] Get the **review link** (Business Profile → **Ask for reviews**). Put it
      in `_data/business.yml` as `google_review_link`, and the profile URL as
      `google_business`.

## Directory listings

Update name, address, phone and website so they match the NAP above exactly:

- [ ] Yelp (claim at biz.yelp.com)
- [ ] HomeAdvisor / Angi
- [ ] Facebook page (facebook.com/StewartAerobic): name, website link,
      address, hours. Consider renaming the page to match the business name.
- [ ] BBB
- [ ] Apple Maps (Apple Business Connect) and Bing Places. Both can import
      from Google Business Profile.
- [ ] TCEQ / county records, if they list a website or a different name.
- [ ] Email signatures, invoices, truck lettering and business cards: new
      website address.

## Review habit

- [ ] After **every maintenance visit and repair**, text the customer the
      Google review link. For example:

  > Thanks for having us out today. If we did a good job, a quick Google
  > review helps a small family business a lot: [review link]. Stewart
  > Engineering Services

- [ ] Reply to every review, good or bad, within a few days.
- [ ] Once there's a real rating, fill in `rating:` in `_data/business.yml`
      (value, count and the link to the reviews). The stars then appear in
      the trust strip, and in Google's structured data. Never type a rating
      you can't link to.
