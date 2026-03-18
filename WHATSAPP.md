# 💬 WHATSAPP.md — WhatsApp Integration Guide

> Brotherhood Omega Dynasty WhatsApp setup for the Dynasty OPS group

---

## Phone Number

**+44 7424 394382** — Primary Dynasty Command WhatsApp

Quick link: [wa.me/447424394382](https://wa.me/447424394382?text=COMMAND%20CENTER)

---

## Group: "DYNASTY OPS"

Create a group with all key members for coordinated operations:
- Commander: Patrick (DJ Sharpshooter)
- Add key team members
- Bot: OMEGA Dynasty Bot (via WhatsApp Business API)

---

## WhatsApp Business API Setup

### Option A — Official Business API

1. Apply at [business.whatsapp.com/products/business-platform](https://business.whatsapp.com/products/business-platform)
2. Get approved for a WhatsApp Business Account
3. Create a phone number in Meta Business Manager
4. Generate API token
5. Configure webhook URL: `https://brotherhoodomegadynasty.com/webhook/whatsapp`
6. Add to `.env`:
   ```env
   WHATSAPP_API_KEY=<your_api_key>
   WHATSAPP_PHONE_NUMBER_ID=<phone_number_id>
   WHATSAPP_WEBHOOK_SECRET=<your_webhook_secret>
   ```

### Option B — whatsapp-web.js (Development/Testing)

For development, the Hustle Bridge container (:3001) uses `whatsapp-web.js`:

```bash
docker compose logs -f hustle-bridge
# Scan the QR code shown with your phone
```

---

## Auto-Response Commands

Send these messages to the WhatsApp number for automated responses:

| Message | Response |
|---------|----------|
| `STATUS` | Full system status report |
| `PNL` | Today's profit/loss |
| `POSITIONS` | Open trading positions |
| `AGENTS` | All 4 agent statuses |
| `EVACUATE` | Emergency: close all positions |
| `RESUME` | Resume trading |
| `BITCOIN` | Bitcoin holdings summary |
| `LOANS` | Liquidium loans status |
| `HELP` | List all commands |
| `COMMAND CENTER` | Dashboard link |

---

## Daily Photo Update

The bot automatically sends a daily update at 08:00 UTC:

```
🔱 OMEGA DYNASTY — DAILY REPORT [DATE]

💰 Profit Today: £X.XX
📊 Total: £X,XXX.XX / £16,670 (XX%)
🎯 Trades: XXX | Win: XX%
🤖 Agents: 4/4 ACTIVE
🐳 Docker: 14/14 UP

🍽 M'Tanga Development Fund: £XXX.XX
Progress photo of M'Tanga attached

CHUKUA KONTROLI YOTE 🔱
```

---

## Webhook Handler

See [integrations/whatsapp/handler.js](integrations/whatsapp/handler.js) for the webhook implementation.

The Hustle Bridge container handles all WhatsApp communication:
```bash
docker compose logs -f hustle-bridge
```

---

## Security Notes

1. Never share the WhatsApp API token
2. Validate all incoming webhook signatures
3. Rate-limit responses to prevent abuse
4. Only process messages from approved numbers

---

*Brotherhood Omega Dynasty · WHATSAPP.md*
