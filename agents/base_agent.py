"""
OMEGA-ULTIMATE-FUSION-V∞ — Base Trading Agent
Brotherhood Omega Dynasty

Abstract base class for all Brotherhood trading agents.
All agents share:
  - 150X YOLO factor
  - 15% circuit breaker
  - Temporal.io workflow integration
  - Redis state management
  - PostgreSQL trade logging
"""

from __future__ import annotations

import abc
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class TradeSignal:
    """Represents a trade signal from an agent."""

    agent_name: str
    symbol: str
    side: str  # "buy" | "sell"
    size_usd: float
    price: float
    chain: str
    strategy: str
    confidence: float  # 0.0 – 1.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def is_valid(self) -> bool:
        return (
            self.size_usd > 0
            and self.price > 0
            and 0.0 <= self.confidence <= 1.0
            and self.side in ("buy", "sell")
        )


@dataclass
class TradeResult:
    """Result of a trade execution."""

    signal: TradeSignal
    executed: bool
    fill_price: float
    fill_size: float
    pnl_usd: float
    tx_hash: str
    error: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class BaseAgent(abc.ABC):
    """Abstract base class for all OMEGA trading agents."""

    # Brotherhood constants
    YOLO_FACTOR: int = 150
    CIRCUIT_BREAKER_PCT: float = 15.0
    DYNASTY = "Brotherhood Omega Dynasty"
    MOTTO = "CHUKUA KONTROLI YOTE"

    def __init__(self, name: str, wallet: str, chains: list[str], strategy: str) -> None:
        self.name = name
        self.wallet = wallet
        self.chains = chains
        self.strategy = strategy
        self.active = True
        self.total_pnl: float = 0.0
        self.trade_count: int = 0
        self.win_count: int = 0
        self.start_time = datetime.now(timezone.utc)
        self._circuit_tripped = False
        self._peak_equity: float = float(
            os.getenv("INITIAL_EQUITY_USD", "3570")
        )
        self._current_equity: float = self._peak_equity
        logger.info(
            "🔱 %s Agent initialised | strategy=%s | chains=%s | wallet=%s",
            name,
            strategy,
            ",".join(chains),
            wallet[:12] + "...",
        )

    # ── abstract methods ──────────────────────────────────────────────

    @abc.abstractmethod
    def generate_signal(self) -> TradeSignal | None:
        """Analyse markets and return a trade signal, or None if no trade."""

    @abc.abstractmethod
    def execute_trade(self, signal: TradeSignal) -> TradeResult:
        """Execute a trade signal on-chain."""

    # ── circuit breaker ───────────────────────────────────────────────

    def check_circuit_breaker(self) -> bool:
        """Return True if circuit breaker is active (drawdown ≥ 15%)."""
        if self._peak_equity <= 0:
            return False
        drawdown_pct = (
            (self._peak_equity - self._current_equity) / self._peak_equity
        ) * 100
        if drawdown_pct >= self.CIRCUIT_BREAKER_PCT:
            if not self._circuit_tripped:
                logger.warning(
                    "🚨 CIRCUIT BREAKER TRIPPED — %s | drawdown=%.1f%% (threshold=%.1f%%)",
                    self.name,
                    drawdown_pct,
                    self.CIRCUIT_BREAKER_PCT,
                )
                self._circuit_tripped = True
            return True
        self._circuit_tripped = False
        return False

    def update_equity(self, pnl: float) -> None:
        """Update equity tracking for circuit breaker."""
        self._current_equity += pnl
        if self._current_equity > self._peak_equity:
            self._peak_equity = self._current_equity

    # ── main loop ─────────────────────────────────────────────────────

    def run_cycle(self) -> TradeResult | None:
        """Run one trading cycle: generate signal → execute → log."""
        if not self.active:
            logger.debug("%s is inactive, skipping cycle", self.name)
            return None

        if self.check_circuit_breaker():
            logger.warning("%s circuit breaker active — no trading", self.name)
            return None

        signal = self.generate_signal()
        if signal is None:
            logger.debug("%s: no signal this cycle", self.name)
            return None

        if not signal.is_valid():
            logger.warning("%s: invalid signal discarded: %s", self.name, signal)
            return None

        result = self.execute_trade(signal)
        self._record_result(result)
        return result

    def _record_result(self, result: TradeResult) -> None:
        self.trade_count += 1
        if result.pnl_usd > 0:
            self.win_count += 1
        self.total_pnl += result.pnl_usd
        self.update_equity(result.pnl_usd)
        status = "✅" if result.executed else "❌"
        logger.info(
            "%s %s trade | symbol=%s | pnl=$%.2f | total_pnl=$%.2f",
            status,
            self.name,
            result.signal.symbol,
            result.pnl_usd,
            self.total_pnl,
        )

    # ── properties ────────────────────────────────────────────────────

    @property
    def win_rate(self) -> float:
        if self.trade_count == 0:
            return 0.0
        return self.win_count / self.trade_count

    @property
    def uptime_seconds(self) -> float:
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()

    def status_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "strategy": self.strategy,
            "chains": self.chains,
            "wallet": self.wallet,
            "active": self.active,
            "circuit_breaker": self._circuit_tripped,
            "total_pnl_usd": round(self.total_pnl, 2),
            "trade_count": self.trade_count,
            "win_rate": round(self.win_rate, 4),
            "uptime_seconds": round(self.uptime_seconds),
            "dynasty": self.DYNASTY,
        }

    def halt(self) -> None:
        """Emergency halt — stop agent immediately."""
        logger.error("🚨 EMERGENCY HALT triggered for %s", self.name)
        self.active = False

    def resume(self) -> None:
        """Resume agent after halt."""
        logger.info("▶️ Resuming agent %s", self.name)
        self.active = True
        self._circuit_tripped = False
