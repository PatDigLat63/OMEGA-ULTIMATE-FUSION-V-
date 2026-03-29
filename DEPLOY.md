# 🚀 DEPLOY.md — OMEGA-ULTIMATE-FUSION-V∞ Deployment Guide

> Complete deployment instructions for the Brotherhood Omega Dynasty system.

---

## Prerequisites

- Docker Engine 24+
- Docker Compose v2.20+
- Git
- Access to DigitalOcean droplet: 206.189.118.255
- Environment variables configured (see [CONFIG.md](CONFIG.md))

---

## Step 1 — SSH into the Server

```bash
ssh root@206.189.118.255
# or with key:
ssh -i ~/.ssh/brotherhood_key root@206.189.118.255
```

---

## Step 2 — Clone / Pull Latest Code

```bash
cd /opt/omega
git pull origin main
# First time:
git clone https://github.com/PatDigLat63/OMEGA-ULTIMATE-FUSION-V-.git /opt/omega
```

---

## Step 3 — Configure Environment

```bash
cp .env.example .env
nano .env
# Fill in all required values (see CONFIG.md)
```

---

## Step 4 — Launch All 14 Containers

```bash
cd /opt/omega/infrastructure/docker
docker compose up -d --build
```

### Verify deployment:
```bash
docker compose ps
# All 14 should show "Up" or "healthy"
```

---

## Step 5 — Check Health

```bash
# Check all containers
docker compose ps

# Check logs for any agent
docker compose logs -f dj
docker compose logs -f hashim
docker compose logs -f bossman
docker compose logs -f patrick

# Check system resources
docker stats --no-stream
```

---

## docker-compose.yml (Full 14-Service Stack)

See [infrastructure/docker/docker-compose.yml](infrastructure/docker/docker-compose.yml) for the complete file.

---

## Auto-Restart Policy

All containers use `restart: unless-stopped` policy. They automatically restart on failure within 30 seconds.

---

## Health Checks

Each container has a health check configured:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:PORT/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## Cron Jobs Setup

```bash
crontab -e
```

Add these lines:
```cron
# Compound cycle — every hour
0 * * * * docker exec omega-evolver node compound.js >> /var/log/omega/compound.log 2>&1

# Evolver mutation — every 6 hours
0 */6 * * * docker exec omega-evolver node evolve.js >> /var/log/omega/evolver.log 2>&1

# Backup to GitHub — every 12 hours
0 */12 * * * /opt/omega/infrastructure/server/backup.sh >> /var/log/omega/backup.log 2>&1

# Daily profit report — 08:00 UTC
0 8 * * * docker exec omega-ledger node report.js --daily >> /var/log/omega/reports.log 2>&1

# Weekly dynasty audit — Sunday 00:00 UTC
0 0 * * 0 docker exec omega-ledger node audit.js --full >> /var/log/omega/audit.log 2>&1
```

---

## GitHub Pages Deployment

The dashboard (index.html) is served via GitHub Pages at:
- https://patdigLat63.github.io/OMEGA-ULTIMATE-FUSION-V-/
- https://brotherhoodomegadynasty.com (custom domain via CNAME)

### Enable GitHub Pages:
1. Go to repository Settings → Pages
2. Source: `main` branch, root folder (`/`)
3. Custom domain: `brotherhoodomegadynasty.com`
4. Enforce HTTPS: ✅ YES

---

## Rollback

```bash
# Rollback to previous commit
git log --oneline -10
git checkout <commit-hash>
docker compose up -d --build

# Emergency: stop all containers
docker compose down
```

---

## Backup & Recovery

```bash
# Manual backup
/opt/omega/infrastructure/server/backup.sh

# Restore from backup
/opt/omega/infrastructure/server/restore.sh <backup-date>
```

---

*Brotherhood Omega Dynasty · DEPLOY.md · THE FINAL FORM*
