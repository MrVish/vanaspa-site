# VĀNA — WhatsApp auto-reply & lead funnel (n8n)

This folder starts with `_`, so GitHub Pages does not publish it.

| File | What it is |
|---|---|
| `vana-whatsapp-funnel.json` | The workflow. Import it into n8n. |
| `leads-sheet-template.csv` | Header row for the Google Sheet the leads go into. |
| `funnel-logic.js` | The brain of the workflow: what to reply and what to record. |
| `build_workflow.py` | Rebuilds the JSON after you edit `funnel-logic.js`. |

## What it does

```
Guest messages +91 81296 62890
        │
        ▼
 WhatsApp Trigger (n8n) ──► Decide replies & lead ──┬──► Send WhatsApp reply(ies)   (Meta Graph API)
                                                    └──► Save lead to sheet          (Google Sheets)
```

**Automatic replies:**

| Guest writes (English or common Manglish) | VĀNA replies with |
|---|---|
| *hi / hello*, or anything as their first message in 12 h | Welcome message plus a tap-able menu: Menu & prices · Book · Location · Couples · Offers · Hours · Website · Talk to our team |
| *price, rate, menu, brochure, ethra…* | The treatment brochure (PDF), then a few favourite prices and the online menu link |
| *location, address, where, parking, evide…* | A map pin, then the address, parking note and Google Maps link |
| *hours, timing, open, close…* | Opening hours |
| *website, instagram, link…* | Website, menu, offers and Instagram links |
| *couple, anniversary, partner…* | The couples suite and its prices |
| *offer, membership, gift, prepaid…* | Opening Month offers (until 18 Oct, then hidden automatically), memberships, gift cards |
| *book, appointment, slot, today, tomorrow…* | "Send the treatment, day and time — our team will confirm personally" |
| *female therapist…* | Confirms a female therapist can be arranged, and asks for treatment, day and time |
| *talk to / manager / cancel / reschedule…* | "Someone from our team will reply here personally" |

**Guardrails:**
- **No repeats:** the same automatic answer is never sent to one person twice within 12 hours. Tapping a menu option always gets an answer.
- **Stays out of the way:** mid-conversation messages the bot doesn't recognise get no automatic reply, so your team handles those.
- **After hours:** messages outside opening hours get "we're closed right now, we'll reply at 12 PM / 11 AM".
- **No stale replies:** messages older than 10 minutes (from outages or retries) are logged but not answered.
- **Nobody is missed:** every message is recorded, whether or not it got a reply.

**Lead sheet:** one row per phone number, updated on every message.

| Column | Filled by | Notes |
|---|---|---|
| phone, name | Bot | |
| first_contact, last_contact, messages | Bot | |
| source | Bot | *Website* (the site's pre-filled messages), *Ad: …* (click-to-WhatsApp ads) or *WhatsApp (direct)* |
| interests | Bot | Treatments they mentioned: deep tissue, couples, facial… |
| last_intent, last_message, last_booking_request | Bot | |
| status | Bot, then team | Set to *New enquiry* once; after that the team changes it (Booked, Visited, Member…) |
| notes | Team | The bot never writes here |

## One-time setup

### 1. Put your number on the WhatsApp Business Platform

The WhatsApp Business *app* can't be automated. The *Platform* (Cloud API) can, and Meta lets one number be on both at once. This is called **coexistence**: your team keeps chatting from the phone app while n8n answers automatically.

1. Go to **business.facebook.com** and make sure *Vana Serene LLP* has a Meta Business portfolio. Business verification raises your messaging limits.
2. Go to **developers.facebook.com**, then **My Apps → Create app → Business**, and add the **WhatsApp** product.
3. In **WhatsApp → API Setup**, add your existing number +91 81296 62890. When asked, choose to connect your **existing WhatsApp Business app** number (coexistence), and follow Meta's steps in the app to scan the QR code. Meta's exact requirements change, so follow what the screen asks.
4. Note down the **Phone number ID** and the **App ID / App Secret** (App settings → Basic).
5. In **Business settings → Users → System users**, create a system user and give it the app and the WhatsApp account. Generate a **permanent token** with `whatsapp_business_messaging` and `whatsapp_business_management`.

**Cost:** replying to a guest within 24 hours of their message is free under Meta's current pricing. Messages *you* start later, such as follow-ups and reminders, must use Meta-approved templates and are charged per message. Check Meta's pricing page when you set up.

### 2. Make the Leads sheet
1. Create a Google Sheet and name the first tab **Leads**.
2. Paste the header row from `leads-sheet-template.csv` into row 1.
3. Keep the sheet private to the team, because it holds guests' phone numbers.

### 3. Import into n8n
1. In n8n, go to **Workflows → Import from file** and choose `vana-whatsapp-funnel.json`.
2. **WhatsApp Trigger:** create a *WhatsApp OAuth* credential with Client ID = App ID and Client Secret = App Secret.
3. **Send WhatsApp reply:** create a *Header Auth* credential with Name `Authorization` and Value `Bearer <permanent token>`.
4. **Save lead to sheet:** connect Google, then paste your Leads sheet URL into *Document*.
5. **Brochure:** the replies link to `https://vanaspa.com/assets/vana-treatment-menu.pdf`, so the website update with the PDF must be live first. To send a different file, change `brochureUrl` at the top of the *Decide replies & lead* node.

### 4. Test, then switch on
1. Click **Test workflow** on the *Test: sample message* node. A row for "Test Guest" should appear in the sheet. The replies will fail for this fake number; that's expected. Delete the test row afterwards.
2. **Activate** the workflow.
3. From another phone, message +91 81296 62890 "hi", then "price", then "location". Check the replies and the sheet.
4. In the **WhatsApp Business app**, turn off the old *Greeting message*, or guests will get two welcomes. Keep the *Away message* off too, because the bot handles after-hours. Keep all your quick replies; the team still uses them.

## Changing replies

The simplest way is to edit the text inside the *Decide replies & lead* node in n8n. Prices are near the `R = {` section, and keywords in `INTENTS`.

To keep this repo in sync, edit `funnel-logic.js`, run `python3 _n8n/build_workflow.py`, and re-import.

**When prices, hours or offers change, update the replies too.** They're written out in the node.

## What's next

- **Staff alert:** a message to the manager (email or Telegram) when someone asks to book outside hours.
- **Follow-up templates:** get Meta-approved templates for the evening follow-up and review request, the 14-day return nudge and the monthly offers broadcast, then send them from n8n based on the sheet's *status* column.
- **Click-to-WhatsApp ads:** on Instagram and Facebook these land straight in this funnel, and the sheet records which ad each lead came from.
