// VĀNA WhatsApp funnel — the "Decide replies & lead" Code node.
// Kept as a separate file so it can be tested; build_workflow.py embeds it into the workflow JSON.
// Input: WhatsApp Cloud API webhook payloads. Output: items with kind = 'reply' (send via Graph API)
// or kind = 'lead' (upsert into the Leads sheet).

const CFG = {
  site: 'https://vanaspa.com',
  brochureUrl: 'https://vanaspa.com/assets/vana-treatment-menu.pdf',
  mapsUrl: 'https://share.google/J33BrEqedsUDC5wgM',
  instagram: 'https://www.instagram.com/vana_wellness_spa/',
  lat: 10.01981,
  lng: 76.35331,
  address: 'E Tower, 1st & 2nd Floor, Kollamkudimugal Road, Athani, Kakkanad, Kochi 682030',
  cooldownHours: 12,          // don't repeat the same automatic answer to one person within this window
  maxAgeSeconds: 600,         // never auto-reply to messages older than this (webhook retries, backlogs)
  openingMonthEnds: '2026-10-19T00:00:00+05:30',
};

// ── Helpers ────────────────────────────────────────────────────────────────
const nowMs = Date.now();
const ist = new Date(nowMs + 5.5 * 3600e3);               // IST clock via UTC getters
const istISO = ist.toISOString().replace('T', ' ').slice(0, 16);
const day = ist.getUTCDay();                               // 0 Sun … 6 Sat
const mins = ist.getUTCHours() * 60 + ist.getUTCMinutes();
const weekend = day === 0 || day === 5 || day === 6;       // Fri–Sun
const openMin = weekend ? 11 * 60 : 12 * 60;
const closeMin = weekend ? 21 * 60 + 30 : 21 * 60;
const isOpen = mins >= openMin && mins < closeMin;
const tomorrowWeekend = day === 4 || day === 5 || day === 6;     // Thu, Fri, Sat → Fri–Sun hours tomorrow
const opensText = mins >= closeMin
  ? (tomorrowWeekend ? 'at 11 AM tomorrow' : 'at 12 PM tomorrow')
  : (weekend ? 'at 11 AM today' : 'at 12 PM today');
const closedLine = isOpen ? '' : `\n\nWe're closed right now — we'll reply ${opensText}.`;
const openingMonth = nowMs < Date.parse(CFG.openingMonthEnds);

const text = (to, body) => ({ messaging_product: 'whatsapp', to, type: 'text', text: { body, preview_url: true } });

