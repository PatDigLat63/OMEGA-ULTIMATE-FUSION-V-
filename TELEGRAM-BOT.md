# OMEGA-ULTIMATE-FUSION-V∞ — Telegram Bot Guide

> Brotherhood Omega Dynasty · Kill-switch and command interface

---

## Setup

### 1. Create Bot via BotFather

```
1. Open Telegram → search @BotFather
2. Send /newbot
3. Name: OMEGA Dynasty Bot
4. Username: omega_dynasty_bot (or similar)
5. Copy the API token
```

### 2. Get Your Chat ID

```
1. Send any message to your new bot
2. Open: https://api.telegram.org/bot<TOKEN>/getUpdates
3. Find "chat":{"id": <YOUR_CHAT_ID>}
```

### 3. Configure Environment

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
TELEGRAM_CHAT_ID=987654321
```

### 4. Start Bot

```bash
docker compose up -d telegram-bot
# OR
python -m integrations.telegram.bot
```

---

## Commands

| Command | Response |
|---------|----------|
| `/start` | Welcome message + system overview |
| `/help` | Full command list |
| `/status` | Live fleet status (all 4 agents) |
| `/pnl` | PnL breakdown per agent |
| `/positions` | Open positions summary |
| `/evacuate` | **Emergency halt** — stops all trading |
| `/resume` | Resume trading after halt |
| `/cb` | Circuit breaker status + drawdown % |

---

## Example Responses

### /status
```
🔱 Fleet Status
AUM: $3,847.23
PnL: +$277.23
Cycles: 1,247
CB: ✅ OK (3.2% drawdown)

Agents:
✅ DJ | +$82.10 | WR: 67%
✅ HASHIM | +$94.50 | WR: 71%
✅ BOSSMAN | +$65.30 | WR: 58%
✅ PATRICK | +$35.33 | WR: 63%
```

### /pnl
```
📊 PnL Report

DJ: +$82.10
HASHIM: +$94.50
BOSSMAN: +$65.30
PATRICK: +$35.33

Fleet total: +$277.23
```

### /evacuate
```
🚨🚨🚨 EMERGENCY EVACUATION PROTOCOL ACTIVATED

All positions closing...
All agents entering safe mode...
Emergency wallets on standby.

Wallet 1: 6q7wbjuPnSE9pBPQ838YfcSQDyMahmXrx3RYxPSYpde1
Wallet 2: EcxNACs4n6rekZR3JCYDBjaVJbyQfn9StYYNRUsHu3xy

Use /resume once positions are confirmed closed.
```

---

## Security

- Only `TELEGRAM_CHAT_ID` can issue commands
- All other chat IDs receive "Unauthorised" response
- No private keys ever transmitted via Telegram
- `/evacuate` halts trading but does NOT auto-close positions (manual step required)
- Bot runs in isolated Docker container with no write access to wallets

---

## Alerts

The bot also receives **automatic alerts** from the fleet:
- Circuit breaker trips
- Agent errors (3+ consecutive failures)
- Backup failures
- Server resource warnings (CPU/RAM >90%)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot not responding | Check `docker logs omega-telegram-bot` |
| "Unauthorised" error | Verify `TELEGRAM_CHAT_ID` matches your chat |
| `/status` shows unavailable | Fleet API down — check `omega-orchestrator` container |
| Slow responses | Check Redis connection |

---

*CHUKUA KONTROLI YOTE — Brotherhood Omega Dynasty*
