/**
 * OMEGA-ULTIMATE-FUSION-V∞ — Integration Tests
 * Tests for WhatsApp, Telegram, and X configurations
 * Run: node test/integrations.js
 */

'use strict';

let passed = 0, failed = 0;

function test(name, fn) {
  try {
    fn();
    console.log(`  ✅ PASS — ${name}`);
    passed++;
  } catch (err) {
    console.error(`  ❌ FAIL — ${name}: ${err.message}`);
    failed++;
  }
}

function assert(condition, msg) {
  if (!condition) throw new Error(msg || 'Assertion failed');
}

function assertEqual(a, b, msg) {
  if (a !== b) throw new Error(msg || `Expected "${b}", got "${a}"`);
}

console.log('\n📡 OMEGA INTEGRATION TESTS\n');

// ── FILE EXISTENCE TESTS ─────────────────────────────────────────
const fs   = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');

console.log('── Required Files ──');

const requiredFiles = [
  'index.html',
  'dashboard.html',
  'README.md',
  'DEPLOY.md',
  'CONFIG.md',
  'EMERGENCY.md',
  'TELEGRAM-BOT.md',
  'WHATSAPP.md',
  'X-TWITTER.md',
  '_config.yml',
  'CNAME',
  '.env.example',
  'assets/css/style.css',
  'assets/js/main.js',
  'infrastructure/docker/docker-compose.yml',
  'integrations/telegram/bot.js',
  'integrations/whatsapp/handler.js',
  'integrations/twitter/poster.js',
  'backup/wallets/README.md',
];

requiredFiles.forEach(file => {
  test(`${file} exists`, () => {
    assert(fs.existsSync(path.join(root, file)), `Missing: ${file}`);
  });
});

// ── TELEGRAM BOT TESTS ───────────────────────────────────────────
console.log('\n── Telegram Bot ──');

const botPath = path.join(root, 'integrations/telegram/bot.js');
test('Telegram bot file is non-empty', () => {
  const stat = fs.statSync(botPath);
  assert(stat.size > 100, 'File is too small');
});

test('Telegram bot exports sendMessage', () => {
  const content = fs.readFileSync(botPath, 'utf8');
  assert(content.includes('sendMessage'), 'Missing sendMessage export');
});

test('Telegram bot has all required commands', () => {
  const content = fs.readFileSync(botPath, 'utf8');
  ['/status', '/pnl', '/positions', '/evacuate', '/resume'].forEach(cmd => {
    assert(content.includes(cmd), `Missing command: ${cmd}`);
  });
});

test('Telegram bot has daily report scheduler', () => {
  const content = fs.readFileSync(botPath, 'utf8');
  assert(content.includes('scheduleDailyReport') || content.includes('08:00') || content.includes("'8, 0'"), 'Missing daily report');
});

// ── WHATSAPP TESTS ───────────────────────────────────────────────
console.log('\n── WhatsApp Handler ──');

const waPath = path.join(root, 'integrations/whatsapp/handler.js');
test('WhatsApp handler is non-empty', () => {
  const stat = fs.statSync(waPath);
  assert(stat.size > 100, 'File is too small');
});

test('WhatsApp handler has STATUS response', () => {
  const content = fs.readFileSync(waPath, 'utf8');
  assert(content.includes('STATUS'), 'Missing STATUS response');
});

test('WhatsApp handler has signature verification', () => {
  const content = fs.readFileSync(waPath, 'utf8');
  assert(content.includes('verifySignature') || content.includes('timingSafeEqual'), 'Missing signature verification');
});

test('WhatsApp handler has health endpoint', () => {
  const content = fs.readFileSync(waPath, 'utf8');
  assert(content.includes('/health'), 'Missing health endpoint');
});

// ── TWITTER POSTER TESTS ─────────────────────────────────────────
console.log('\n── X/Twitter Poster ──');

const twPath = path.join(root, 'integrations/twitter/poster.js');
test('Twitter poster is non-empty', () => {
  const stat = fs.statSync(twPath);
  assert(stat.size > 100, 'File is too small');
});

test('Twitter poster has postTweet function', () => {
  const content = fs.readFileSync(twPath, 'utf8');
  assert(content.includes('postTweet'), 'Missing postTweet function');
});

test('Twitter poster has YOLO template', () => {
  const content = fs.readFileSync(twPath, 'utf8');
  assert(content.includes('yoloPost') || content.includes('YOLO'), 'Missing YOLO template');
});

test('Twitter poster limits tweet length to 280 chars', () => {
  const content = fs.readFileSync(twPath, 'utf8');
  assert(content.includes('280'), 'Missing 280-char limit enforcement');
});

test('Twitter poster uses OAuth 1.0a', () => {
  const content = fs.readFileSync(twPath, 'utf8');
  assert(content.includes('oauth') || content.includes('OAuth'), 'Missing OAuth implementation');
});

// ── GITHUB PAGES TESTS ───────────────────────────────────────────
console.log('\n── GitHub Pages ──');

test('CNAME contains correct domain', () => {
  const cname = fs.readFileSync(path.join(root, 'CNAME'), 'utf8').trim();
  assertEqual(cname, 'brotherhoodomegadynasty.com', 'CNAME should be brotherhoodomegadynasty.com');
});

test('_config.yml has theme configured', () => {
  const config = fs.readFileSync(path.join(root, '_config.yml'), 'utf8');
  assert(config.includes('theme') || config.includes('jekyll'), 'Missing theme in _config.yml');
});

// ── ENV EXAMPLE TESTS ─────────────────────────────────────────────
console.log('\n── Environment Config ──');

test('.env.example has all required variables', () => {
  const env = fs.readFileSync(path.join(root, '.env.example'), 'utf8');
  const required = [
    'POSTGRES_PASSWORD',
    'TELEGRAM_BOT_TOKEN',
    'WHATSAPP_API_KEY',
    'TWITTER_API_KEY',
    'SOLANA_RPC_URL',
  ];
  required.forEach(v => {
    assert(env.includes(v), `Missing env variable: ${v}`);
  });
});

test('.env is in .gitignore', () => {
  const gitignore = fs.readFileSync(path.join(root, '.gitignore'), 'utf8');
  assert(gitignore.includes('.env'), '.env should be in .gitignore');
});

// ── SUMMARY ──────────────────────────────────────────────────────
console.log(`\n═══════════════════════════════════════`);
console.log(`RESULTS: ${passed + failed} tests | ✅ ${passed} passed | ❌ ${failed} failed`);
if (failed > 0) {
  console.error(`\n⚠️  ${failed} test(s) failed`);
  process.exit(1);
} else {
  console.log('\n🔱 ALL INTEGRATION TESTS PASSED — DYNASTY CONNECTED');
  process.exit(0);
}
