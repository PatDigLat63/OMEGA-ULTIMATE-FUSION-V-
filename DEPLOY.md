# OMEGA-ULTIMATE-FUSION-V∞ — Deployment Guide

> Brotherhood Omega Dynasty · DigitalOcean · Ubuntu 24.04

## Prerequisites

- DigitalOcean Droplet (min 4 vCPU / 8 GB RAM) at `206.189.118.255`
- SSH access as root or sudo user
- Domain DNS pointed to server: `brotherhoodomegadynasty.com → 206.189.118.255`
- Docker + Docker Compose v2 installed

---

## 1. Server Bootstrap

```bash
# SSH into server
ssh root@206.189.118.255

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh
systemctl enable docker && systemctl start docker

# Install Docker Compose v2
mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 \
    -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose

# Verify
docker compose version
```

---

## 2. Clone Repository

```bash
git clone https://github.com/PatDigLat63/OMEGA-ULTIMATE-FUSION-V-
cd OMEGA-ULTIMATE-FUSION-V-
```

---

## 3. Configure Environment

```bash
cp .env.example .env
nano .env
```

Required variables in `.env`:

```env
# PostgreSQL
POSTGRES_PASSWORD=<strong-random-password>

# Redis
REDIS_PASSWORD=<strong-random-password>

# RabbitMQ
RABBITMQ_PASSWORD=<strong-random-password>

# Grafana
GRAFANA_PASSWORD=<strong-random-password>

# Telegram Bot
TELEGRAM_BOT_TOKEN=<bot-token-from-BotFather>
TELEGRAM_CHAT_ID=<your-chat-id>

# Twitter/X
TWITTER_BEARER_TOKEN=<bearer-token>
TWITTER_API_KEY=<api-key>
TWITTER_API_SECRET=<api-secret>
TWITTER_ACCESS_TOKEN=<access-token>
TWITTER_ACCESS_SECRET=<access-secret>

# Webhook
WEBHOOK_SECRET=<strong-random-secret>

# Initial AUM
INITIAL_EQUITY_USD=3570
```

---

## 4. SSL Certificate

```bash
# Install Certbot
apt install certbot -y

# Issue certificate
certbot certonly --standalone \
    -d brotherhoodomegadynasty.com \
    -d www.brotherhoodomegadynasty.com \
    --email patrick@brotherhoodomegadynasty.com \
    --agree-tos --non-interactive

# Link to nginx path
mkdir -p /etc/ssl/certs /etc/ssl/private
ln -sf /etc/letsencrypt/live/brotherhoodomegadynasty.com/fullchain.pem /etc/ssl/certs/omega.crt
ln -sf /etc/letsencrypt/live/brotherhoodomegadynasty.com/privkey.pem /etc/ssl/private/omega.key

# Auto-renewal cron
echo "0 3 * * * certbot renew --quiet" | crontab -
```

---

## 5. Deploy the Fleet

```bash
cd infrastructure/docker
docker compose up -d --build

# Verify all 32 containers running
docker compose ps
```

Expected output (32 containers, all Up):

```
omega-agent-dj         Up
omega-agent-hashim     Up
omega-agent-bossman    Up
omega-agent-patrick    Up
omega-orchestrator     Up
omega-circuit-breaker  Up
omega-postgres         Up (healthy)
omega-redis            Up (healthy)
omega-temporal         Up (healthy)
omega-temporal-ui      Up
omega-temporal-worker  Up
omega-agentbus         Up (healthy)
omega-telegram-bot     Up
omega-webhook          Up
omega-twitter-bot      Up
omega-nginx            Up (healthy)
omega-prometheus       Up
omega-grafana          Up
omega-alertmanager     Up
omega-monitor          Up
omega-backup           Up
omega-rpc-solana       Up
omega-rpc-bitcoin      Up
omega-rpc-ethereum     Up
omega-rpc-avalanche    Up
omega-rpc-polygon      Up
omega-rpc-arbitrum     Up
omega-rpc-optimism     Up
omega-rpc-bsc          Up
omega-rpc-fantom       Up
omega-rpc-near         Up
omega-rpc-cosmos       Up
omega-rpc-polkadot     Up
```

---

## 6. Verify Deployment

```bash
# Check fleet status
curl http://localhost:8000/status | python3 -m json.tool

# Check Telegram bot
# Send /status to your bot

# Check Grafana
# Open https://brotherhoodomegadynasty.com/grafana

# Check Temporal UI
# Open https://brotherhoodomegadynasty.com/temporal
```

---

## 7. GitHub Pages

The `index.html` dashboard is automatically served at:
- `https://patdiglat63.github.io/OMEGA-ULTIMATE-FUSION-V-/`
- `https://brotherhoodomegadynasty.com/` (via CNAME)

Enable GitHub Pages in repo Settings → Pages → Branch: main → folder: root.

---

## Monitoring

| Service | URL |
|---------|-----|
| Grafana | `https://brotherhoodomegadynasty.com/grafana` |
| Temporal | `https://brotherhoodomegadynasty.com/temporal` |
| Status API | `https://brotherhoodomegadynasty.com/api/status` |
| Webhook | `https://brotherhoodomegadynasty.com/webhook/ping` |

---

## Updating

```bash
# Pull latest code
git pull

# Rebuild and restart
cd infrastructure/docker
docker compose up -d --build

# Zero-downtime rolling update for agents
docker compose up -d --no-deps --build agent-dj agent-hashim agent-bossman agent-patrick
```

---

## Rollback

```bash
# Rollback to previous image
docker compose down
git checkout HEAD~1
docker compose up -d --build
```

---

*CHUKUA KONTROLI YOTE — Brotherhood Omega Dynasty*
