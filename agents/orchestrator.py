"""
OMEGA-ULTIMATE-FUSION-V∞ — Orchestrator
Brotherhood Omega Dynasty

The brain of the Brotherhood trading fleet.
Coordinates all 4 agents, manages circuit breaker,
integrates Telegram/WhatsApp/X notifications,
and exposes a health/status HTTP API.

Start with: python -m agents.orchestrator
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
import json

from agents.bossman_agent import BossmanAgent
from agents.circuit_breaker import CircuitBreaker
from agents.dj_agent import DJAgent
from agents.hashim_agent import HashimAgent
from agents.patrick_agent import PatrickAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

INITIAL_AUM = float(os.getenv("INITIAL_EQUITY_USD", "3570"))
CYCLE_INTERVAL = int(os.getenv("CYCLE_INTERVAL_SECONDS", "30"))
API_PORT = int(os.getenv("API_PORT", "8000"))


class Orchestrator:
    """
    🔱 OMEGA Orchestrator — coordinates all 4 Brotherhood agents.
    Implements 150X YOLO factor and 15% fleet-wide circuit breaker.
    """

    MOTTO = "CHUKUA KONTROLI YOTE"

    def __init__(self) -> None:
        self.agents = [
            DJAgent(),
            HashimAgent(),
            BossmanAgent(),
            PatrickAgent(),
        ]
        self.circuit_breaker = CircuitBreaker(
            initial_equity=INITIAL_AUM,
            on_trip=self._emergency_halt,
            on_reset=self._broadcast_resume,
        )
        self.running = False
        self.cycle_count = 0
        self.start_time = datetime.now(timezone.utc)
        logger.info("🔱 OMEGA Orchestrator initialised | agents=%d | aum=$%.2f", len(self.agents), INITIAL_AUM)
        logger.info("🔱 %s", self.MOTTO)

    def start(self) -> None:
        """Start the orchestrator — runs forever."""
        self.running = True
        logger.info("▶️ OMEGA trading fleet ONLINE")
        self._start_api_server()
        self._main_loop()

    def _main_loop(self) -> None:
        while self.running:
            cycle_start = time.monotonic()
            self.cycle_count += 1
            logger.info("🔄 Cycle %d starting...", self.cycle_count)

            if self.circuit_breaker.is_tripped:
                logger.warning("⚠️ Circuit breaker active — halting all trades")
                time.sleep(CYCLE_INTERVAL)
                continue

            total_pnl = 0.0
            for agent in self.agents:
                try:
                    result = agent.run_cycle()
                    if result:
                        total_pnl += result.pnl_usd
                except Exception as e:
                    logger.error("Agent %s cycle error: %s", agent.name, e)

            # Update fleet-wide circuit breaker
            combined_equity = INITIAL_AUM + sum(a.total_pnl for a in self.agents)
            self.circuit_breaker.update(combined_equity)

            elapsed = time.monotonic() - cycle_start
            sleep_time = max(0, CYCLE_INTERVAL - elapsed)
            logger.info(
                "✅ Cycle %d complete | fleet_pnl=$%.2f | equity=$%.2f | sleep=%.1fs",
                self.cycle_count, total_pnl, combined_equity, sleep_time,
            )
            time.sleep(sleep_time)

    def _emergency_halt(self) -> None:
        """Halt all agents when circuit breaker trips."""
        logger.error("🚨 EMERGENCY HALT — halting all agents")
        for agent in self.agents:
            agent.halt()
        # In production: send Telegram /evacuate, WhatsApp alert, X post

    def _broadcast_resume(self) -> None:
        logger.info("▶️ Circuit breaker reset — resuming agents")
        for agent in self.agents:
            agent.resume()

    def fleet_status(self) -> dict:
        return {
            "dynasty": "Brotherhood Omega Dynasty",
            "motto": self.MOTTO,
            "uptime_seconds": round((datetime.now(timezone.utc) - self.start_time).total_seconds()),
            "cycle_count": self.cycle_count,
            "running": self.running,
            "circuit_breaker": self.circuit_breaker.status(),
            "agents": [a.status_dict() for a in self.agents],
            "fleet_pnl_usd": round(sum(a.total_pnl for a in self.agents), 2),
            "aum_usd": round(INITIAL_AUM + sum(a.total_pnl for a in self.agents), 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def _start_api_server(self) -> None:
        orchestrator = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path in ("/health", "/"):
                    data = json.dumps({"status": "ok", "dynasty": "Brotherhood Omega Dynasty"})
                elif self.path == "/status":
                    data = json.dumps(orchestrator.fleet_status(), indent=2)
                else:
                    self.send_response(404)
                    self.end_headers()
                    return
                body = data.encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", len(body))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, fmt, *args):
                pass  # suppress default access logging

        server = HTTPServer(("0.0.0.0", API_PORT), Handler)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        logger.info("🌐 Status API listening on :%d", API_PORT)


if __name__ == "__main__":
    orch = Orchestrator()
    orch.start()
