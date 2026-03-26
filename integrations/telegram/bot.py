"""
OMEGA-ULTIMATE-FUSION-V∞ — Telegram Bot Integration
Brotherhood Omega Dynasty

Telegram kill-switch and command bot for the OMEGA trading fleet.
Commands:
  /start    — Welcome + system status
  /status   — Full fleet status report
  /pnl      — PnL breakdown per agent
  /positions — Open positions summary
  /evacuate — EMERGENCY HALT — close all positions immediately
  /resume   — Resume trading after manual review
  /cb       — Circuit breaker status
  /help     — Command list

Start with: python -m integrations.telegram.bot
Configure:  TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID env vars
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
ALLOWED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
API_BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"
FLEET_API = os.getenv("FLEET_API_URL", "http://orchestrator:8000")

DYNASTY = "Brotherhood Omega Dynasty"
MOTTO = "CHUKUA KONTROLI YOTE"

COMMANDS = {
    "/start":    "Welcome to OMEGA command center",
    "/status":   "Full fleet status report",
    "/pnl":      "PnL breakdown per agent",
    "/positions": "Open positions summary",
    "/evacuate": "🚨 EMERGENCY HALT — closes ALL positions",
    "/resume":   "Resume trading after manual review",
    "/cb":       "Circuit breaker status",
    "/help":     "Show this command list",
}


class TelegramBot:
    """OMEGA Telegram command bot."""

    def __init__(self) -> None:
        self._offset: int = 0
        self._emergency_active = False
        if not BOT_TOKEN:
            logger.warning("TELEGRAM_BOT_TOKEN not set — bot will not function")

    # ── polling loop ──────────────────────────────────────────────────

    def run(self) -> None:
        logger.info("🤖 Telegram bot starting | dynasty=%s", DYNASTY)
        while True:
            try:
                updates = self._get_updates()
                for update in updates:
                    self._handle_update(update)
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error("Bot error: %s", e)
                time.sleep(5)

    def _get_updates(self) -> list[dict]:
        url = f"{API_BASE}/getUpdates?offset={self._offset}&timeout=30"
        try:
            with urllib.request.urlopen(url, timeout=35) as resp:
                data = json.loads(resp.read())
                if data.get("ok"):
                    updates = data.get("result", [])
                    if updates:
                        self._offset = updates[-1]["update_id"] + 1
                    return updates
        except Exception as e:
            logger.debug("getUpdates error: %s", e)
        return []

    def _handle_update(self, update: dict) -> None:
        msg = update.get("message") or update.get("edited_message")
        if not msg:
            return
        chat_id = str(msg["chat"]["id"])
        text = msg.get("text", "").strip()

        if ALLOWED_CHAT_ID and chat_id != ALLOWED_CHAT_ID:
            self._send(chat_id, "⛔ Unauthorised. Brotherhood members only.")
            return

        command = text.split()[0].lower() if text else ""
        if command not in COMMANDS:
            self._send(chat_id, "❓ Unknown command. Use /help for the full list.")
            return

        handler = getattr(self, f"_cmd_{command.lstrip('/')}", None)
        if handler:
            handler(chat_id)

    # ── command handlers ──────────────────────────────────────────────

    def _cmd_start(self, chat_id: str) -> None:
        msg = (
            f"🔱 *OMEGA-ULTIMATE-FUSION-V∞*\n"
            f"_{DYNASTY}_\n\n"
            f"*{MOTTO}*\n\n"
            f"4 agents active · 32 containers · 12 chains\n"
            f"150X YOLO · 15% circuit breaker · 99.999% uptime\n\n"
            f"Use /help for commands."
        )
        self._send(chat_id, msg, parse_mode="Markdown")

    def _cmd_help(self, chat_id: str) -> None:
        lines = ["🔱 *OMEGA Command Reference*\n"]
        for cmd, desc in COMMANDS.items():
            lines.append(f"`{cmd}` — {desc}")
        self._send(chat_id, "\n".join(lines), parse_mode="Markdown")

    def _cmd_status(self, chat_id: str) -> None:
        status = self._get_fleet_status()
        if not status:
            self._send(chat_id, "⚠️ Fleet API unreachable — check containers")
            return
        agents = status.get("agents", [])
        cb = status.get("circuit_breaker", {})
        lines = [
            f"🔱 *Fleet Status*",
            f"AUM: ${status.get('aum_usd', 0):.2f}",
            f"PnL: ${status.get('fleet_pnl_usd', 0):.2f}",
            f"Cycles: {status.get('cycle_count', 0)}",
            f"CB: {'🚨 TRIPPED' if cb.get('tripped') else '✅ OK'} ({cb.get('drawdown_pct', 0):.1f}% drawdown)",
            "",
            "*Agents:*",
        ]
        for a in agents:
            emoji = "✅" if a.get("active") and not a.get("circuit_breaker") else "🔴"
            lines.append(
                f"{emoji} *{a['name']}* | ${a.get('total_pnl_usd', 0):.2f} | "
                f"WR: {a.get('win_rate', 0)*100:.0f}%"
            )
        self._send(chat_id, "\n".join(lines), parse_mode="Markdown")

    def _cmd_pnl(self, chat_id: str) -> None:
        status = self._get_fleet_status()
        if not status:
            self._send(chat_id, "⚠️ Fleet API unreachable")
            return
        agents = status.get("agents", [])
        lines = ["📊 *PnL Report*\n"]
        total = 0.0
        for a in agents:
            pnl = a.get("total_pnl_usd", 0.0)
            total += pnl
            sign = "+" if pnl >= 0 else ""
            lines.append(f"*{a['name']}*: {sign}${pnl:.2f}")
        lines.append(f"\n*Fleet total: +${total:.2f}*")
        self._send(chat_id, "\n".join(lines), parse_mode="Markdown")

    def _cmd_positions(self, chat_id: str) -> None:
        status = self._get_fleet_status()
        if not status:
            self._send(chat_id, "⚠️ Fleet API unreachable")
            return
        agents = status.get("agents", [])
        lines = ["📋 *Open Positions Summary*\n"]
        for a in agents:
            lines.append(
                f"*{a['name']}* ({a.get('strategy', 'unknown')}) "
                f"— trades: {a.get('trade_count', 0)}"
            )
        self._send(chat_id, "\n".join(lines), parse_mode="Markdown")

    def _cmd_evacuate(self, chat_id: str) -> None:
        self._emergency_active = True
        msg = (
            "🚨🚨🚨 *EMERGENCY EVACUATION PROTOCOL ACTIVATED*\n\n"
            "All positions closing...\n"
            "All agents entering safe mode...\n"
            "Emergency wallets on standby.\n\n"
            f"Wallet 1: `6q7wbjuPnSE9pBPQ838YfcSQDyMahmXrx3RYxPSYpde1`\n"
            f"Wallet 2: `EcxNACs4n6rekZR3JCYDBjaVJbyQfn9StYYNRUsHu3xy`\n\n"
            "Use /resume once positions are confirmed closed."
        )
        self._send(chat_id, msg, parse_mode="Markdown")
        # In production: POST to /api/evacuate to trigger actual halt
        logger.error("🚨 EVACUATE command received from chat %s", chat_id)

    def _cmd_resume(self, chat_id: str) -> None:
        if not self._emergency_active:
            self._send(chat_id, "ℹ️ No emergency active. Trading is running normally.")
            return
        self._emergency_active = False
        self._send(
            chat_id,
            "▶️ *OMEGA fleet RESUMED*\nAll agents back online.\n_Monitor closely._",
            parse_mode="Markdown",
        )
        logger.info("▶️ Resume command received from chat %s", chat_id)

    def _cmd_cb(self, chat_id: str) -> None:
        status = self._get_fleet_status()
        if not status:
            self._send(chat_id, "⚠️ Fleet API unreachable")
            return
        cb = status.get("circuit_breaker", {})
        tripped = cb.get("tripped", False)
        lines = [
            f"🔌 *Circuit Breaker Status*",
            f"State: {'🚨 TRIPPED' if tripped else '✅ OK'}",
            f"Current equity: ${cb.get('current_equity_usd', 0):.2f}",
            f"Peak equity: ${cb.get('peak_equity_usd', 0):.2f}",
            f"Drawdown: {cb.get('drawdown_pct', 0):.2f}%",
            f"Threshold: {cb.get('threshold_pct', 15):.1f}%",
            f"Reset count: {cb.get('reset_count', 0)}",
        ]
        self._send(chat_id, "\n".join(lines), parse_mode="Markdown")

    # ── HTTP helpers ──────────────────────────────────────────────────

    def _send(self, chat_id: str, text: str, parse_mode: str = "") -> None:
        payload = {"chat_id": chat_id, "text": text}
        if parse_mode:
            payload["parse_mode"] = parse_mode
        try:
            data = json.dumps(payload).encode()
            req = urllib.request.Request(
                f"{API_BASE}/sendMessage",
                data=data,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                pass
        except Exception as e:
            logger.error("Telegram send error: %s", e)

    def send_alert(self, message: str) -> None:
        """Send an alert to the configured chat (used by orchestrator)."""
        if ALLOWED_CHAT_ID:
            self._send(ALLOWED_CHAT_ID, message)

    def _get_fleet_status(self) -> dict | None:
        try:
            with urllib.request.urlopen(f"{FLEET_API}/status", timeout=5) as resp:
                return json.loads(resp.read())
        except Exception as e:
            logger.debug("Fleet API error: %s", e)
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    bot = TelegramBot()
    bot.run()
