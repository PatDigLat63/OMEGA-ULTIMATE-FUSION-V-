"""
OMEGA-ULTIMATE-FUSION-V∞ — Integration Test Suite
Tests for Telegram bot, WhatsApp webhook, Twitter bot, webhook server.
"""

import json
import os
import pytest
import io
from unittest.mock import MagicMock, patch


# ── Telegram Bot ──────────────────────────────────────────────────────────────

class TestTelegramBot:
    def test_instantiation(self):
        from integrations.telegram.bot import TelegramBot
        bot = TelegramBot()
        assert bot._offset == 0
        assert not bot._emergency_active

    def test_cmd_start_sends_message(self):
        from integrations.telegram.bot import TelegramBot
        bot = TelegramBot()
        with patch.object(bot, "_send") as mock_send:
            bot._cmd_start("12345")
            mock_send.assert_called_once()
            args = mock_send.call_args[0]
            assert "OMEGA" in args[1]

    def test_cmd_help_lists_all_commands(self):
        from integrations.telegram.bot import TelegramBot, COMMANDS
        bot = TelegramBot()
        with patch.object(bot, "_send") as mock_send:
            bot._cmd_help("12345")
            text = mock_send.call_args[0][1]
            for cmd in COMMANDS:
                assert cmd in text

    def test_cmd_evacuate_sets_emergency_flag(self):
        from integrations.telegram.bot import TelegramBot
        bot = TelegramBot()
        with patch.object(bot, "_send"):
            bot._cmd_evacuate("12345")
        assert bot._emergency_active

    def test_cmd_resume_clears_emergency_flag(self):
        from integrations.telegram.bot import TelegramBot
        bot = TelegramBot()
        bot._emergency_active = True
        with patch.object(bot, "_send"):
            bot._cmd_resume("12345")
        assert not bot._emergency_active

    def test_unauthorized_chat_rejected(self):
        os.environ["TELEGRAM_CHAT_ID"] = "99999"
        from importlib import reload
        import integrations.telegram.bot as tb_module
        reload(tb_module)
        bot = tb_module.TelegramBot()
        with patch.object(bot, "_send") as mock_send:
            bot._handle_update({
                "message": {
                    "chat": {"id": "wrong_id"},
                    "text": "/status"
                }
            })
            text = mock_send.call_args[0][1]
            assert "Unauthorised" in text or "Brotherhood" in text
        del os.environ["TELEGRAM_CHAT_ID"]

    def test_unknown_command_triggers_help_suggestion(self):
        from integrations.telegram.bot import TelegramBot
        bot = TelegramBot()
        with patch.object(bot, "_send") as mock_send:
            bot._handle_update({
                "message": {"chat": {"id": "123"}, "text": "/unknown"}
            })
            text = mock_send.call_args[0][1]
            assert "/help" in text.lower() or "unknown" in text.lower()

    def test_send_alert_targets_configured_chat(self):
        os.environ["TELEGRAM_CHAT_ID"] = "42"
        from importlib import reload
        import integrations.telegram.bot as tb_module
        reload(tb_module)
        bot = tb_module.TelegramBot()
        with patch.object(bot, "_send") as mock_send:
            bot.send_alert("test alert")
            mock_send.assert_called_once_with("42", "test alert")
        del os.environ["TELEGRAM_CHAT_ID"]


# ── WhatsApp Webhook ──────────────────────────────────────────────────────────

class TestWhatsAppWebhook:
    def _make_handler(self, path, body, method="POST", headers=None):
        """Create a WhatsAppWebhookHandler for testing without a real socket."""
        from integrations.whatsapp.webhook import WhatsAppWebhookHandler
        handler = WhatsAppWebhookHandler.__new__(WhatsAppWebhookHandler)
        handler.path = path
        handler.headers = headers or {}
        handler._body = body
        handler._responses = []
        return handler

    def test_help_command(self):
        from integrations.whatsapp.webhook import WhatsAppWebhookHandler
        handler = WhatsAppWebhookHandler.__new__(WhatsAppWebhookHandler)
        result = handler._dispatch_command("HELP")
        assert "STATUS" in result
        assert "HALT" in result

    def test_halt_command(self):
        from integrations.whatsapp.webhook import WhatsAppWebhookHandler
        handler = WhatsAppWebhookHandler.__new__(WhatsAppWebhookHandler)
        result = handler._dispatch_command("HALT")
        assert "HALT" in result.upper() or "EMERGENCY" in result.upper()

    def test_resume_command(self):
        from integrations.whatsapp.webhook import WhatsAppWebhookHandler
        handler = WhatsAppWebhookHandler.__new__(WhatsAppWebhookHandler)
        result = handler._dispatch_command("RESUME")
        assert "RESUME" in result.upper() or "FLEET" in result.upper()

    def test_unknown_command_returns_empty(self):
        from integrations.whatsapp.webhook import WhatsAppWebhookHandler
        handler = WhatsAppWebhookHandler.__new__(WhatsAppWebhookHandler)
        result = handler._dispatch_command("INVALID")
        assert result == ""

    def test_signature_verification_no_header(self):
        from integrations.whatsapp.webhook import WhatsAppWebhookHandler
        handler = WhatsAppWebhookHandler.__new__(WhatsAppWebhookHandler)
        handler.headers = {}
        assert handler._verify_signature(b"test")


