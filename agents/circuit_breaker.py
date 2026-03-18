"""
OMEGA-ULTIMATE-FUSION-V∞ — Circuit Breaker
Brotherhood Omega Dynasty

15% drawdown circuit breaker — protects the entire fleet.
Trips when combined portfolio equity drops ≥15% from high-water mark.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Callable

logger = logging.getLogger(__name__)

CIRCUIT_BREAKER_PCT = 15.0  # 15% max drawdown


@dataclass
class CircuitState:
    peak_equity: float
    current_equity: float
    tripped: bool = False
    trip_time: datetime | None = None
    trip_drawdown_pct: float = 0.0
    reset_count: int = 0


class CircuitBreaker:
    """
    Fleet-wide 15% circuit breaker.
    When drawdown from peak exceeds threshold, all agents are halted
    and emergency protocols are triggered.
    """

    THRESHOLD_PCT = CIRCUIT_BREAKER_PCT
    COOLDOWN_SECONDS = 3600  # 1-hour cooldown before manual reset allowed

    def __init__(
        self,
        initial_equity: float,
        on_trip: Callable[[], None] | None = None,
        on_reset: Callable[[], None] | None = None,
    ) -> None:
        self._lock = Lock()
        self._state = CircuitState(
            peak_equity=initial_equity,
            current_equity=initial_equity,
        )
        self._on_trip = on_trip
        self._on_reset = on_reset
        logger.info(
            "🔱 CircuitBreaker initialised | initial_equity=$%.2f | threshold=%.1f%%",
            initial_equity,
            self.THRESHOLD_PCT,
        )

    def update(self, new_equity: float) -> bool:
        """
        Update equity and check circuit breaker.
        Returns True if circuit is tripped.
        """
        with self._lock:
            self._state.current_equity = new_equity
            if new_equity > self._state.peak_equity:
                self._state.peak_equity = new_equity

            if self._state.peak_equity <= 0:
                return False

            drawdown_pct = (
                (self._state.peak_equity - self._state.current_equity)
                / self._state.peak_equity
            ) * 100

            if drawdown_pct >= self.THRESHOLD_PCT and not self._state.tripped:
                self._trip(drawdown_pct)
                return True

            return self._state.tripped

    def _trip(self, drawdown_pct: float) -> None:
        self._state.tripped = True
        self._state.trip_time = datetime.now(timezone.utc)
        self._state.trip_drawdown_pct = drawdown_pct
        logger.error(
            "🚨🚨🚨 CIRCUIT BREAKER TRIPPED | drawdown=%.2f%% | equity=$%.2f (peak=$%.2f)",
            drawdown_pct,
            self._state.current_equity,
            self._state.peak_equity,
        )
        if self._on_trip:
            try:
                self._on_trip()
            except Exception as e:
                logger.error("Circuit breaker callback error: %s", e)

    def reset(self, manual: bool = False) -> bool:
        """
        Reset circuit breaker. Manual reset requires cooldown elapsed.
        Returns True if reset was successful.
        """
        with self._lock:
            if not self._state.tripped:
                return True
            if manual and self._state.trip_time:
                elapsed = (datetime.now(timezone.utc) - self._state.trip_time).total_seconds()
                if elapsed < self.COOLDOWN_SECONDS:
                    remaining = int(self.COOLDOWN_SECONDS - elapsed)
                    logger.warning(
                        "Circuit breaker cooldown active — %ds remaining", remaining
                    )
                    return False
            self._state.tripped = False
            self._state.trip_time = None
            self._state.trip_drawdown_pct = 0.0
            self._state.reset_count += 1
            logger.info(
                "✅ Circuit breaker reset | resets=%d | equity=$%.2f",
                self._state.reset_count,
                self._state.current_equity,
            )
            if self._on_reset:
                try:
                    self._on_reset()
                except Exception as e:
                    logger.error("Circuit breaker reset callback error: %s", e)
            return True

    @property
    def is_tripped(self) -> bool:
        return self._state.tripped

    @property
    def current_drawdown_pct(self) -> float:
        with self._lock:
            if self._state.peak_equity <= 0:
                return 0.0
            return (
                (self._state.peak_equity - self._state.current_equity)
                / self._state.peak_equity
            ) * 100

    def status(self) -> dict:
        with self._lock:
            if self._state.peak_equity > 0:
                drawdown = (
                    (self._state.peak_equity - self._state.current_equity)
                    / self._state.peak_equity
                ) * 100
            else:
                drawdown = 0.0
            return {
                "tripped": self._state.tripped,
                "peak_equity_usd": round(self._state.peak_equity, 2),
                "current_equity_usd": round(self._state.current_equity, 2),
                "drawdown_pct": round(drawdown, 2),
                "threshold_pct": self.THRESHOLD_PCT,
                "reset_count": self._state.reset_count,
                "trip_time": self._state.trip_time.isoformat() if self._state.trip_time else None,
            }
