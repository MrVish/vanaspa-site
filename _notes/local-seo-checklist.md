# VĀNA — local SEO checklist (off-site work)

This file lives in `_notes/` so GitHub Pages does not publish it. The website changes are done; everything
below happens in Google Business Profile (GBP), Search Console and directories.

## 1. Use the same business details everywhere

Copy these exactly into GBP, Justdial, Bing Places, Apple Business Connect, Facebook and Instagram:

```
VĀNA Wellness Spa
E Tower, 1st & 2nd Floor, Kollamkudimugal Road, Athani, Kakkanad, Kochi, Kerala 682030
+91 81296 62890
https://vanaspa.com
Mon–Thu 12:00 PM – 9:00 PM · Fri–Sun 11:00 AM – 9:30 PM
```

## 2. Google Business Profile

**Categories.** Primary: *Day spa*. Additional: *Spa* and *Massage spa*. Google may ask you to verify again
after a category change.

**Description** (under 750 characters):

> VĀNA Wellness Spa is a boutique wellness spa in Athani, Kakkanad, Kochi, minutes from Infopark and
> SmartCity. We offer Swedish, Balinese, aromatherapy, deep tissue and sports massage, couples spa
> experiences, four-hands massage, reflexology, head and shoulder therapies, facials, body scrubs and
> wraps, manicure and pedicure. VĀNA has private treatment rooms each with their own bath, a dedicated
> couples suite with steam and shower, and professionally trained therapists. Open seven days a week
> with evening appointments available.

**Services.** Add each service with its price and a one-line description. Use these names so they match
the website:

| Service name in GBP | Price |
|---|---|
| Swedish Massage (Swedish Restore) | ₹2,500 – 3,200 |
| Aromatherapy Massage (Aromatherapy Calm) | ₹2,600 – 3,200 |
| Balinese Massage (Balinese Harmony) | ₹2,700 – 3,500 |
| Deep Tissue Massage (Deep Tissue Release) | ₹2,800 – 3,500 |
| Sports Massage (Sports Recovery) | ₹3,000 – 3,500 |
| Four Hands Massage | ₹4,800 – 5,800 |
| Couples Massage (Couples Signature) | ₹5,700 – 6,500 |
| Signature Scrub, Massage & Steam | ₹3,800 |
| Foot Reflexology | ₹700 – 1,400 |
| Head & Scalp Massage | ₹1,000 |
| Neck, Back & Shoulder Massage | ₹1,500 – 1,800 |
| Steam & Shower | ₹500 |
| De-Tan | ₹1,200 |
| Facials | ₹2,300 – 2,500 |
| Body Scrub (Forest Scrub) | ₹2,200 |
| Body Wrap (Cocoon Wrap) | ₹2,200 |
| Manicure | ₹1,400 – 2,000 |
| Pedicure | ₹1,600 – 2,300 |

Link each service to its page where one exists, for example
`https://vanaspa.com/deep-tissue-massage-kakkanad/` or `https://vanaspa.com/couples-spa-kakkanad/`.

**Photos.** Upload real photos now that the spa is open: at least 3 exterior (signage, entrance from the
road), 3 interior (reception, corridor, lounge), 3 of treatment rooms (a single, the couples suite, the
steam), plus the team. Add a few every week rather than all at once. Keep the AI visualisations off GBP.

**Posts.** One useful Google post a week, e.g. the Opening Month offers (until 18 October), then
memberships, then the couples suite.

## 3. Reviews

Ask every guest, not just the happy ones, with the direct review link, a couple of hours after the session:

> Thank you for coming to VĀNA today. If you have a minute, even a short Google review about your
> experience would really help a new local business like ours: <review link>

- Never offer a discount or freebie in exchange for a review. Google does not allow it.
- Don't tell guests what words to use.
- Reply to every review personally and mention what they had, e.g.: "Thank you for visiting VĀNA. We're
  glad the Deep Tissue session helped with the shoulder tension. Hope to see you again soon."

## 4. Search Console (after this website update is live)

1. Open Search Console for `vanaspa.com`. The Google verification tag is already in `index.html`.
2. Go to **Sitemaps** and submit `https://vanaspa.com/sitemap.xml`.
3. Use **URL Inspection** on `https://vanaspa.com/` and choose **Request indexing**. Do the same for
   `/massage-kakkanad/`, `/deep-tissue-massage-kakkanad/` and `/couples-spa-kakkanad/`.
4. Check the homepage and one service page in Google's Rich Results Test
   (https://search.google.com/test/rich-results). They should show *Local business*, *FAQ* and *Breadcrumbs*.
5. Once a month, look at **Performance → Queries** to see which searches bring impressions, and build
   the next page from what you see.

## 5. Directories and mentions

Justdial, Bing Places, Apple Business Connect, Facebook page, and any Kochi wellness/lifestyle listings.
Use the details in section 1 every time.

For local mentions and links, try Kochi publications, Infopark/SmartCity company HR teams (for corporate
wellness), gyms and running clubs (for sports massage), and hotels nearby.

## 6. Website to-dos that need you

- **Real photos:** replace the images in `assets/img/` with real photographs. Keep the same file names and
  the pages update automatically. Then delete the "design visualisation" captions (in `index.html` and
  `_tools/build_pages.py`).
- **Opening Month band** hides itself on 19 October 2026. Delete it from `index.html` after that, and remove
  the Opening Month section from `offers` in `_tools/build_pages.py`.
- **Next pages to write:** "What happens during your first massage", "Sports vs deep tissue massage",
  "Couples spa in Kakkanad: what to expect". Add them to `PAGES` and `JOURNAL_POSTS` in the build script.