# ── Twitter Bot ───────────────────────────────────────────────────────────────

class TestTwitterBot:
    def test_instantiation(self):
        from integrations.twitter.bot import TwitterBot
        bot = TwitterBot()
        assert bot._last_post_time == 0.0

    def test_render_template(self):
        from integrations.twitter.bot import TwitterBot
        bot = TwitterBot()
        text = bot._render("alive")
        assert "OMEGA" in text
        assert "CHUKUA KONTROLI YOTE" in text
        assert "#OMEGA" in text

    def test_dry_run_when_no_credentials(self):
        from integrations.twitter.bot import TwitterBot
        bot = TwitterBot()
        # Credentials not set — should succeed as dry run
        result = bot._post("Test tweet from OMEGA")
        assert result is True

    def test_render_pnl_milestone(self):
        from integrations.twitter.bot import TwitterBot
        bot = TwitterBot()
        text = bot._render("pnl_milestone", pnl=500.0, aum=4000.0)
        assert "500" in text
        assert "4000" in text

    def test_render_emergency(self):
        from integrations.twitter.bot import TwitterBot
        bot = TwitterBot()
        text = bot._render("emergency")
        assert "EMERGENCY" in text.upper()

    def test_tweet_max_280_chars(self):
        from integrations.twitter.bot import TwitterBot
        bot = TwitterBot()
        for template_key in ["alive", "emergency"]:
            text = bot._render(template_key)
            assert len(text) <= 280, f"{template_key} template too long: {len(text)}"


# ── Webhook Server ────────────────────────────────────────────────────────────

class TestWebhookServer:
    def _make_request(self, path, method="GET", body=b"", headers=None, secret=""):
        """Simulate an HTTP request to the webhook handler."""
        from integrations.webhook.server import WebhookHandler, WEBHOOK_SECRET
        import io

        class FakeSocket:
            def makefile(self, mode):
                return io.BytesIO(body)

        handler = WebhookHandler.__new__(WebhookHandler)
        handler.path = path
        handler.headers = headers or {}
        handler.rfile = io.BytesIO(body)
        handler._response_status = None
        handler._response_headers = {}
        handler._response_body = b""

        def send_response(code):
            handler._response_status = code

        def send_header(k, v):
            handler._response_headers[k] = v

        def end_headers():
            pass

        wfile = io.BytesIO()
        handler.send_response = send_response
        handler.send_header = send_header
        handler.end_headers = end_headers
        handler.wfile = wfile
        return handler

    def test_health_endpoint(self):
        from integrations.webhook.server import WebhookHandler
        handler = self._make_request("/health")
        handler.do_GET()
        assert handler._response_status == 200

    def test_unknown_get_returns_404(self):
        from integrations.webhook.server import WebhookHandler
        handler = self._make_request("/unknown")
        handler.do_GET()
        assert handler._response_status == 404

    def test_trade_webhook_appends_event(self):
        from integrations.webhook import server as ws
        ws._events.clear()
        from integrations.webhook.server import WebhookHandler
        body = json.dumps({"symbol": "SOL/USDC", "pnl": 12.5}).encode()
        handler = self._make_request("/webhook/trade", body=body, headers={"Content-Length": str(len(body))})
        handler._verify_signature = lambda b: True  # bypass sig check
        handler.do_POST()
        assert handler._response_status == 200
        assert len(ws._events) == 1
        assert ws._events[0]["type"] == "trade"

    def test_alert_webhook(self):
        from integrations.webhook import server as ws
        ws._events.clear()
        body = json.dumps({"level": "WARNING", "message": "circuit breaker at 12%"}).encode()
        handler = self._make_request("/webhook/alert", body=body, headers={"Content-Length": str(len(body))})
        handler._verify_signature = lambda b: True
        handler.do_POST()
        assert handler._response_status == 200
        assert ws._events[0]["type"] == "alert"

    def test_event_log_max_1000(self):
        from integrations.webhook import server as ws
        ws._events.clear()
        for i in range(1100):
            ws._append_event({"type": "trade", "timestamp": "now", "data": {}})
        assert len(ws._events) <= 1000
