DEL INTERNATIONAL HOSPITAL — WEBSITE FILES
==========================================

UPDATED 22 November 2026 (early hours)
----------------------------------------
- Preview countdown timer (user, 2026-11-22): a dark bar at the
  very top of the page, above the Open 24/7 bar — "LIVE PREVIEW
  EXPIRES IN 07 DAYS : 00 HRS : 00 MIN : 00 SEC" with orange
  numbers and "Temporary preview — taken offline when the timer
  reaches zero." It counts down live to Monday 30 November 2026
  at 23:59. On Monday 23 November (when the link is sent) it
  reads 07 DAYS all day. It reads 08 DAYS on Sunday, which is
  correct — it ticks to 07 on Monday. Change PREVIEW_EXPIRY in
  build-del-demo.py to move the date.
- Transparent header on scroll (user, 2026-11-22): at the top
  the header is solid as before, but once you start scrolling
  its background fades to see-through (soft white with a blur)
  so the page shows through and it stops feeling like a big
  block. The logo, the Home / Services / About us / Contact
  links and the Book appointment button all stay visible and
  clickable. The timer bar above stays solid and pinned, and
  the Open 24/7 bar scrolls away. (Checked in the page itself:
  the fade rule and the scroll switch are in place. A live
  scrolled screenshot could not be taken here — the headless
  browser does not scroll — so please scroll it yourself to
  see the header go see-through.)

WHAT IS IN THIS FOLDER
----------------------
index.html
    The whole website in ONE file. All the photos are already inside it,
    so this file alone is enough to publish the site.

images/
    The original photos used on the site, kept separate so you can
    swap or reuse them:
    - del-building-real.jpg ..... the real Del building (hero photo)
    - del-building-upscale.jpg .. the bright AI building photo (hero)
    - doctor-consultation.jpg ... doctor talking to a patient (hero)
    - reception-real.jpg ........ real Del reception (gallery)
    - team-real.jpg ............. real Del staff group (gallery + About)
    - waiting-real.jpg .......... real Del waiting area (gallery)
    - billboard-real.jpg ........ real Del roadside sign (gallery)
    - maternity.jpg ............. maternity ward photo (gallery)
    - services/ ................. the photos for each service (42 files)

HOW TO PUBLISH IT (EASIEST WAY)
--------------------------------
Option 1 — Netlify Drop (free, no account needed, 1 minute)
    1. Go to https://app.netlify.com/drop in your browser.
    2. Drag this whole folder onto the page.
    3. Netlify gives you a live link like
       https://del-international-hospital.netlify.app
       Share that link with Del.

Option 2 — GitHub Pages (free)
    1. Create a free GitHub account and a new repository.
    2. Upload index.html (and the images folder) to it.
    3. In Settings > Pages, turn on GitHub Pages.
    4. You get a link like https://yourname.github.io/del-hospital/

Option 3 — Any web hosting
    Upload index.html to the hosting's main folder (usually
    called public_html or www). That is all it needs.

BEFORE YOU SHOW IT TO DEL
-------------------------
These are SAMPLES and placeholders — replace them first:
- The 3 patient reviews (Ama S., Kwame & Akosua, Efua M.) are
  sample words I wrote. Use Del's real patient words.
- The mission and vision wording is short text I wrote from
  their reference. Del can change the words.
- Phone numbers: the site says 030 254 3255 / 030 254 3256,
  but Del's own roadside sign shows 0303 301353 / 0501 568322.
  Confirm which numbers are correct.
- Email: the site says info@delinternationalhospital.com,
  but listings disagree. Confirm the real email.
- WhatsApp: the site assumes 030 254 3256. Confirm it.
- Most service photos are stock photos of Black/Ghanaian
  people as stand-ins. Swap in Del's real photos when they
  send them — just replace the file with the same name and
  rebuild, or send the photos to Muse.
- Their building sign lists "Eye Care" — ask Del if they
  still offer it. It is not on the site right now.
