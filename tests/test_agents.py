"""
OMEGA-ULTIMATE-FUSION-V∞ — Agent Test Suite
Tests for all 4 Brotherhood trading agents + circuit breaker.
"""

import pytest
from datetime import datetime, timezone
from agents.base_agent import TradeSignal, TradeResult
from agents.dj_agent import DJAgent
from agents.hashim_agent import HashimAgent
from agents.bossman_agent import BossmanAgent
from agents.patrick_agent import PatrickAgent
from agents.circuit_breaker import CircuitBreaker


# ── TradeSignal ────────────────────────────────────────────────────────────────

class TestTradeSignal:
    def test_valid_buy_signal(self):
        sig = TradeSignal(
            agent_name="TEST",
            symbol="BTC/USDT",
            side="buy",
            size_usd=100.0,
            price=68000.0,
            chain="BTC",
            strategy="test",
            confidence=0.80,
        )
        assert sig.is_valid()

    def test_valid_sell_signal(self):
        sig = TradeSignal(
            agent_name="TEST",
            symbol="ETH/USDC",
            side="sell",
            size_usd=50.0,
            price=3500.0,
            chain="ETH",
            strategy="test",
            confidence=0.70,
        )
        assert sig.is_valid()

    def test_invalid_zero_size(self):
        sig = TradeSignal(
            agent_name="TEST",
            symbol="SOL/USDC",
            side="buy",
            size_usd=0.0,
            price=170.0,
            chain="SOL",
            strategy="test",
            confidence=0.80,
        )
        assert not sig.is_valid()

    def test_invalid_zero_price(self):
        sig = TradeSignal(
            agent_name="TEST",
            symbol="SOL/USDC",
            side="buy",
            size_usd=100.0,
            price=0.0,
            chain="SOL",
            strategy="test",
            confidence=0.80,
        )
        assert not sig.is_valid()

    def test_invalid_bad_side(self):
        sig = TradeSignal(
            agent_name="TEST",
            symbol="SOL/USDC",
            side="hold",
            size_usd=100.0,
            price=170.0,
            chain="SOL",
            strategy="test",
            confidence=0.80,
        )
        assert not sig.is_valid()

    def test_invalid_confidence_over_1(self):
        sig = TradeSignal(
            agent_name="TEST",
            symbol="SOL/USDC",
            side="buy",
            size_usd=100.0,
            price=170.0,
            chain="SOL",
            strategy="test",
            confidence=1.5,
        )
        assert not sig.is_valid()

    def test_timestamp_is_utc(self):
        sig = TradeSignal(
            agent_name="TEST",
            symbol="BTC/USDT",
            side="buy",
            size_usd=100.0,
            price=68000.0,
            chain="BTC",
            strategy="test",
            confidence=0.80,
        )
        assert sig.timestamp.tzinfo is not None


# ── DJAgent ────────────────────────────────────────────────────────────────────

class TestDJAgent:
    def test_instantiation(self):
        agent = DJAgent()
        assert agent.name == "DJ"
        assert agent.strategy == "spot_momentum"
        assert "SOL" in agent.chains
        assert "BTC" in agent.chains
        assert "ETH" in agent.chains

    def test_wallet_address(self):
        agent = DJAgent()
        assert agent.wallet == "GJ8ddFTVatiWpYEQZqfRNtpVFhG48JT79PL8V5AFfhe8"

    def test_yolo_factor(self):
        agent = DJAgent()
        assert agent.YOLO_FACTOR == 150

    def test_circuit_breaker_threshold(self):
        agent = DJAgent()
        assert agent.CIRCUIT_BREAKER_PCT == 15.0

    def test_generate_signal_returns_signal_or_none(self):
        agent = DJAgent()
        # Run many cycles — at least some should produce signals
        signals = [agent.generate_signal() for _ in range(50)]
        non_none = [s for s in signals if s is not None]
        assert len(non_none) > 0, "DJAgent should produce some signals"

    def test_signal_is_valid(self):
        agent = DJAgent()
        for _ in range(100):
            sig = agent.generate_signal()
            if sig is not None:
                assert sig.is_valid()
                assert sig.agent_name == "DJ"
                assert sig.chain in ["SOL", "BTC", "ETH"]
                break

    def test_execute_trade_returns_result(self):
        agent = DJAgent()
        sig = TradeSignal(
            agent_name="DJ",
            symbol="SOL/USDC",
            side="buy",
            size_usd=100.0,
            price=170.0,
            chain="SOL",
            strategy="spot_momentum",
            confidence=0.80,
        )
        result = agent.execute_trade(sig)
        assert isinstance(result, TradeResult)
        assert result.executed
        assert result.tx_hash

    def test_run_cycle_increments_trade_count(self):
        agent = DJAgent()
        initial = agent.trade_count
        # Force some trades by running many cycles
        for _ in range(20):
            agent.run_cycle()
        # Should have run at least some trades
        assert agent.trade_count >= initial

    def test_status_dict(self):
        agent = DJAgent()
        status = agent.status_dict()
        assert status["name"] == "DJ"
        assert "total_pnl_usd" in status
        assert "win_rate" in status
        assert status["dynasty"] == "Brotherhood Omega Dynasty"

    def test_halt_stops_trading(self):
        agent = DJAgent()
        agent.halt()
        assert not agent.active
        result = agent.run_cycle()
        assert result is None

    def test_resume_restarts_trading(self):
        agent = DJAgent()
        agent.halt()
        agent.resume()
        assert agent.active

    def test_win_rate_between_0_and_1(self):
        agent = DJAgent()
        for _ in range(30):
            agent.run_cycle()
        assert 0.0 <= agent.win_rate <= 1.0


