"""
OMEGA-ULTIMATE-FUSION-V∞ — Circuit Breaker Test Suite
"""

import pytest
from agents.circuit_breaker import CircuitBreaker


class TestCircuitBreaker:
    def test_initialisation(self):
        cb = CircuitBreaker(initial_equity=3570.0)
        assert not cb.is_tripped
        assert cb.current_drawdown_pct == 0.0

    def test_no_trip_below_threshold(self):
        cb = CircuitBreaker(initial_equity=1000.0)
        cb.update(920.0)  # 8% drawdown — below 15%
        assert not cb.is_tripped

    def test_trips_at_threshold(self):
        cb = CircuitBreaker(initial_equity=1000.0)
        cb.update(840.0)  # 16% drawdown — above 15%
        assert cb.is_tripped

    def test_trips_exactly_at_threshold(self):
        cb = CircuitBreaker(initial_equity=1000.0)
        cb.update(850.0)  # exactly 15% drawdown
        assert cb.is_tripped

    def test_on_trip_callback_fired(self):
        fired = []
        cb = CircuitBreaker(initial_equity=1000.0, on_trip=lambda: fired.append(True))
        cb.update(800.0)
        assert len(fired) == 1

    def test_callback_fired_only_once(self):
        fired = []
        cb = CircuitBreaker(initial_equity=1000.0, on_trip=lambda: fired.append(True))
        cb.update(800.0)
        cb.update(750.0)  # deeper — should NOT fire again
        assert len(fired) == 1

    def test_peak_equity_updates_on_gain(self):
        cb = CircuitBreaker(initial_equity=1000.0)
        cb.update(1100.0)  # new high
        cb.update(935.0)   # 15% below 1100 = 935 → should trip
        assert cb.is_tripped

    def test_reset_after_cooldown(self):
        cb = CircuitBreaker(initial_equity=1000.0)
        cb.update(800.0)
        assert cb.is_tripped
        # Force trip_time to be old enough
        from datetime import datetime, timezone, timedelta
        cb._state.trip_time = datetime.now(timezone.utc) - timedelta(seconds=3700)
        reset_ok = cb.reset(manual=True)
        assert reset_ok
        assert not cb.is_tripped

    def test_reset_before_cooldown_denied(self):
        cb = CircuitBreaker(initial_equity=1000.0)
        cb.update(800.0)
        assert cb.is_tripped
        reset_ok = cb.reset(manual=True)
        assert not reset_ok
        assert cb.is_tripped  # still tripped

    def test_on_reset_callback(self):
        resets = []
        cb = CircuitBreaker(
            initial_equity=1000.0,
            on_reset=lambda: resets.append(True),
        )
        cb.update(800.0)
        from datetime import datetime, timezone, timedelta
        cb._state.trip_time = datetime.now(timezone.utc) - timedelta(seconds=3700)
        cb.reset(manual=True)
        assert len(resets) == 1

    def test_status_dict_structure(self):
        cb = CircuitBreaker(initial_equity=3570.0)
        status = cb.status()
        assert "tripped" in status
        assert "peak_equity_usd" in status
        assert "current_equity_usd" in status
        assert "drawdown_pct" in status
        assert "threshold_pct" in status
        assert status["threshold_pct"] == 15.0

    def test_drawdown_pct_accuracy(self):
        cb = CircuitBreaker(initial_equity=1000.0)
        cb.update(900.0)
        assert abs(cb.current_drawdown_pct - 10.0) < 0.01

    def test_zero_initial_equity_no_crash(self):
        cb = CircuitBreaker(initial_equity=0.0)
        tripped = cb.update(0.0)
        assert not tripped

    def test_brotherhood_threshold_is_15pct(self):
        cb = CircuitBreaker(initial_equity=100.0)
        assert cb.THRESHOLD_PCT == 15.0

    def test_reset_count_increments(self):
        cb = CircuitBreaker(initial_equity=1000.0)
        cb.update(800.0)
        from datetime import datetime, timezone, timedelta
        cb._state.trip_time = datetime.now(timezone.utc) - timedelta(seconds=3700)
        cb.reset(manual=True)
        assert cb._state.reset_count == 1