// ── Intent and interest detection ─────────────────────────────────────────
const INTENTS = [
  ['menu',     /\b(menu|price|prices|pricing|rate|rates|cost|charge|charges|tariff|brochure|list|services|treatments?|how much|ethra|ethrayanu|rate entha)\b/],
  ['location', /\b(location|locate|where|address|map|maps|direction|directions|route|parking|evide|evideya|sthalam|landmark)\b/],
  ['hours',    /\b(hours|timing|timings|open|opening|close|closing|till when|until when|working time)\b/],
  ['website',  /\b(website|site|web|link|instagram|insta)\b/],
  ['couples',  /\b(couple|couples|partner|wife|husband|anniversary|honeymoon|together|two of us)\b/],
  ['offers',   /\b(offer|offers|discount|membership|memberships|package|packages|prepaid|gift|voucher|founding|return14|afternoon|early|bring)\b/],
  ['female',   /\b(female|lady|ladies|woman|women) (therapist|staff|masseuse)|\bfemale therapist\b/],
  ['book',     /\b(book|booking|appointment|slot|slots|available|availability|reserve|reservation|today|tomorrow|tonight|this evening|walk ?in)\b|i'?d like to book/],
  ['human',    /\b(call me|talk to|speak to|human|manager|staff|person|complaint|problem|issue|refund|cancel|reschedule)\b/],
];
const INTERESTS = [
  ['deep tissue', /deep ?tissue/], ['swedish', /swedish/], ['balinese', /balinese/], ['sports', /sports?/],
  ['aromatherapy', /aroma/], ['four hands', /four ?hands?|4 ?hands?/], ['couples', /couple/],
  ['signature', /signature/], ['reflexology', /reflexology|foot/], ['head & scalp', /head|scalp/],
  ['neck, back & shoulders', /neck|back|shoulder/], ['facial', /facial/], ['manicure', /manicure/],
  ['pedicure', /pedicure/], ['scrub / wrap', /scrub|wrap/], ['de-tan', /de-?tan/], ['steam', /steam/],
  ['membership', /membership|monthly/], ['prepaid / gift', /prepaid|gift|voucher|bronze|silver|gold|platinum/],
];

// ── Reply builders ────────────────────────────────────────────────────────
const R = {
  welcome: (to, name) => ({
    messaging_product: 'whatsapp', to, type: 'interactive',
    interactive: {
      type: 'list',
      body: { text: `Welcome to VĀNA Wellness Spa${name ? ', ' + name.split(' ')[0] : ''} 🌿\nA boutique spa in Athani, Kakkanad — a few minutes from Infopark, open every day into the evening.\n\nTap below for what you need, or just type your question — our team replies personally.${closedLine}` },
      footer: { text: 'vanaspa.com' },
      action: {
        button: 'How can we help?',
        sections: [{
          title: 'VĀNA Wellness Spa',
          rows: [
            { id: 'menu', title: 'Menu & prices', description: 'Our treatment brochure (PDF)' },
            { id: 'book', title: 'Book a session', description: 'Tell us a day and time' },
            { id: 'location', title: 'Location & parking', description: 'E Tower, Athani, Kakkanad' },
            { id: 'couples', title: 'Couples suite', description: 'Private steam & shower for two' },
            { id: 'offers', title: 'Offers & memberships', description: openingMonth ? 'Opening Month offers until 18 Oct' : 'Memberships, prepaid & gift cards' },
            { id: 'hours', title: 'Opening hours', description: 'Open every day' },
            { id: 'website', title: 'Website & Instagram', description: 'See the space and the full menu' },
            { id: 'human', title: 'Talk to our team', description: 'We reply personally' },
          ],
        }],
      },
    },
  }),
  menu: (to) => [
    { messaging_product: 'whatsapp', to, type: 'document',
      document: { link: CFG.brochureUrl, filename: 'VANA-Treatment-Menu.pdf', caption: 'The VĀNA treatment menu. Every price is the full price.' } },
    text(to, `A few favourites:\n• Swedish Restore — 60 min ₹2,500 · 90 min ₹3,200\n• Deep Tissue Release — 60 min ₹2,800 · 90 min ₹3,500 (steam & shower included)\n• Couples Signature — 90 min ₹5,700 for two\n• Neck, Back & Shoulders — 30 min ₹1,500\n\nFull menu online: ${CFG.site}/#treatments\n\nWould you like to book? Send the treatment, day and time.`),
  ],
  location: (to) => [
    { messaging_product: 'whatsapp', to, type: 'location',
      location: { latitude: CFG.lat, longitude: CFG.lng, name: 'VĀNA Wellness Spa', address: CFG.address } },
    text(to, `We're at E Tower, 1st & 2nd Floor, Kollamkudimugal Road, Athani, Kakkanad — a few minutes from Infopark. Parking on site, lift to both floors.\n\nGoogle Maps: ${CFG.mapsUrl}`),
  ],
  hours: (to) => [text(to, `We're open every day:\nMonday – Thursday, 12 PM – 9 PM\nFriday – Sunday, 11 AM – 9:30 PM\n\nThe last session starts 90 minutes before closing.`)],
  website: (to) => [text(to, `Website: ${CFG.site}\nMenu & prices: ${CFG.site}/#treatments\nOffers & memberships: ${CFG.site}/offers/\nInstagram: ${CFG.instagram}`)],
  couples: (to) => [text(to, `Our couples suite has its own private steam and shower — it's the one room we hold back, so evenings and weekends go first.\n\nThe Couples Signature (scrub, massage and a private 15-minute steam, side by side) is ₹5,700 for 90 min or ₹6,500 for 120 min, for both of you.\n\nMore: ${CFG.site}/couples-spa-kakkanad/\n\nSend two or three times that work and we'll hold the best one.`)],
  offers: (to) => [text(to, (openingMonth
    ? `Opening Month offers, until 18 October — say the word when you book:\n• FOUNDING — first 100 guests: a year of priority evening slots, steam with every massage, and a monthly 60→90 upgrade\n• RETURN14 — come back within 14 days for a free Head & Scalp\n• BRING — bring a first-time friend: their steam is on us\n• AFTERNOON — weekdays 11 AM – 4 PM, free steam with any massage\n• EARLY — buy a prepaid tier and your first session goes 60→90\n\n`
    : '') + `Memberships from ₹2,000/month, prepaid tiers worth up to ₹71,500, and gift cards at face value.\n\nDetails: ${CFG.site}/offers/`)],
  book: (to) => [text(to, `Lovely — send us the treatment, the day and the time you'd like (and whether you'd prefer a female therapist). Our team will confirm your slot personally.${closedLine}`)],
  female: (to) => [text(to, `Of course — we'll book a female therapist for you. Every room is private with its own bath. Which treatment, day and time would you like?${closedLine}`)],
  human: (to) => [text(to, `Of course — someone from our team will reply here personally.${closedLine}`)],
};

// ── Main ──────────────────────────────────────────────────────────────────
const store = $getWorkflowStaticData('global');
store.leads = store.leads || {};
const out = [];

for (const item of $input.all()) {
  const j = item.json;
  const value = j.entry?.[0]?.changes?.[0]?.value ?? j.body?.entry?.[0]?.changes?.[0]?.value ?? j;
  const msg = value?.messages?.[0];
  if (!msg || !msg.from) continue;                        // delivery/read statuses, echoes, etc.

  const phoneId = value.metadata?.phone_number_id;
  const from = msg.from;
  const name = value.contacts?.[0]?.profile?.name || '';
  let body = '', tapped = '';
  if (msg.type === 'text') body = msg.text?.body || '';
  else if (msg.type === 'interactive') {
    const r = msg.interactive?.list_reply || msg.interactive?.button_reply;
    tapped = r?.id || ''; body = r?.title || '';
  } else if (msg.type === 'button') body = msg.button?.text || '';
  else body = `[${msg.type}]`;
  const t = body.toLowerCase();

  // Lead memory (per phone number)
  const isNew = !store.leads[from];
  const lead = store.leads[from] || { first: istISO, count: 0, sent: {}, interests: [], lastIn: 0 };
  const firstInWindow = nowMs - (lead.lastIn || 0) > CFG.cooldownHours * 3600e3;
  lead.count += 1;
  lead.lastIn = nowMs;

  // What do they want?
  let intents = [];
  if (tapped) intents = [tapped];
  else if (msg.type === 'text') intents = INTENTS.filter(([, re]) => re.test(t)).map(([k]) => k);
  if (intents.includes('female')) intents = intents.filter(i => i !== 'book');
  for (const [k, re] of INTERESTS) if (re.test(t) && !lead.interests.includes(k)) lead.interests.push(k);

  // Where did they come from?
  let source = '';
  if (isNew) {
    if (msg.referral) source = 'Ad: ' + (msg.referral.headline || msg.referral.source_url || msg.referral.source_type || 'click-to-WhatsApp');
    else if (/vāna/i.test(body)) source = 'Website';                 // the site's pre-filled messages spell VĀNA with the macron
    else source = 'WhatsApp (direct)';
  }

  // Which automatic replies?
  const fresh = nowMs / 1000 - Number(msg.timestamp || nowMs / 1000) <= CFG.maxAgeSeconds;
  const cooled = k => tapped || nowMs - (lead.sent[k] || 0) > CFG.cooldownHours * 3600e3;
  const replies = [];
  if (fresh) {
    for (const k of intents) {
      if (R[k] && k !== 'welcome' && cooled(k)) { replies.push(...R[k](from)); lead.sent[k] = nowMs; }
    }
    // Welcome list: first message in a while with no clear question, or a brand-new contact after their answer
    if ((!intents.length && firstInWindow) || (isNew && intents.length && !tapped)) {
      if (cooled('welcome')) { replies.push(R.welcome(from, name)); lead.sent.welcome = nowMs; }
    }
  }
  store.leads[from] = lead;

  // Blue ticks first, then replies in order
  if (replies.length) out.push({ json: { kind: 'reply', phone_number_id: phoneId, payload: { messaging_product: 'whatsapp', status: 'read', message_id: msg.id } } });
  for (const p of replies) out.push({ json: { kind: 'reply', phone_number_id: phoneId, payload: p } });

  // Lead row: only the columns we own; never overwrite a status the team has set
  const row = {
    kind: 'lead',
    phone: '+' + from,
    name,
    last_contact: istISO,
    messages: lead.count,
    interests: lead.interests.join(', '),
    last_intent: intents.join(', ') || (msg.type === 'text' ? 'other' : msg.type),
    last_message: body.slice(0, 300),
  };
  if (isNew) Object.assign(row, { status: 'New enquiry', source, first_contact: lead.first });
  if (intents.includes('book') || intents.includes('female')) row.last_booking_request = istISO;
  out.push({ json: row });
}

return out;