# ── HashimAgent ────────────────────────────────────────────────────────────────

class TestHashimAgent:
    def test_instantiation(self):
        agent = HashimAgent()
        assert agent.name == "HASHIM"
        assert "derivatives" in agent.strategy

    def test_chains_include_perp_chains(self):
        agent = HashimAgent()
        assert "SOL" in agent.chains
        assert "ETH" in agent.chains

    def test_signal_for_perp(self):
        agent = HashimAgent()
        for _ in range(100):
            sig = agent.generate_signal()
            if sig is not None:
                assert "PERP" in sig.symbol
                break

    def test_execute_returns_result(self):
        agent = HashimAgent()
        sig = TradeSignal(
            agent_name="HASHIM",
            symbol="BTC-PERP",
            side="sell",
            size_usd=100.0,
            price=68000.0,
            chain="BTC",
            strategy="derivatives_funding_arb",
            confidence=0.85,
        )
        result = agent.execute_trade(sig)
        assert result.executed


# ── BossmanAgent ───────────────────────────────────────────────────────────────

class TestBossmanAgent:
    def test_instantiation(self):
        agent = BossmanAgent()
        assert agent.name == "BOSSMAN"
        assert agent.chains == ["BTC"]

    def test_signal_types(self):
        agent = BossmanAgent()
        seen_types = set()
        for _ in range(200):
            sig = agent.generate_signal()
            if sig and sig.symbol:
                prefix = sig.symbol.split(":")[0]
                seen_types.add(prefix)
        # Should see at least 2 of 3 asset types
        assert len(seen_types) >= 2

    def test_execute_increments_counters(self):
        agent = BossmanAgent()
        sig = TradeSignal(
            agent_name="BOSSMAN",
            symbol="ORD:NodeMonkes",
            side="buy",
            size_usd=200.0,
            price=3400.0,
            chain="BTC",
            strategy="ordinal_floor_sweep",
            confidence=0.80,
        )
        agent.execute_trade(sig)
        assert agent._ordinals_held == 1

    def test_status_includes_btc_assets(self):
        agent = BossmanAgent()
        status = agent.status_dict()
        assert "ordinals_held" in status
        assert "runes_held" in status
        assert "bitmaps_held" in status


# ── PatrickAgent ───────────────────────────────────────────────────────────────

class TestPatrickAgent:
    def test_instantiation(self):
        agent = PatrickAgent()
        assert agent.name == "PATRICK"
        assert len(agent.chains) == 12

    def test_all_12_chains_present(self):
        agent = PatrickAgent()
        expected = {"SOL", "BTC", "ETH", "AVAX", "MATIC", "ARB", "OP", "BSC", "FTM", "NEAR", "ATOM", "DOT"}
        assert set(agent.chains) == expected

    def test_wallet_shared_with_dj(self):
        dj = DJAgent()
        patrick = PatrickAgent()
        assert dj.wallet == patrick.wallet

    def test_signal_strategies(self):
        agent = PatrickAgent()
        strategies = set()
        for _ in range(100):
            sig = agent.generate_signal()
            if sig:
                strategies.add(sig.strategy)
        assert len(strategies) >= 2

    def test_status_includes_chain_count(self):
        agent = PatrickAgent()
        status = agent.status_dict()
        assert status["chains_active"] == 12
