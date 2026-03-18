# 🔱 OMEGA-ULTIMATE-FUSION-V∞ 🔱

> The final, verified fortress of the Brotherhood Omega Dynasty.  
> 15 Autonomous Containers · 12 Chains · 150X YOLO · 15% Circuit Breaker · 99.999% Uptime  
> Self-deploying · Self-evolving · Unstoppable  
> **CHUKUA KONTROLI YOTE.**

---

## 🚨 PRIORITY-ZERO DIRECTIVE

**Liquidium Loan LQ-004 is URGENT.**  
The system is programmed to handle this immediately upon awakening.

---

## Architecture

| Layer | Services |
|---|---|
| **Core Infrastructure** | PostgreSQL 15, Redis 7, Agent Bus, Dashboard (nginx) |
| **Autonomous Agents** | DJ `:3003`, Hashim `:3004`, Bossman `:3006`, Patrick `:3005` |
| **Core Services** | Ledger `:3010`, Learner `:3011`, Evolver `:3012`, Telegram `:3013`, Scanner `:3014`, Hustle `:3001` |

All containers run on the shared `omega_net` bridge network.

---

## Deployment

Deployment is handled automatically by the **GitHub Actions CI/CD pipeline**.  
Every push to the `main` branch triggers a fresh deploy to the DigitalOcean droplet.

### Manual deploy / First-time awakening

```bash
# 1. Connect to the host
ssh root@206.189.118.255

# 2. Navigate to the fortress
cd /opt/omega-fusion

# 3. Grant secrets (fill in ALL values)
cp .env.template .env
nano .env

# 4. Awaken the system
docker-compose up -d
```

### Updating the running system

```bash
cd /opt/omega-fusion
git pull origin main
docker-compose up -d --build
```

---

## Required Secrets

Copy `.env.template` to `.env` and fill in every value.  
See `.env.template` for the full list of required keys.

> ⚠️ **Never commit `.env` to version control.**

---

## Master Console (Dashboard)

Once running, visit:  
`http://206.189.118.255:8082/` — or — `http://brotherhoodomegadynasty.com:8082/`

---

### 🔱 CHUKUA KONTROLI YOTE 🔱
