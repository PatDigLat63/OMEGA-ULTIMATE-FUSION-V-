# OMEGA-ULTIMATE-FUSION-V∞ — Configuration Reference

> Brotherhood Omega Dynasty · All environment variables and config options

---

## Environment Variables

### Core

| Variable | Default | Description |
|----------|---------|-------------|
| `INITIAL_EQUITY_USD` | `3570` | Starting AUM in USD |
| `CYCLE_INTERVAL_SECONDS` | `30` | Trading cycle interval |
| `API_PORT` | `8000` | Orchestrator HTTP API port |

### Database

| Variable | Required | Description |
|----------|----------|-------------|
| `POSTGRES_PASSWORD` | ✅ | PostgreSQL password |
| `DATABASE_URL` | auto | Full connection string (auto-built) |

### Redis

| Variable | Required | Description |
|----------|----------|-------------|
| `REDIS_PASSWORD` | ✅ | Redis auth password |
| `REDIS_URL` | auto | Connection URL (auto-built) |

### Telegram

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ | BotFather token |
| `TELEGRAM_CHAT_ID` | ✅ | Authorised chat ID |

### Twitter/X

| Variable | Required | Description |
|----------|----------|-------------|
| `TWITTER_BEARER_TOKEN` | ✅ | OAuth 2.0 bearer token |
| `TWITTER_API_KEY` | ✅ | OAuth 1.0a consumer key |
| `TWITTER_API_SECRET` | ✅ | OAuth 1.0a consumer secret |
| `TWITTER_ACCESS_TOKEN` | ✅ | OAuth 1.0a access token |
| `TWITTER_ACCESS_SECRET` | ✅ | OAuth 1.0a access secret |

### Webhook

| Variable | Default | Description |
|----------|---------|-------------|
| `WEBHOOK_SECRET` | `omega-brotherhood-secret` | HMAC signing secret |
| `PORT` | `9000` | Webhook server port |

### Monitoring

| Variable | Required | Description |
|----------|----------|-------------|
| `GRAFANA_PASSWORD` | ✅ | Grafana admin password |

---

## Agent Configuration

### Circuit Breaker
- **Threshold**: 15% drawdown from peak equity
- **Cooldown**: 1 hour before manual reset
- **Scope**: Fleet-wide (all 4 agents halted simultaneously)

### YOLO Factor
- **Setting**: 150X
- **Meaning**: Maximum aggressiveness multiplier for position sizing
- **Implementation**: Size = `equity * 0.02 * confidence²` (per agent)

### Chains
PATRICK agent operates on all 12 chains:
1. SOL (Solana)
2. BTC (Bitcoin)
3. ETH (Ethereum)
4. AVAX (Avalanche)
5. MATIC (Polygon)
6. ARB (Arbitrum)
7. OP (Optimism)
8. BSC (BNB Smart Chain)
9. FTM (Fantom)
10. NEAR (NEAR Protocol)
11. ATOM (Cosmos)
12. DOT (Polkadot)

---

## Docker Compose Profiles

```bash
# Full fleet (default)
docker compose up -d

# Agents only (no monitoring)
docker compose up -d agent-dj agent-hashim agent-bossman agent-patrick orchestrator

# Monitoring only
docker compose up -d prometheus grafana alertmanager

# Integrations only
docker compose up -d telegram-bot webhook-server twitter-bot
```

---

## Nginx Configuration

Key settings in `infrastructure/nginx/nginx.conf`:

- Rate limit: 30 req/min for API, 10 req/s for webhooks
- SSL: TLSv1.2 + TLSv1.3 only
- HSTS: 1-year max-age
- Proxy timeouts: 30s for webhooks

---

## Temporal.io Configuration

Namespace: `omega-dynasty` (default)
Workflow retention: 7 days
History size limit: 50 MB
Activity retry: max 10 attempts, exponential backoff (1s → 30s)

---

## Backup Configuration

| Setting | Value |
|---------|-------|
| Interval | 1 hour |
| Local retention | 48 backups (48 hours) |
| Remote storage | DigitalOcean Spaces |
| Compression | gzip |

---

## .env.example

```env
# ── Core ──────────────────────────────────────────
INITIAL_EQUITY_USD=3570
CYCLE_INTERVAL_SECONDS=30

# ── Database ──────────────────────────────────────
POSTGRES_PASSWORD=changeme_strong_password

# ── Redis ─────────────────────────────────────────
REDIS_PASSWORD=changeme_redis_password

# ── RabbitMQ ──────────────────────────────────────
RABBITMQ_PASSWORD=changeme_rabbit_password

# ── Grafana ───────────────────────────────────────
GRAFANA_PASSWORD=changeme_grafana_password

# ── Telegram ──────────────────────────────────────
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# ── Twitter / X ───────────────────────────────────
TWITTER_BEARER_TOKEN=
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=

# ── Webhook ───────────────────────────────────────
WEBHOOK_SECRET=changeme_webhook_secret

# ── DigitalOcean Spaces (backups) ─────────────────
DO_SPACES_KEY=
DO_SPACES_SECRET=
DO_SPACES_BUCKET=omega-backups
DO_SPACES_ENDPOINT=nyc3.digitaloceanspaces.com
```

---

*CHUKUA KONTROLI YOTE — Brotherhood Omega Dynasty*
