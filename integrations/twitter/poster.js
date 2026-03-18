/**
 * OMEGA-ULTIMATE-FUSION-V∞ — X (Twitter) Auto-Poster
 * Brotherhood Omega Dynasty · @patrickdl44
 * Posts daily profits, YOLO events, dynasty announcements
 */

'use strict';

// ── NOTE ─────────────────────────────────────────────────────────
// This module uses the Twitter API v2. Requires Elevated access.
// All API credentials must be set via environment variables.
// See CONFIG.md for setup instructions.

const https = require('https');
const crypto = require('crypto');

const CONSUMER_KEY    = process.env.TWITTER_API_KEY    || '';
const CONSUMER_SECRET = process.env.TWITTER_API_SECRET || '';
const ACCESS_TOKEN    = process.env.TWITTER_ACCESS_TOKEN  || '';
const ACCESS_SECRET   = process.env.TWITTER_ACCESS_SECRET || '';

const HASHTAGS = '#OmegaDynasty #Brotherhood #SolanaTrading #AutoTrading';

// ── OAUTH 1.0a SIGNING ───────────────────────────────────────────
function oauthSign(method, url, params) {
  const ts    = Math.floor(Date.now() / 1000).toString();
  const nonce = crypto.randomBytes(16).toString('hex');

  const oauthParams = {
    oauth_consumer_key:     CONSUMER_KEY,
    oauth_nonce:            nonce,
    oauth_signature_method: 'HMAC-SHA1',
    oauth_timestamp:        ts,
    oauth_token:            ACCESS_TOKEN,
    oauth_version:          '1.0',
    ...params,
  };

  const sortedKeys = Object.keys(oauthParams).sort();
  const paramStr = sortedKeys
    .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(oauthParams[k])}`)
    .join('&');

  const baseStr = [
    method.toUpperCase(),
    encodeURIComponent(url),
    encodeURIComponent(paramStr),
  ].join('&');

  const sigKey = `${encodeURIComponent(CONSUMER_SECRET)}&${encodeURIComponent(ACCESS_SECRET)}`;
  const sig = crypto.createHmac('sha1', sigKey).update(baseStr).digest('base64');

  oauthParams.oauth_signature = sig;

  const header = 'OAuth ' + Object.keys(oauthParams)
    .filter(k => k.startsWith('oauth_'))
    .sort()
    .map(k => `${encodeURIComponent(k)}="${encodeURIComponent(oauthParams[k])}"`)
    .join(', ');

  return header;
}

// ── POST TWEET ───────────────────────────────────────────────────
// NOTE: X API v2 /2/tweets supports OAuth 1.0a (user context) for posting.
// If switching to OAuth 2.0 (app-only), use Bearer token and update headers.
function postTweet(text) {
  if (!CONSUMER_KEY || !ACCESS_TOKEN) {
    console.log('[TWITTER] Credentials not set — skipping post');
    return Promise.resolve({ skipped: true });
  }

  const url  = 'https://api.twitter.com/2/tweets';
  const body = JSON.stringify({ text: text.slice(0, 280) });
  const auth = oauthSign('POST', url, {});

  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.twitter.com',
      path: '/2/tweets',
      method: 'POST',
      headers: {
        'Authorization':  auth,
        'Content-Type':   'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };
    const req = https.request(options, res => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        console.log(`[TWITTER] Post result: ${res.statusCode}`);
        resolve(JSON.parse(data));
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ── TEMPLATES ────────────────────────────────────────────────────
function dailyProfitPost(profit, total, pct, trades, winRate) {
  return `🔱 OMEGA DYNASTY DAILY UPDATE\n\n💰 Today: +£${profit.toFixed(2)}\n📊 Total: £${total.toFixed(2)} / £16,670 (${pct.toFixed(1)}%)\n🎯 ${trades} trades | ${winRate.toFixed(1)}% win rate\n🤖 4/4 agents ACTIVE\n\nCHUKUA KONTROLI YOTE 🔱\n\n${HASHTAGS}`;
}

function yoloPost(pair, leverage) {
  return `⚡ YOLO MODE ENGAGED\n\n${leverage}X LEVERAGE · ALL IN\nSignal: ${pair} momentum\n\nThe dynasty plays to WIN 🔱\n\n#YOLO #OmegaDynasty #Solana`;
}

function milestonePost(amount) {
  return `💰 DYNASTY MILESTONE: £${amount.toLocaleString()} EARNED\n\nProgress: ${((amount / 16670) * 100).toFixed(1)}% to financial freedom\n24/7 compound machine running 🔱\n\n${HASHTAGS}`;
}

function dynastyAnnouncement(message) {
  return `🔱 OMEGA DYNASTY ANNOUNCEMENT\n\n${message}\n\nCHUKUA KONTROLI YOTE\n\n${HASHTAGS}`;
}

module.exports = {
  postTweet,
  dailyProfitPost,
  yoloPost,
  milestonePost,
  dynastyAnnouncement,
};
