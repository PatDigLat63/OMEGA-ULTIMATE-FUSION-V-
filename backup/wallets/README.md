# 🔒 WALLET BACKUP — OMEGA-ULTIMATE-FUSION-V∞

> **SECURITY WARNING**: This directory contains wallet backup files.
> Never commit actual private keys or seed phrases. This README documents the system only.

---

## Backup System Overview

The wallet backup system uses GPG encryption with a 3-of-5 split key approach for maximum security while ensuring recovery is always possible.

---

## Directory Structure

```
backup/wallets/
├── README.md          — This file
├── encrypted/         — GPG-encrypted wallet files
│   ├── master.gpg     — Master encrypted backup (GPG)
│   └── .gitkeep       — Placeholder (actual backups not committed)
└── (paper/)           — Paper wallet templates (see /backup/paper/)
```

---

## Wallet Addresses (Reference)

| Agent | Network | Address (masked) |
|-------|---------|-----------------|
| DJ Sharpshooter | Solana | GJ8d...fhe8 |
| Hashim Treasury | Solana | JCYTo...Q28e |
| Bossman Risk | Solana | FodX16...QLwF |
| Patrick Scanner | Solana | GJ8d...fhe8 |
| Emergency 1 | Solana | 6q7w...pde1 |
| Emergency 2 | Solana | EcxN...u3xy |

> Full addresses visible in the dashboard (click-to-copy, never stored in plaintext here).

---

## GPG Encryption Setup

```bash
# Generate GPG key pair for OMEGA backups
gpg --gen-key
# Choose: RSA and RSA, 4096 bits, never expire
# Name: OMEGA Dynasty Backup
# Email: backup@brotherhoodomegadynasty.com

# Export public key (safe to share)
gpg --armor --export backup@brotherhoodomegadynasty.com > omega_public_key.asc

# Encrypt a wallet file
gpg --recipient backup@brotherhoodomegadynasty.com \
    --encrypt --armor \
    --output backup/wallets/encrypted/master.gpg \
    wallet_export.json

# Decrypt (requires private key)
gpg --decrypt backup/wallets/encrypted/master.gpg > wallet_export.json
```

---

## 3-of-5 Split Key System

The master decryption key is split into 5 shares using Shamir's Secret Sharing.
Any 3 of the 5 shares can reconstruct the full key.

**Key Holder Assignments:**
1. Share 1 — Commander (Patrick): Physical secure location
2. Share 2 — Trusted family member: Separate physical location
3. Share 3 — Encrypted cloud storage (personal account)
4. Share 4 — Legal representative / solicitor
5. Share 5 — Hardware wallet (offline)

**Recovery:** Combine any 3 shares using:
```bash
# Using ssss-combine (install: apt install ssss)
ssss-combine -t 3
# Enter 3 of the 5 shares when prompted
```

---

## Emergency Recovery Process

1. Locate 3 of the 5 key shares
2. Reconstruct master key: `ssss-combine -t 3`
3. Decrypt wallet: `gpg --decrypt backup/wallets/encrypted/master.gpg`
4. Import seed phrase to Phantom/Solflare wallet
5. Transfer funds to emergency wallets if needed

---

## Security Rules

- ❌ NEVER commit actual seed phrases or private keys
- ❌ NEVER share key shares digitally without encryption
- ✅ Keep `encrypted/` directory files in local secure backup only
- ✅ Test recovery process quarterly
- ✅ Rotate GPG keys annually

---

*Brotherhood Omega Dynasty · Wallet Security · PROTECT THE DYNASTY*
