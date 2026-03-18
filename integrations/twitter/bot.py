"""
OMEGA-ULTIMATE-FUSION-V∞ — X (Twitter) Bot Integration
Brotherhood Omega Dynasty

Auto-posts dynasty updates, trade alerts, and PnL reports
to @patrickdl44 on X (Twitter).

Features:
  - Scheduled dynasty announcements
  - PnL milestone posts (every $100 profit)
  - Emergency alerts
  - Manual post trigger via CLI

Start with: python -m integrations.twitter.bot
Configure:  TWITTER_* env vars (OAuth 2.0 PKCE or OAuth 1.0a)
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
import urllib.error
from base64 import b64encode
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

TWITTER_HANDLE = "@patrickdl44"
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
API_KEY = os.getenv("TWITTER_API_KEY", "")
API_SECRET = os.getenv("TWITTER_API_SECRET", "")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET", "")
FLEET_API = os.getenv("FLEET_API_URL", "http://orchestrator:8000")

DYNASTY = "Brotherhood Omega Dynasty"
MOTTO = "CHUKUA KONTROLI YOTE"
HASHTAGS = "#OMEGA #BrotherhoodDynasty #Web3 #DeFi #Crypto"

TWEET_TEMPLATES = {
    "alive": "🔱 OMEGA-ULTIMATE-FUSION-V∞ is LIVE.\n4 agents trading. 12 chains. 150X YOLO.\n{motto}\n{tags}",
    "pnl_milestone": "📊 Fleet PnL milestone: +${pnl:.0f}\nAUM: ${aum:.0f} | Agents: DJ·HASHIM·BOSSMAN·PATRICK\n{motto}\n{tags}",
    "emergency": "🚨 OMEGA EMERGENCY PROTOCOL ACTIVE\nAll positions closing. Brotherhood safe mode engaged.\n{tags}",
    "daily_report": "📈 Daily OMEGA Report [{date}]\nFleet PnL: +${pnl:.2f}\nTrades: {trades} | Win Rate: {wr:.0f}%\n{motto}\n{tags}",
    "circuit_breaker": "⚠️ Circuit breaker engaged at {drawdown:.1f}% drawdown.\nBrotherhood safety systems ACTIVE. Protecting the dynasty.\n{tags}",
}


class TwitterBot:
    """Posts dynasty updates to @patrickdl44."""

    POST_INTERVAL = 3600  # 1-hour minimum between posts
    PNL_MILESTONE_INCREMENT = 100.0  # post every $100 profit

    def __init__(self) -> None:
        self._last_post_time: float = 0.0
        self._last_pnl_milestone: float = 0.0
        if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
            logger.warning("Twitter credentials not fully configured — posting disabled")

    def run(self) -> None:
        """Main loop — posts periodic updates."""
        logger.info("🐦 Twitter bot starting | handle=%s", TWITTER_HANDLE)
        self._post(self._render("alive"))
        while True:
            try:
                self._check_milestones()
                time.sleep(60)
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error("Twitter bot error: %s", e)
                time.sleep(30)

    def _check_milestones(self) -> None:
        status = self._get_fleet_status()
        if not status:
            return
        pnl = status.get("fleet_pnl_usd", 0.0)
        aum = status.get("aum_usd", 3570.0)

        # PnL milestone post
        if pnl >= self._last_pnl_milestone + self.PNL_MILESTONE_INCREMENT:
            self._last_pnl_milestone = (pnl // self.PNL_MILESTONE_INCREMENT) * self.PNL_MILESTONE_INCREMENT
            self._post(self._render("pnl_milestone", pnl=pnl, aum=aum))

    def post_alert(self, message: str) -> bool:
        """Post an emergency or important alert immediately."""
        return self._post(message)

    def post_daily_report(self, pnl: float, trades: int, win_rate: float) -> bool:
        text = self._render(
            "daily_report",
            date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            pnl=pnl,
            trades=trades,
            wr=win_rate * 100,
        )
        return self._post(text)

    def post_emergency(self) -> bool:
        return self._post(self._render("emergency"))

    def post_circuit_breaker(self, drawdown_pct: float) -> bool:
        return self._post(self._render("circuit_breaker", drawdown=drawdown_pct))

    # ── private helpers ───────────────────────────────────────────────

    def _render(self, template_key: str, **kwargs) -> str:
        template = TWEET_TEMPLATES[template_key]
        return template.format(motto=MOTTO, tags=HASHTAGS, **kwargs)

    def _post(self, text: str) -> bool:
        """Post a tweet via Twitter API v2."""
        if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET]):
            logger.info("📝 [DRY RUN] Tweet: %s", text[:100])
            return True

        # Rate-limit guard
        now = time.monotonic()
        if now - self._last_post_time < self.POST_INTERVAL:
            logger.debug("Rate limit — skipping tweet")
            return False

        try:
            payload = json.dumps({"text": text[:280]}).encode()
            # OAuth 1.0a — simplified (production: use tweepy)
            auth_header = self._build_auth_header("POST", "https://api.twitter.com/2/tweets")
            req = urllib.request.Request(
                "https://api.twitter.com/2/tweets",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": auth_header,
                },
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read())
                tweet_id = result.get("data", {}).get("id", "?")
                logger.info("✅ Tweet posted | id=%s | handle=%s", tweet_id, TWITTER_HANDLE)
                self._last_post_time = now
                return True
        except urllib.error.HTTPError as e:
            logger.error("Twitter API error: %d %s", e.code, e.read().decode()[:200])
        except Exception as e:
            logger.error("Tweet failed: %s", e)
        return False

    def _build_auth_header(self, method: str, url: str) -> str:
        """Build OAuth 1.0a Authorization header (simplified)."""
        import hashlib, hmac, time, uuid
        ts = str(int(time.time()))
        nonce = uuid.uuid4().hex
        params = {
            "oauth_consumer_key": API_KEY,
            "oauth_nonce": nonce,
            "oauth_signature_method": "HMAC-SHA256",
            "oauth_timestamp": ts,
            "oauth_token": ACCESS_TOKEN,
            "oauth_version": "1.0",
        }
        param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        base_str = f"{method}&{urllib.parse.quote(url, safe='')}&{urllib.parse.quote(param_str, safe='')}"
        signing_key = f"{urllib.parse.quote(API_SECRET, safe='')}&{urllib.parse.quote(ACCESS_SECRET, safe='')}"
        sig = b64encode(
            hmac.new(signing_key.encode(), base_str.encode(), hashlib.sha256).digest()
        ).decode()
        params["oauth_signature"] = sig
        return "OAuth " + ", ".join(
            f'{k}="{urllib.parse.quote(str(v), safe="")}"'
            for k, v in sorted(params.items())
        )

    def _get_fleet_status(self) -> dict | None:
        try:
            with urllib.request.urlopen(f"{FLEET_API}/status", timeout=5) as resp:
                return json.loads(resp.read())
        except Exception:
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    bot = TwitterBot()
    bot.run()
