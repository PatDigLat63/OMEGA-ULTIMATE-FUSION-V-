# OMEGA-ULTIMATE-FUSION-V∞ — System Architecture

> Brotherhood Omega Dynasty · Technical Architecture Reference

---

## Overview

```
                    ┌─────────────────────────────────┐
                    │   GitHub Pages / CNAME           │
                    │   brotherhoodomegadynasty.com    │
                    │   index.html — Dashboard         │
                    └──────────────┬──────────────────┘
                                   │ HTTPS
                    ┌──────────────▼──────────────────┐
                    │   Nginx Reverse Proxy            │
                    │   206.189.118.255                │
                    └──┬──────┬──────┬──────┬─────────┘
                       │      │      │      │
              ┌────────▼─┐ ┌──▼──┐ ┌▼──┐ ┌─▼──────────┐
              │Orchestrat│ │API  │ │GF │ │Temporal UI  │
              │  :8000   │ │     │ │:3000│  :8080      │
              └────┬─────┘ └─────┘ └───┘ └────────────┘
                   │
     ┌─────────────┼──────────────────────┐
     │             │                      │
┌────▼────┐  ┌─────▼──────┐  ┌───────────▼──────────┐
│Temporal │  │ AgentBus   │  │  Circuit Breaker      │
│  :7233  │  │ (RabbitMQ) │  │  15% threshold        │
└────┬────┘  └─────┬──────┘  └───────────────────────┘
     │             │
     │    ┌────────┼────────────────┐
     │    │        │                │
┌────▼────▼┐ ┌─────▼──┐ ┌──────────▼──┐ ┌────────────┐
│ DJ Agent │ │HASHIM  │ │BOSSMAN Agent│ │PATRICK     │
│ Spot     │ │Deriv   │ │Ordinals     │ │Cross-chain │
│ SOL/BTC  │ │Perps   │ │Runes/Bitmap │ │12 Chains   │
└────┬─────┘ └────┬───┘ └──────┬──────┘ └─────┬──────┘
     │            │            │               │
     └────────────┴────────────┴───────────────┘
                               │
              ┌────────────────┼───────────────┐
              │                │               │
         ┌────▼────┐    ┌──────▼──┐    ┌──────▼──┐
         │Postgres │    │  Redis  │    │Prometheus│
         │  :5432  │    │  :6379  │    │  :9090   │
         └─────────┘    └─────────┘    └────┬─────┘
                                            │
                                       ┌────▼─────┐
                                       │ Grafana  │
                                       │  :3000   │
                                       └──────────┘
```

---

## Container Fleet (32 Total)

### Trading Agents (6)
| Container | Purpose |
|-----------|---------|
| `omega-agent-dj` | DJ spot trading (SOL/BTC/ETH) |
| `omega-agent-hashim` | HASHIM derivatives & perps |
| `omega-agent-bossman` | BOSSMAN Ordinals/Runes/Bitmaps |
| `omega-agent-patrick` | PATRICK cross-chain (12 chains) |
| `omega-orchestrator` | Fleet coordinator + health API |
| `omega-circuit-breaker` | 15% drawdown protection |

### Workflow Engine (3)
| Container | Purpose |
|-----------|---------|
| `omega-temporal` | Temporal.io server |
| `omega-temporal-ui` | Temporal web interface |
| `omega-temporal-worker` | Workflow task worker |

### Data Layer (2)
| Container | Purpose |
|-----------|---------|
| `omega-postgres` | PostgreSQL 16 trade ledger |
| `omega-redis` | Redis 7 state cache |

### Infrastructure (4)
| Container | Purpose |
|-----------|---------|
| `omega-agentbus` | RabbitMQ message bus |
| `omega-nginx` | Reverse proxy + SSL |
| `omega-monitor` | System monitor |
| `omega-backup` | Hourly database backup |

### Integrations (3)
| Container | Purpose |
|-----------|---------|
| `omega-telegram-bot` | Telegram kill-switch bot |
| `omega-webhook` | Webhook receiver |
| `omega-twitter-bot` | X @patrickdl44 poster |

### Observability (3)
| Container | Purpose |
|-----------|---------|
| `omega-prometheus` | Metrics collection |
| `omega-grafana` | Dashboards |
| `omega-alertmanager` | Alert routing |

### Chain RPC Proxies (12)
| Container | Chain |
|-----------|-------|
| `omega-rpc-solana` | Solana |
| `omega-rpc-bitcoin` | Bitcoin |
| `omega-rpc-ethereum` | Ethereum |
| `omega-rpc-avalanche` | Avalanche |
| `omega-rpc-polygon` | Polygon |
| `omega-rpc-arbitrum` | Arbitrum |
| `omega-rpc-optimism` | Optimism |
| `omega-rpc-bsc` | BNB Smart Chain |
| `omega-rpc-fantom` | Fantom |
| `omega-rpc-near` | NEAR |
| `omega-rpc-cosmos` | Cosmos |
| `omega-rpc-polkadot` | Polkadot |

**Total: 6 + 3 + 2 + 4 + 3 + 3 + 12 = 33 defined, 32 deployed**

---

## Data Flow

### Trade Execution
```
1. Agent.generate_signal() — market analysis
2. Signal validation (confidence, size, circuit breaker)
3. Signal published to AgentBus (RabbitMQ)
4. Agent.execute_trade(signal) — DEX/venue execution
5. TradeResult recorded to PostgreSQL
6. PnL + equity updates → Circuit breaker check
7. Prometheus metrics updated
8. If milestone → Telegram/X notification
```

### Emergency Flow
```
1. Portfolio equity drops ≥15% from peak
2. CircuitBreaker.update() returns True
3. Orchestrator._emergency_halt() called
4. All agents: agent.halt() → agent.active = False
5. Telegram alert: /evacuate message
6. WhatsApp alert
7. X emergency post
8. System waits for manual /resume
```

---

## Network Architecture

All containers run on `omega-net` (172.20.0.0/16 bridge network).

External exposure:
- Port 80 → Nginx (HTTP → HTTPS redirect)
- Port 443 → Nginx (HTTPS)
- Port 9000 → Webhook server (proxied via Nginx)

Internal only:
- 5432 (PostgreSQL), 6379 (Redis), 7233 (Temporal), 5672 (RabbitMQ)

---

## Temporal.io Workflows

| Workflow | Purpose |
|----------|---------|
| `TradingCycleWorkflow` | Periodic agent cycle execution |
| `CompoundingWorkflow` | Hourly compound calculations |
| `BackupWorkflow` | Database backup orchestration |
| `HealthCheckWorkflow` | Agent health verification |
| `EmergencyEvacuationWorkflow` | Emergency halt + notification |

---

*CHUKUA KONTROLI YOTE — Brotherhood Omega Dynasty*
