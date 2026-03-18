"""
OMEGA-ULTIMATE-FUSION-V∞ — Webhook Server
Brotherhood Omega Dynasty

Central webhook receiver for external events:
  - Exchange fill notifications
  - Price alerts from oracles
  - Telegram bot callbacks
  - WhatsApp status updates
  - Monitoring alerts

POST /webhook/trade     — Trade fill notification
POST /webhook/alert     — Price/risk alert
POST /webhook/ping      — Health check
GET  /health            — Server health

Start with: python -m integrations.webhook.server
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "omega-brotherhood-secret")
PORT = int(os.getenv("PORT", "9000"))

_events: list[dict] = []  # in-memory event log (last 1000)
MAX_EVENTS = 1000


class WebhookHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/health", "/"):
            self._json_response(200, {"status": "ok", "dynasty": "Brotherhood Omega Dynasty"})
        elif path == "/events":
            self._json_response(200, {"events": _events[-100:]})
        else:
            self._json_response(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""

        if not self._verify_signature(body):
            self._json_response(401, {"error": "invalid signature"})
            return

        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._json_response(400, {"error": "invalid JSON"})
            return

        if path == "/webhook/trade":
            self._handle_trade(payload)
        elif path == "/webhook/alert":
            self._handle_alert(payload)
        elif path == "/webhook/ping":
            self._json_response(200, {"pong": True})
            return
        else:
            self._json_response(404, {"error": "unknown webhook path"})
            return

        self._json_response(200, {"received": True})

    def _handle_trade(self, payload: dict) -> None:
        event = {
            "type": "trade",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": payload,
        }
        _append_event(event)
        logger.info("📥 Trade webhook: %s", json.dumps(payload)[:200])

    def _handle_alert(self, payload: dict) -> None:
        event = {
            "type": "alert",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": payload,
        }
        _append_event(event)
        level = payload.get("level", "info").upper()
        logger.log(
            logging.ERROR if level == "CRITICAL" else logging.WARNING if level == "WARNING" else logging.INFO,
            "🔔 Alert webhook [%s]: %s",
            level,
            payload.get("message", ""),
        )

    def _verify_signature(self, body: bytes) -> bool:
        sig = self.headers.get("X-Omega-Signature", "")
        if not sig:
            return True  # No sig provided — allow (dev mode)
        expected = "sha256=" + hmac.new(
            WEBHOOK_SECRET.encode(), body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(sig, expected)

    def _json_response(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        logger.debug(fmt, *args)


def _append_event(event: dict) -> None:
    _events.append(event)
    if len(_events) > MAX_EVENTS:
        del _events[0]


def run_server() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    logger.info("🪝 Webhook server listening on :%d", PORT)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
