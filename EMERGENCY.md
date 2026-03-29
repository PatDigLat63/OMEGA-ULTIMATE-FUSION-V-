# 🚨 EMERGENCY.md — Kill Switch Procedures

> **Brotherhood Omega Dynasty Emergency Protocol**
> Use these procedures ONLY when immediate action is required to protect funds.

---

## ⚡ Level 1 — Pause Trading (Soft Stop)

Pauses new trades but keeps positions open.

### Via Telegram Bot:
```
/pause
```

### Via Dashboard:
Click **EVACUATE** button in the red alert banner.

### Via SSH:
```bash
ssh root@206.189.118.255
docker exec omega-bossman node pause.js
```

---

## 🚨 Level 2 — Close All Positions (Evacuation)

Closes all open positions and returns funds to treasury wallet.

### Via Telegram Bot:
```
/evacuate
```

### Via Dashboard:
1. Open the red alert banner
2. Click **EVACUATE**
3. Confirm in command log

### Via SSH:
```bash
ssh root@206.189.118.255
docker exec omega-bossman node evacuate.js --all
```

---

## 💀 Level 3 — Full System Shutdown (Nuclear Option)

Stops ALL containers. **Use only in extreme emergency.**

```bash
ssh root@206.189.118.255
cd /opt/omega/infrastructure/docker
docker compose down --timeout 30
```

### Restart after nuclear option:
```bash
docker compose up -d
```

---

## 💰 Emergency Fund Recovery

If server is unreachable, recover funds directly via wallet:

### Required Information:
- Seed phrases stored encrypted in `/backup/wallets/encrypted/`
- Recovery key split across 5 locations (3-of-5 required)

### Recovery Steps:
1. Retrieve 3 of 5 key shares
2. GPG decrypt: `gpg --decrypt backup/wallets/encrypted/master.gpg`
3. Import to Phantom/Solflare wallet
4. Transfer to emergency wallet addresses:
   - Emergency 1: `6q7wbjuPnSE9pBPQ838YfcSQDyMahmXrx3RYxPSYpde1`
   - Emergency 2: `EcxNACs4n6rekZR3JCYDBjaVJbyQfn9StYYNRUsHu3xy`

---

## ⚠️ LQ-004 Liquidium Loan — URGENT PROCEDURE

**Loan expires in 2 days.** Take action immediately.

### Option A — Repay Loan:
```
/evacuate        (close positions to raise funds)
/pnl             (check available balance)
```
Then repay directly via Liquidium platform.

### Option B — Extend Loan:
Log into Liquidium and extend before expiry.

### Option C — Refinance:
Contact Liquidium support for refinancing options.

**Contact:** Telegram @OmegaDynastyBot · WhatsApp +44 7424 394382

---

## 📞 Emergency Contacts

| Channel | Address | Command |
|---------|---------|---------|
| Telegram | @OmegaDynastyBot | `/evacuate` |
| WhatsApp | +44 7424 394382 | Send "EMERGENCY" |
| X (Twitter) | @patrickdl44 | DM "EVACUATE" |
| SSH | 206.189.118.255 | Direct server access |

---

## 🔄 Post-Emergency Checklist

After any emergency:
- [ ] Verify all funds are secured
- [ ] Check database integrity: `docker exec omega-postgres pg_dump omega_db > emergency_backup.sql`
- [ ] Review logs: `docker compose logs --since 1h > emergency_logs.txt`
- [ ] Notify dynasty via Telegram/WhatsApp
- [ ] Post-mortem analysis
- [ ] Update EMERGENCY.md with lessons learned
- [ ] Resume trading when safe: `/resume`

---

*Brotherhood Omega Dynasty · EMERGENCY.md · PROTECT THE DYNASTY*
