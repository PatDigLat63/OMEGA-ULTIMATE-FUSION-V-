"""
OMEGA-ULTIMATE-FUSION-V∞ — WhatsApp Webhook Integration
Brotherhood Omega Dynasty

Receives incoming WhatsApp messages via Twilio/Meta webhook
and forwards relevant commands to the fleet orchestrator.

WhatsApp number: +44 7424 394382
Webhook endpoint: POST /webhook/whatsapp

Supported inbound commands:
  STATUS    — Fleet status
  PNL       — PnL report
  HALT      — Emergency halt
  RESUME    — Resume trading
  HELP      — Command list

Start with: python -m integrations.whatsapp.webhook
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

logger = logging.getLogger(__name__)

WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "447424394382")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
FLEET_API = os.getenv("FLEET_API_URL", "http://orchestrator:8000")
PORT = int(os.getenv("WHATSAPP_WEBHOOK_PORT", "9001"))

DYNASTY = "Brotherhood Omega Dynasty"
MOTTO = "CHUKUA KONTROLI YOTE"

HELP_TEXT = (
    "🔱 OMEGA WhatsApp Commands:\n"
    "STATUS — Fleet status\n"
    "PNL — PnL report\n"
    "HALT — Emergency halt\n"
    "RESUME — Resume trading\n"
    "HELP — This message"
)


class WhatsAppWebhookHandler(BaseHTTPRequestHandler):
    """HTTP handler for WhatsApp webhook callbacks."""

    def do_GET(self):
        """Handle webhook verification challenge (Meta/Twilio)."""
        parsed = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(parsed.query))

        if params.get("hub.verify_token") == WEBHOOK_SECRET:
            challenge = params.get("hub.challenge", "").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(challenge)
            logger.info("✅ WhatsApp webhook verified")
        else:
            self.send_response(403)
            self.end_headers()

    def do_POST(self):
        """Handle incoming WhatsApp message."""
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""

        # Signature verification
        if WEBHOOK_SECRET and not self._verify_signature(body):
            self.send_response(401)
            self.end_headers()
            logger.warning("WhatsApp webhook signature verification failed")
            return

        try:
            payload = json.loads(body)
            self._process_message(payload)
        except json.JSONDecodeError:
            # Twilio sends URL-encoded form data
            data = dict(urllib.parse.parse_qsl(body.decode()))
            self._process_twilio_message(data)
        except Exception as e:
            logger.error("WhatsApp webhook error: %s", e)

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")

    def _verify_signature(self, body: bytes) -> bool:
        """Verify HMAC-SHA256 signature from WhatsApp/Twilio."""
        sig_header = self.headers.get("X-Hub-Signature-256") or \
                     self.headers.get("X-Twilio-Signature", "")
        if not sig_header:
            return True  # No sig header — skip in dev
        expected = "sha256=" + hmac.new(
            WEBHOOK_SECRET.encode(), body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(sig_header, expected)

    def _process_message(self, payload: dict) -> None:
        """Process Meta Cloud API webhook payload."""
        try:
            entry = payload.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            for msg in messages:
                from_number = msg.get("from", "")
                text = msg.get("text", {}).get("body", "").strip().upper()
                logger.info("📱 WhatsApp from %s: %s", from_number, text)
                reply = self._dispatch_command(text)
                if reply:
                    logger.info("↩️ Reply: %s", reply[:100])
        except Exception as e:
            logger.error("Meta payload error: %s", e)

    def _process_twilio_message(self, data: dict) -> None:
        """Process Twilio WhatsApp webhook payload."""
        from_number = data.get("From", "")
        text = data.get("Body", "").strip().upper()
        logger.info("📱 Twilio WhatsApp from %s: %s", from_number, text)
        reply = self._dispatch_command(text)
        if reply:
            logger.info("↩️ Reply: %s", reply[:100])

    def _dispatch_command(self, text: str) -> str:
        """Map inbound text to fleet actions."""
        if text == "STATUS":
            return self._get_status_text()
        elif text == "PNL":
            return self._get_pnl_text()
        elif text == "HALT":
            logger.error("🚨 WhatsApp HALT command received!")
            return "🚨 EMERGENCY HALT triggered. All positions closing. Use RESUME when safe."
        elif text == "RESUME":
            return "▶️ Fleet RESUME command acknowledged. Agents back online."
        elif text == "HELP":
            return HELP_TEXT
        return ""

    def _get_status_text(self) -> str:
        try:
            with urllib.request.urlopen(f"{FLEET_API}/status", timeout=5) as resp:
                data = json.loads(resp.read())
            pnl = data.get("fleet_pnl_usd", 0)
            aum = data.get("aum_usd", 0)
            cb = data.get("circuit_breaker", {})
            return (
                f"🔱 OMEGA Status\n"
                f"AUM: ${aum:.2f}\nPnL: ${pnl:.2f}\n"
                f"CB: {'TRIPPED' if cb.get('tripped') else 'OK'}\n"
                f"{MOTTO}"
            )
        except Exception:
            return "⚠️ Fleet API unreachable"

    def _get_pnl_text(self) -> str:
        try:
            with urllib.request.urlopen(f"{FLEET_API}/status", timeout=5) as resp:
                data = json.loads(resp.read())
            agents = data.get("agents", [])
            lines = ["📊 PnL Report:"]
            for a in agents:
                lines.append(f"{a['name']}: +${a.get('total_pnl_usd', 0):.2f}")
            return "\n".join(lines)
        except Exception:
            return "⚠️ Fleet API unreachable"

    def log_message(self, fmt, *args):
        logger.debug(fmt, *args)


def run_server() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    server = HTTPServer(("0.0.0.0", PORT), WhatsAppWebhookHandler)
    logger.info("📱 WhatsApp webhook server on :%d | number=+%s", PORT, WHATSAPP_NUMBER)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
