// Cloudflare Pages Function: POST /api/lead
// Sends contact-form leads by email through Resend.
// Required environment variables (Cloudflare Pages > Settings > Variables):
//   RESEND_API_KEY  - Resend API key (secret)
//   LEAD_TO_EMAIL   - inbox that receives leads
//   LEAD_FROM_EMAIL - verified sender, e.g. "DryBeacon Leads <leads@drybeacon.com>"

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });

const clean = (v, max) => String(v || '').replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, max);

export async function onRequestPost({ request, env }) {
  let data;
  try {
    data = await request.json();
  } catch {
    return json({ error: 'Invalid request.' }, 400);
  }
  if (data.company_site) return json({ ok: true }); // honeypot filled: silently drop

  const name = clean(data.name, 80);
  const phone = clean(data.phone, 30);
  const zip = clean(data.zip, 10);
  const message = clean(data.message, 2000);
  const page = clean(data.page, 200);
  const consent = data.consent === 'yes' || data.consent === 'on';

  if (!name || !/^[0-9+().\-\s]{10,20}$/.test(phone) || !/^\d{5}$/.test(zip)) {
    return json({ error: 'Please enter your name, a valid phone number and a 5-digit ZIP code.' }, 422);
  }
  if (!consent) return json({ error: 'Please tick the consent box so we can contact you.' }, 422);
  if (!env.RESEND_API_KEY || !env.LEAD_TO_EMAIL || !env.LEAD_FROM_EMAIL) {
    return json({ error: 'The form is not set up yet. Please call instead.' }, 503);
  }

  const submitted = new Date().toISOString();
  const text = [
    `New water damage request (${submitted})`,
    `Name: ${name}`,
    `Phone: ${phone}`,
    `ZIP: ${zip}`,
    `Page: ${page}`,
    `Consent to contact: yes (${submitted})`,
    '',
    message || '(no message)',
  ].join('\n');

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.LEAD_FROM_EMAIL,
      to: [env.LEAD_TO_EMAIL],
      subject: `Water damage request - ZIP ${zip}`,
      text,
    }),
  });
  if (!res.ok) return json({ error: 'Could not send right now. Please call instead.' }, 502);
  return json({ ok: true });
}

export const onRequest = () => json({ error: 'Method not allowed.' }, 405);
