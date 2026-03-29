# ✈️ TELEGRAM-BOT.md — Telegram Bot Setup Guide

> Complete setup for @OmegaDynastyBot — your 24/7 Dynasty Command Bot

---

## Step 1 — Create Bot via @BotFather

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow prompts:
   - Bot name: `Omega Dynasty Bot`
   - Username: `OmegaDynastyBot`
4. Copy the bot token: `1234567890:ABCdef...`
5. Add token to `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=1234567890:ABCdef...
   ```

---

## Step 2 — Get Your Chat ID

1. Start a conversation with your bot
2. Send `/start`
3. Visit: `https://api.telegram.org/bot<TOKEN>/getUpdates`
4. Find `chat.id` in the response
5. Add to `.env`:
   ```env
   TELEGRAM_CHAT_ID=123456789
   ```

---

## Step 3 — Configure Webhook

```bash
# Set webhook to your server
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://brotherhoodomegadynasty.com/webhook/telegram"}'

# Verify webhook is set
curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
```

---

## Step 4 — Deploy Bot Container

The Telegram bot runs in the `telegram` container on port `:3013`.

```bash
docker compose up -d telegram
docker compose logs -f telegram
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message + status overview |
| `/status` | Full system status (all 14 containers) |
| `/pnl` | Today's P&L report |
| `/positions` | All open positions |
| `/evacuate` | Emergency — close all positions |
| `/resume` | Resume trading after pause |
| `/pause` | Pause new trades |
| `/agents` | Status of all 4 agents |
| `/bitcoin` | Bitcoin holdings summary |
| `/lq` | Liquidium loans status |
| `/help` | Show all commands |

---

## Auto-Alerts Configuration

The bot automatically sends alerts for:

| Event | Trigger | Message |
|-------|---------|---------|
| LQ-004 expiry | 7d, 3d, 2d, 1d, 12h, 6h, 1h before | ⚠️ LQ-004 expires in X — ACTION REQUIRED |
| Daily summary | 08:00 UTC every day | 📊 Daily P&L report |
| YOLO mode engaged | When activated | ⚡ YOLO 10X MODE ACTIVATED |
| Container down | Any container stops | 🚨 CONTAINER DOWN: [name] |
| Profit milestone | Every £500 | 💰 Milestone: £X earned |
| Circuit breaker | Triggered | 🛑 CIRCUIT BREAKER ENGAGED |

---

## Daily Summary (08:00 UTC)

The bot sends a formatted daily report:
```
🔱 OMEGA DAILY REPORT
📅 Date: [DATE]
💰 Today's Profit: £X.XX
📈 Trades: XXX
🎯 Win Rate: XX.X%
💎 Total Profit: £X,XXX.XX
🎯 Target Progress: XX.X%
⚡ All 4 Agents: ACTIVE
🐳 Containers: 14/14 UP
```

---

## Webhook Handler Code Reference

See [integrations/telegram/bot.js](integrations/telegram/bot.js) for the full implementation.

---

*Brotherhood Omega Dynasty · TELEGRAM-BOT.md*
