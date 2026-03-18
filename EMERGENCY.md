# OMEGA-ULTIMATE-FUSION-V∞ — Emergency Protocols

> Brotherhood Omega Dynasty · Emergency Response Guide

**READ THIS BEFORE TOUCHING THE KILL SWITCH**

---

## Severity Levels

| Level | Condition | Response |
|-------|-----------|----------|
| 🟡 WARNING | Drawdown 5–10% | Monitor closely, reduce sizes |
| 🟠 ALERT | Drawdown 10–14% | Pause new entries, review positions |
| 🔴 CRITICAL | Drawdown ≥15% | **Circuit breaker auto-trips** |
| 🚨 EMERGENCY | Manual halt needed | Execute DYNASTY PROTOCOL |

---

## DYNASTY PROTOCOL — Step by Step

### Automatic (Circuit Breaker ≥15%)

The system handles this automatically:
1. Fleet-wide trade halt (all 4 agents stop)
2. Telegram alert to `TELEGRAM_CHAT_ID`
3. WhatsApp alert to `+44 7424 394382`
4. X post from `@patrickdl44`
5. Positions remain open (not force-closed automatically)
6. Monitor via Grafana: `https://brotherhoodomegadynasty.com/grafana`

### Manual Emergency Halt

**Via Telegram (fastest):**
```
/evacuate
```

**Via SSH (nuclear option):**
```bash
ssh root@206.189.118.255
cd /root/OMEGA-ULTIMATE-FUSION-V-/infrastructure/docker
docker compose stop agent-dj agent-hashim agent-bossman agent-patrick orchestrator
```

**Via WhatsApp:**
Send `HALT` to `+44 7424 394382`

---

## Position Closure

After halting agents, close positions manually:

### Solana (DJ/HASHIM)
1. Open Phantom Wallet
2. Connect to wallet `GJ8ddFTVatiWpYEQZqfRNtpVFhG48JT79PL8V5AFfhe8`
3. Close all open orders via Jupiter/dYdX

### Bitcoin (BOSSMAN)
1. Log into Magic Eden / Gamma.io
2. Delist all Ordinal listings
3. Transfer to emergency vault if needed

### Cross-chain (PATRICK)
1. Pause all bridge transactions
2. Withdraw from yield protocols
3. Bridge funds back to primary wallet

---

## Emergency Wallet Activation

If primary wallet is compromised:

```
Emergency Vault 1: 6q7wbjuPnSE9pBPQ838YfcSQDyMahmXrx3RYxPSYpde1
Emergency Vault 2: EcxNACs4n6rekZR3JCYDBjaVJbyQfn9StYYNRUsHu3xy
```

1. Connect hardware wallet (Ledger/Trezor)
2. Import emergency vault address
3. 2-of-3 multisig required for withdrawals
4. Transfer primary wallet assets to Emergency Vault 1
5. Report to Brotherhood via encrypted channel

---

## Resuming After Emergency

1. Identify root cause of drawdown
2. Review trade logs: `docker compose logs agent-dj agent-hashim`
3. Check Grafana for anomalies
4. Discuss with Brotherhood before resuming
5. Reset circuit breaker (requires 1-hour cooldown):

**Via Telegram:**
```
/resume
```

**Via SSH:**
```bash
curl -X POST http://206.189.118.255:8000/circuit-breaker/reset \
    -H "X-Omega-Secret: <secret>"
```

---

## Server Recovery

If DigitalOcean droplet is down:

```bash
# 1. Provision new droplet from snapshot
# (Take snapshots monthly!)
doctl compute droplet-action snapshot <droplet-id>

# 2. Or rebuild from scratch
bash DEPLOY.md instructions

# 3. Restore latest database
bash backup/scripts/restore.sh

# 4. Verify wallet addresses before deploying
cat backup/wallets/README.md
```

---

## Communication During Emergency

| Channel | Contact | Message |
|---------|---------|---------|
| Telegram | Bot | `/evacuate` |
| WhatsApp | `+44 7424 394382` | `HALT` |
| X | `@patrickdl44` | Emergency post (auto) |

---

## Post-Emergency Review

Within 24 hours:
- [ ] Root cause analysis
- [ ] PnL impact assessment
- [ ] System improvement plan
- [ ] Brotherhood debrief
- [ ] Update emergency protocols if needed

---

*Brotherhood stays calm under pressure.*
*CHUKUA KONTROLI YOTE — Brotherhood Omega Dynasty*
