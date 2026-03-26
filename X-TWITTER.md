# OMEGA-ULTIMATE-FUSION-V∞ — X (Twitter) Integration Guide

> Brotherhood Omega Dynasty · @patrickdl44 dynasty announcements

---

## Overview

The Twitter/X bot automatically posts dynasty updates, PnL milestones, and emergency alerts from `@patrickdl44`. It uses Twitter API v2 with OAuth 1.0a.

---

## Setup

### 1. Twitter Developer Account

```
1. Apply at developer.twitter.com
2. Create a new App (call it "OMEGA Dynasty Bot")
3. Enable OAuth 1.0a with Read+Write permissions
4. Generate all 4 keys:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret
5. Also get your Bearer Token from OAuth 2.0 section
```

### 2. Environment Variables

```env
TWITTER_BEARER_TOKEN=<bearer-token>
TWITTER_API_KEY=<api-key>
TWITTER_API_SECRET=<api-secret>
TWITTER_ACCESS_TOKEN=<access-token>
TWITTER_ACCESS_SECRET=<access-secret>
```

### 3. Start Bot

```bash
docker compose up -d twitter-bot
# OR
python -m integrations.twitter.bot
```

---

## Auto-Post Schedule

| Trigger | Content |
|---------|---------|
| Startup | "OMEGA is LIVE" announcement |
| Every +$100 PnL | PnL milestone update |
| Emergency halt | Emergency alert post |
| Circuit breaker | Drawdown warning |
| Daily (configurable) | Daily performance report |

---

## Tweet Templates

### Startup
```
🔱 OMEGA-ULTIMATE-FUSION-V∞ is LIVE.
4 agents trading. 12 chains. 150X YOLO.
CHUKUA KONTROLI YOTE
#OMEGA #BrotherhoodDynasty #Web3 #DeFi #Crypto
```

### PnL Milestone
```
📊 Fleet PnL milestone: +$500
AUM: $4,070 | Agents: DJ·HASHIM·BOSSMAN·PATRICK
CHUKUA KONTROLI YOTE
#OMEGA #BrotherhoodDynasty #Web3 #DeFi #Crypto
```

### Emergency
```
🚨 OMEGA EMERGENCY PROTOCOL ACTIVE
All positions closing. Brotherhood safe mode engaged.
#OMEGA #BrotherhoodDynasty #Web3 #DeFi #Crypto
```

---

## Rate Limits

Twitter API v2 rate limits:
- **Free tier**: 1,500 tweets/month
- **Basic**: 3,000 tweets/month
- **Pro**: 300,000 tweets/month

The bot includes a minimum 1-hour gap between posts to stay well within limits.

---

## Manual Post via CLI

```bash
# Post a custom update
python3 -c "
from integrations.twitter.bot import TwitterBot
bot = TwitterBot()
bot.post_alert('🔱 OMEGA fleet performance update: all systems nominal. CHUKUA KONTROLI YOTE #OMEGA')
"
```

---

## Dry Run Mode

If Twitter credentials are not configured, the bot runs in dry-run mode:
- Logs tweet content to stdout
- Does NOT make API calls
- Returns success (for testing)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Auth errors | Re-generate all 4 OAuth tokens |
| Rate limit exceeded | Reduce post frequency, upgrade tier |
| 403 Forbidden | Check app has Write permissions enabled |
| Bot not posting | Check `docker logs omega-twitter-bot` |

---

## Follow @patrickdl44

The `@patrickdl44` account is the official Brotherhood Omega Dynasty voice on X:
- Live trading updates
- Dynasty announcements
- System status broadcasts
- Legacy & lineage posts

---

*CHUKUA KONTROLI YOTE — Brotherhood Omega Dynasty*
