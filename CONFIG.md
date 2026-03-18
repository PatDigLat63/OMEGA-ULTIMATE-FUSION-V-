# ⚙️ CONFIG.md — OMEGA-ULTIMATE-FUSION-V∞ Configuration Reference

> **SECURITY WARNING**: Never commit actual API keys, private keys, or secrets to this repository.
> Use environment variables exclusively. This file documents the **variables** required, not their values.

---

## Environment Variables (.env)

Copy `.env.example` to `.env` and fill in all values before deploying.

```env
# ── SERVER ──────────────────────────────────────────
SERVER_IP=206.189.118.255
SERVER_REGION=lon1
DOMAIN=brotherhoodomegadynasty.com

# ── DATABASE ─────────────────────────────────────────
POSTGRES_USER=omega_user
POSTGRES_PASSWORD=<set_strong_password>
POSTGRES_DB=omega_db
POSTGRES_PORT=5432

# ── REDIS ────────────────────────────────────────────
REDIS_PORT=6379
REDIS_PASSWORD=<set_strong_password>

# ── AGENT PORTS ──────────────────────────────────────
DJ_PORT=3003
HASHIM_PORT=3004
PATRICK_PORT=3005
BOSSMAN_PORT=3006
AGENTBUS_HTTP_PORT=8081
AGENTBUS_WS_PORT=9081
DASHBOARD_PORT=8082
LEDGER_PORT=3010
LEARNER_PORT=3011
EVOLVER_PORT=3012
TELEGRAM_PORT=3013
SCANNER_PORT=3014
HUSTLE_BRIDGE_PORT=3001

# ── SOLANA RPC ───────────────────────────────────────
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_WS_URL=wss://api.mainnet-beta.solana.com
HELIUS_API_KEY=<your_helius_api_key>

# ── TELEGRAM ─────────────────────────────────────────
TELEGRAM_BOT_TOKEN=<from_botfather>
TELEGRAM_CHAT_ID=<your_chat_id>
TELEGRAM_WEBHOOK_URL=https://brotherhoodomegadynasty.com/webhook/telegram

# ── WHATSAPP ─────────────────────────────────────────
WHATSAPP_PHONE=+447424394382
WHATSAPP_API_KEY=<your_whatsapp_business_api_key>
WHATSAPP_WEBHOOK_SECRET=<set_webhook_secret>

# ── X / TWITTER ──────────────────────────────────────
TWITTER_API_KEY=<your_twitter_api_key>
TWITTER_API_SECRET=<your_twitter_api_secret>
TWITTER_ACCESS_TOKEN=<your_access_token>
TWITTER_ACCESS_SECRET=<your_access_token_secret>
TWITTER_HANDLE=patrickdl44

# ── TRADING ──────────────────────────────────────────
DAILY_PROFIT_TARGET=16.67
TOTAL_PROFIT_TARGET=16670
YOLO_MULTIPLIER=10
CIRCUIT_BREAKER_PCT=15
MAX_DRAWDOWN_PCT=20
COMPOUND_INTERVAL_HOURS=1

# ── BACKUP ───────────────────────────────────────────
GITHUB_BACKUP_REPO=PatDigLat63/OMEGA-ULTIMATE-FUSION-V-
GITHUB_TOKEN=<your_github_token>
BACKUP_INTERVAL_HOURS=12
```

---

## Agent Wallet Addresses

> Full addresses are in the dashboard. Masked here for security.

| Agent | Wallet (masked) |
|-------|----------------|
| DJ Sharpshooter | `GJ8d...fhe8` |
| Hashim Treasury | `JCYTo...Q28e` |
| Bossman Risk | `FodX16...QLwF` |
| Patrick Scanner | `GJ8d...fhe8` |
| Emergency 1 | `6q7w...pde1` |
| Emergency 2 | `EcxN...u3xy` |

---

## API Keys Required

| Service | Purpose | Where to Get |
|---------|---------|--------------|
| Helius | Solana RPC & WebSocket | [helius.dev](https://helius.dev) |
| Telegram BotFather | Bot token | [@BotFather](https://t.me/BotFather) |
| WhatsApp Business API | Messaging | [business.whatsapp.com](https://business.whatsapp.com) |
| X Developer API | Auto-posting | [developer.twitter.com](https://developer.twitter.com) |
| GitHub Token | Backup writes | [github.com/settings/tokens](https://github.com/settings/tokens) |

---

## Security Best Practices

1. **Never commit `.env`** — it is in `.gitignore`
2. **Rotate API keys** every 90 days
3. **Use strong passwords** for PostgreSQL and Redis (32+ chars)
4. **Restrict SSH** — key-based auth only, disable password auth
5. **Firewall rules** — only open required ports (22, 80, 443, 8082)
6. **GPG encrypt** wallet backups before storage

---

*Brotherhood Omega Dynasty · CONFIG.md · KEEP SECRETS SECRET*
