# 𝕏 X-TWITTER.md — X (Twitter) Automation Guide

> Auto-posting dynasty updates to @patrickdl44

---

## Profile

**Handle:** @patrickdl44
**Platform:** X (formerly Twitter)
**URL:** [x.com/patrickdl44](https://x.com/patrickdl44)

---

## X Developer API Setup

### Step 1 — Create Developer Account

1. Visit [developer.twitter.com](https://developer.twitter.com)
2. Apply for Elevated access (required for posting)
3. Create a new App: `OMEGA Dynasty Bot`

### Step 2 — Generate API Keys

In your App settings under "Keys and Tokens":
- API Key
- API Key Secret
- Access Token (your account)
- Access Token Secret

Add to `.env`:
```env
TWITTER_API_KEY=<your_api_key>
TWITTER_API_SECRET=<your_api_secret>
TWITTER_ACCESS_TOKEN=<your_access_token>
TWITTER_ACCESS_SECRET=<your_access_token_secret>
TWITTER_HANDLE=patrickdl44
```

---

## Auto-Post Triggers

| Event | Post Content |
|-------|-------------|
| Daily profit (08:00 UTC) | Daily P&L summary with progress |
| YOLO mode engaged | YOLO announcement + position |
| Profit milestone (each £500) | Milestone celebration |
| LQ-004 alert | Loan management update |
| Dynasty announcement | Custom message |
| Weekly audit | Weekly summary stats |

---

## Post Templates

### Daily Profit Post:
```
🔱 OMEGA DYNASTY DAILY UPDATE

💰 Today: +£X.XX
📊 Total: £X,XXX.XX / £16,670 (XX%)
🎯 X trades | XX% win rate
🤖 4/4 agents ACTIVE

CHUKUA KONTROLI YOTE 🔱

#OmegaDynasty #SolanaTrading #AutoTrading #Brotherhood
```

### YOLO Mode Post:
```
⚡ YOLO MODE ENGAGED

10X LEVERAGE · ALL IN
Signal: [PAIR] +X.X% momentum

The dynasty plays to WIN 🔱

#YOLO #OmegaDynasty #Solana
```

### Milestone Post:
```
💰 DYNASTY MILESTONE: £X,XXX EARNED

Progress: XX% to financial freedom
Daily compound machine running 24/7 🔱

#OmegaDynasty #PassiveIncome #Brotherhood
```

---

## Implementation

The Twitter container runs in the background and posts via the X API v2.

```bash
# Check Twitter poster status
docker compose logs -f telegram
# (Twitter posting is part of the reporting service)

# Manual post
docker exec omega-telegram node twitter-post.js --message "Test post"
```

See [integrations/twitter/poster.js](integrations/twitter/poster.js) for implementation.

---

## Rate Limits

X API Free tier allows:
- 1,500 tweets per month (posting)
- 500,000 reads per month

Configure posting frequency in `.env`:
```env
TWITTER_DAILY_POST=true
TWITTER_YOLO_POST=true
TWITTER_MILESTONE_POST=true
TWITTER_RATE_LIMIT_DAILY=10
```

---

## Hashtags

Standard dynasty hashtags to use:
`#OmegaDynasty #Brotherhood #CHUKUAKONTROLIYOTE #SolanaTrading #AutoTrading #DJSharpshooter #BitcoinOrdinals #Liquidium`

---

*Brotherhood Omega Dynasty · X-TWITTER.md · @patrickdl44*
