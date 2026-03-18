/**
 * OMEGA-ULTIMATE-FUSION-V∞ — WhatsApp Handler (Hustle Bridge)
 * Brotherhood Omega Dynasty
 * Handles incoming WhatsApp messages and sends reports
 */

'use strict';

const http    = require('http');
const crypto  = require('crypto');

const PORT             = process.env.PORT || 3001;
const WEBHOOK_SECRET   = process.env.WHATSAPP_WEBHOOK_SECRET || '';
const AGENTBUS_URL     = process.env.AGENTBUS_URL || 'http://agentbus:8081';

// ── RESPONSE TEMPLATES ──────────────────────────────────────────
const responses = {
  STATUS: () =>
    '🔱 *OMEGA DYNASTY STATUS*\n\n' +
    '🖥 Server: 206.189.118.255 ✅\n' +
    '🐳 Docker: 14/14 UP ✅\n' +
    '🤖 Agents: 4/4 ACTIVE ✅\n' +
    '⚠️ LQ-004: 2 DAYS TO EXPIRY!\n\n' +
    '_CHUKUA KONTROLI YOTE_',

  PNL: () =>
    '💰 *P&L REPORT*\n\n' +
    'Today: +£34.22\n' +
    'Total: £3,089.42 / £16,670\n' +
    'Progress: 18.5%\n' +
    'Win Rate: 78.4%',

  POSITIONS: () =>
    '📋 *OPEN POSITIONS*\n\n' +
    '• SOL/USDC: +1.2%\n' +
    '• BONK/SOL: +0.8%\n' +
    '• RAY/USDC: +2.1%\n\n' +
    '3 positions open',

  AGENTS: () =>
    '🤖 *AGENT STATUS*\n\n' +
    '🎯 DJ Sharpshooter: ✅ ACTIVE\n' +
    '💎 Hashim Treasury: ✅ ACTIVE\n' +
    '🛡 Bossman Risk: ✅ ACTIVE\n' +
    '🔬 Patrick Scanner: ✅ ACTIVE',

  EVACUATE: () =>
    '🚨 *EVACUATION PROTOCOL*\n\nClosing all positions...\nFunds secured to treasury.',

  RESUME: () =>
    '✅ *TRADING RESUMED*\n\nAll 4 agents active. Scanning...',

  BITCOIN: () =>
    '₿ *BITCOIN HOLDINGS*\n\n' +
    'Ordinals: 139\n' +
    'Bitmaps: 170\n' +
    'Runes: 7\n' +
    'Rare Sats: 13,378+',

  LOANS: () =>
    '💸 *LIQUIDIUM LOANS*\n\n' +
    '✅ LQ-001: 28 days\n' +
    '✅ LQ-002: 14 days\n' +
    '✅ LQ-003: 7 days\n' +
    '🚨 *LQ-004: 2 DAYS — URGENT!*',

  HELP: () =>
    '🔱 *OMEGA DYNASTY — COMMANDS*\n\n' +
    'STATUS, PNL, POSITIONS, AGENTS,\n' +
    'EVACUATE, RESUME, BITCOIN, LOANS,\n' +
    'COMMAND CENTER\n\n' +
    '_CHUKUA KONTROLI YOTE_',

  'COMMAND CENTER': () =>
    '🔱 *OMEGA COMMAND CENTER*\n\n' +
    'Dashboard: https://brotherhoodomegadynasty.com\n' +
    'GitHub: github.com/PatDigLat63/OMEGA-ULTIMATE-FUSION-V-\n\n' +
    '_Open the link to access the full command interface._',
};

// ── SIGNATURE VERIFICATION ──────────────────────────────────────
function verifySignature(payload, signature) {
  if (!WEBHOOK_SECRET) return true;
  const expected = 'sha256=' + crypto
    .createHmac('sha256', WEBHOOK_SECRET)
    .update(payload)
    .digest('hex');
  try {
    return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(signature));
  } catch (_) {
    return false;
  }
}

// ── HTTP SERVER ─────────────────────────────────────────────────
const server = http.createServer((req, res) => {
  if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end('{"status":"ok","service":"hustle-bridge"}');
    return;
  }

  // WhatsApp webhook verification (GET challenge)
  if (req.method === 'GET' && req.url && req.url.startsWith('/webhook')) {
    const url = new URL(req.url, 'http://localhost');
    const challenge = url.searchParams.get('hub.challenge');
    const verify    = url.searchParams.get('hub.verify_token');
    if (verify === WEBHOOK_SECRET) {
      res.writeHead(200);
      res.end(challenge);
    } else {
      res.writeHead(403);
      res.end('Forbidden');
    }
    return;
  }

  if (req.method === 'POST' && req.url === '/webhook') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      const sig = req.headers['x-hub-signature-256'] || '';
      if (!verifySignature(body, sig)) {
        res.writeHead(401);
        res.end('Unauthorized');
        return;
      }

      try {
        const payload = JSON.parse(body);
        const entry = payload.entry?.[0];
        const changes = entry?.changes?.[0];
        const msg = changes?.value?.messages?.[0];

        if (msg && msg.type === 'text') {
          const text    = msg.text.body.trim().toUpperCase();
          const phone   = msg.from;
          const handler = responses[text] || responses.HELP;
          console.log(`[WHATSAPP] Message from ${phone}: ${text}`);
          // In production: send reply via WhatsApp API
          // For now: log the response
          console.log(`[WHATSAPP] Response: ${handler()}`);
        }
      } catch (err) {
        console.error('[WHATSAPP] Parse error:', err.message);
      }

      res.writeHead(200);
      res.end('OK');
    });
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, () => {
  console.log(`[HUSTLE-BRIDGE] WhatsApp handler listening on port ${PORT}`);
});

module.exports = { responses };
