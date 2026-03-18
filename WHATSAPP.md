# OMEGA-ULTIMATE-FUSION-V∞ — WhatsApp Integration Guide

> Brotherhood Omega Dynasty · WhatsApp command interface via +44 7424 394382

---

## Overview

WhatsApp integration allows Brotherhood members to monitor and control the OMEGA fleet via SMS-style messages. Commands are received via a webhook from Twilio or Meta Cloud API and processed by the `integrations/whatsapp/webhook.py` server.

---

## Setup — Option A: Twilio (Recommended)

### 1. Twilio WhatsApp Sandbox

```
1. Sign up at twilio.com
2. Navigate to Messaging → Try WhatsApp
3. Send "join <code>" to +1 415 523 8886
4. Note your Account SID and Auth Token
```

### 2. Configure Webhook URL

In Twilio console → WhatsApp sandbox settings:
```
Webhook URL: https://brotherhoodomegadynasty.com/webhook/whatsapp
HTTP Method: POST
```

### 3. Environment Variables

```env
WEBHOOK_SECRET=<your-twilio-auth-token>
WHATSAPP_WEBHOOK_PORT=9001
```

### 4. Start Server

```bash
docker compose up -d webhook-server
# OR
python -m integrations.whatsapp.webhook
```

---

## Setup — Option B: Meta Cloud API

### 1. Meta App Setup

```
1. Create app at developers.facebook.com
2. Add WhatsApp product
3. Get Phone Number ID and Access Token
4. Configure webhook URL
```

### 2. Webhook Verification

The server handles Meta's GET verification challenge automatically:
```
Verify Token: <your WEBHOOK_SECRET>
Callback URL: https://brotherhoodomegadynasty.com/webhook/whatsapp
```

---

## Commands

Send these messages to `+44 7424 394382`:

| Message | Response |
|---------|----------|
| `STATUS` | Fleet status (AUM, PnL, circuit breaker) |
| `PNL` | PnL breakdown per agent |
| `HALT` | Emergency halt (all trading stops) |
| `RESUME` | Resume trading after halt |
| `HELP` | Command list |

> Commands are **case-insensitive** — `status`, `STATUS`, `Status` all work.

---

## Example Conversation

```
Patrick: STATUS

OMEGA Bot: 🔱 OMEGA Status
           AUM: $3,847.23
           PnL: +$277.23
           CB: OK
           CHUKUA KONTROLI YOTE

Patrick: PNL

OMEGA Bot: 📊 PnL Report:
           DJ: +$82.10
           HASHIM: +$94.50
           BOSSMAN: +$65.30
           PATRICK: +$35.33

Patrick: HALT

OMEGA Bot: 🚨 EMERGENCY HALT triggered.
           All positions closing.
           Use RESUME when safe.
```

---

## Security

- Signature verification via HMAC-SHA256 (Twilio) or `X-Hub-Signature-256` (Meta)
- HALT command logs to database with timestamp and sender number
- No private keys transmitted via WhatsApp
- Rate limiting: max 10 req/s via Nginx

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Webhook not receiving | Check `docker logs omega-webhook` |
| Verification failed | Confirm `WEBHOOK_SECRET` matches Twilio/Meta config |
| Commands not working | Check fleet API is running: `curl localhost:8000/health` |
| No response | Verify webhook URL is publicly accessible |

---

*CHUKUA KONTROLI YOTE — Brotherhood Omega Dynasty*
