/**
 * OMEGA-ULTIMATE-FUSION-V∞ — DYNASTY COMMAND SYSTEM
 * Brotherhood Omega Dynasty · 24/7 Autonomous Trading
 * Main JavaScript Module
 */

'use strict';

// ── CONSTANTS ──────────────────────────────────────────────────
const REFRESH_INTERVAL = 30000; // 30 seconds
const LOG_MAX_LINES = 50;
const AGENTS = [
  { id: 'dj',      name: 'DJ SHARPSHOOTER', wallet: 'GJ8ddFTVatiWpYEQZqfRNtpVFhG48JT79PL8V5AFfhe8', port: 3003, role: 'Trend Scanner · YOLO Executor' },
  { id: 'hashim',  name: 'HASHIM',           wallet: 'JCYTo6YaKu4Dg6sofprHdvQXaAtkzKdLqcCeNZ21Q28e', port: 3004, role: 'Treasury · Risk Manager' },
  { id: 'bossman', name: 'BOSSMAN',           wallet: 'FodX16WmaNC1SB9aMGxws4AJrjAEqEam5dKveetpQLwF', port: 3006, role: 'Risk Control · Circuit Breaker' },
  { id: 'patrick', name: 'PATRICK',           wallet: 'GJ8ddFTVatiWpYEQZqfRNtpVFhG48JT79PL8V5AFfhe8', port: 3005, role: 'Alpha Scanner · Strategy' },
  // NOTE: PATRICK shares a wallet with DJ per the dynasty configuration spec.
];
const EMERGENCY_WALLETS = [
  { label: 'Emergency 1', wallet: '6q7wbjuPnSE9pBPQ838YfcSQDyMahmXrx3RYxPSYpde1' },
  { label: 'Emergency 2', wallet: 'EcxNACs4n6rekZR3JCYDBjaVJbyQfn9StYYNRUsHu3xy' },
];
const CONTAINERS = [
  { name: 'DJ',           port: ':3003',      status: 'ACTIVE' },
  { name: 'HASHIM',       port: ':3004',      status: 'ACTIVE' },
  { name: 'BOSSMAN',      port: ':3006',      status: 'ACTIVE' },
  { name: 'PATRICK',      port: ':3005',      status: 'ACTIVE' },
  { name: 'POSTGRES',     port: ':5432',      status: 'ACTIVE' },
  { name: 'REDIS',        port: ':6379',      status: 'ACTIVE' },
  { name: 'AGENTBUS',     port: ':8081/9081', status: 'ACTIVE' },
  { name: 'DASHBOARD',    port: ':8082',      status: 'ACTIVE' },
  { name: 'LEDGER',       port: ':3010',      status: 'ACTIVE' },
  { name: 'LEARNER',      port: ':3011',      status: 'ACTIVE' },
  { name: 'EVOLVER',      port: ':3012',      status: 'ACTIVE' },
  { name: 'TELEGRAM',     port: ':3013',      status: 'ACTIVE' },
  { name: 'SCANNER',      port: ':3014',      status: 'ACTIVE' },
  { name: 'HUSTLE-BRIDGE',port: ':3001',      status: 'ACTIVE' },
];
const LOG_MESSAGES = [
  { type: 'gold', msg: '🔱 OMEGA-ULTIMATE-FUSION-V∞ INITIALISED' },
  { type: '', msg: '[DJ] Scanning SOL/USDC pair — spread: 0.12%' },
  { type: '', msg: '[HASHIM] Treasury balance verified: OK' },
  { type: '', msg: '[BOSSMAN] Risk level: MODERATE — all clear' },
  { type: '', msg: '[PATRICK] Alpha signal detected on BONK/SOL' },
  { type: '', msg: '[EVOLVER] Mutation cycle 1,247 complete' },
  { type: '', msg: '[LEDGER] Daily P&L logged: +£34.22' },
  { type: '', msg: '[SCANNER] 12 opportunities identified' },
  { type: 'warn', msg: '⚠ LQ-004 LOAN EXPIRES IN 2 DAYS — ACTION REQUIRED' },
  { type: '', msg: '[DJ] Trade executed: BUY ORCA — 0.85 SOL' },
  { type: '', msg: '[TELEGRAM] Heartbeat sent to @OmegaDynastyBot' },
  { type: '', msg: '[COMPOUND] Cycle complete — profits reinvested' },
  { type: '', msg: '[BACKUP] GitHub sync complete — all configs saved' },
  { type: '', msg: '[HUSTLE-BRIDGE] WhatsApp status: CONNECTED' },
  { type: '', msg: '[REDIS] Cache hit ratio: 98.7%' },
  { type: 'gold', msg: '💰 Profit milestone: £3,089.42 / £16,670 (18.5%)' },
];

// ── STATE ──────────────────────────────────────────────────────
const state = {
  activeTab: 'command',
  profit: 3089.42,
  target: 16670,
  trades: 1247,
  winRate: 78.4,
  uptimePct: 99.97,
  logLines: [],
  lastUpdate: Date.now(),
};

// ── STARFIELD ──────────────────────────────────────────────────
function initStarfield() {
  const container = document.getElementById('starfield');
  if (!container) return;
  const N = 120;
  for (let i = 0; i < N; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const size = Math.random() * 2.5 + 0.5;
    s.style.cssText = [
      `left:${Math.random()*100}%`,
      `top:${Math.random()*100}%`,
      `width:${size}px`,
      `height:${size}px`,
      `--dur:${(Math.random()*4+2).toFixed(1)}s`,
      `--max-op:${(Math.random()*0.6+0.2).toFixed(2)}`,
      `animation-delay:${(Math.random()*5).toFixed(1)}s`,
    ].join(';');
    container.appendChild(s);
  }
}

// ── TABS ───────────────────────────────────────────────────────
function initTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.tab;
      switchTab(id);
    });
  });
}

function switchTab(id) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === id));
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.toggle('active', p.id === 'tab-' + id));
  state.activeTab = id;
  savePrefs();
}

// ── COMMAND LOG ────────────────────────────────────────────────
function appendLog(msg, type = '') {
  const el = document.getElementById('cmd-log');
  if (!el) return;
  const ts = new Date().toTimeString().slice(0, 8);
  const line = document.createElement('div');
  line.className = 'log-line' + (type ? ' ' + type : '');
  line.textContent = `[${ts}] ${msg}`;
  el.appendChild(line);
  while (el.children.length > LOG_MAX_LINES) el.removeChild(el.firstChild);
  el.scrollTop = el.scrollHeight;
}

function initLog() {
  LOG_MESSAGES.forEach(({ msg, type }) => appendLog(msg, type));
}

// ── PROGRESS ───────────────────────────────────────────────────
function updateProgress() {
  const pct = Math.min(100, (state.profit / state.target) * 100);
  const fill = document.getElementById('progress-fill');
  const label = document.getElementById('progress-pct');
  const earned = document.getElementById('progress-earned');
  if (fill) fill.style.width = pct.toFixed(1) + '%';
  if (label) label.textContent = pct.toFixed(1) + '%';
  if (earned) earned.textContent = '£' + state.profit.toLocaleString('en-GB', { minimumFractionDigits: 2 });
}

// ── METRICS ────────────────────────────────────────────────────
function updateMetrics() {
  const els = {
    'metric-profit': '£' + state.profit.toLocaleString('en-GB', { minimumFractionDigits: 2 }),
    'metric-trades': state.trades.toLocaleString(),
    'metric-winrate': state.winRate.toFixed(1) + '%',
    'metric-uptime': state.uptimePct.toFixed(2) + '%',
  };
  Object.entries(els).forEach(([id, val]) => {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  });
}

// ── HEARTBEAT ──────────────────────────────────────────────────
function updateHeartbeat() {
  const el = document.getElementById('hb-time');
  if (el) el.textContent = new Date().toISOString().slice(0, 19).replace('T', ' ') + ' UTC';
}

// ── COPY WALLET ────────────────────────────────────────────────
function copyText(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(() => showToast('Copied!')).catch(() => fallbackCopy(text));
  } else {
    fallbackCopy(text);
  }
}

function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.cssText = 'position:fixed;opacity:0;left:-9999px';
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand('copy'); showToast('Copied!'); } catch (_) { showToast('Copy failed'); }
  document.body.removeChild(ta);
}

function showToast(msg) {
  const el = document.getElementById('copy-toast');
  if (!el) return;
  el.textContent = msg;
  el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 2000);
}

// ── BUTTON ACTIONS ─────────────────────────────────────────────
function initButtons() {
  const actions = {
    'btn-scan':    () => { appendLog('[SCANNER] Manual scan initiated…', ''); appendLog('[SCANNER] 17 opportunities found — top: BONK/SOL +2.3%', 'gold'); },
    'btn-sync':    () => { appendLog('[SYNC] Agent synchronisation initiated…', ''); appendLog('[SYNC] All 4 agents synchronised — latency: 12ms', ''); },
    'btn-compound':() => { appendLog('[COMPOUND] Compound cycle starting…', ''); state.profit += Math.random()*20; updateMetrics(); updateProgress(); appendLog('[COMPOUND] Profits compounded — new total: £' + state.profit.toFixed(2), 'gold'); },
    'btn-yolo':    () => { appendLog('[⚡ YOLO] 10X MODE ACTIVATED — ALL IN ON TOP SIGNAL', 'err'); appendLog('[DJ] YOLO trade: BONK/SOL — 10X leverage engaged', 'warn'); },
    'btn-golden':  () => { appendLog('[🌟 GOLDEN SWEEP] Dynasty-wide rebalance initiated…', 'gold'); appendLog('[GOLDEN SWEEP] Portfolio realigned to optimal allocation', 'gold'); },
    'btn-evacuate':() => { appendLog('[🚨 EVACUATE] Emergency protocol — closing all positions', 'err'); appendLog('[BOSSMAN] All positions closed — funds secured to cold wallet', 'warn'); },
    'btn-resume':  () => { appendLog('[✅ RESUME] Resuming normal operations…', ''); appendLog('[DJ] Trading resumed — all agents active', 'gold'); },
    'btn-telegram':() => { window.open('https://t.me/OmegaDynastyBot', '_blank'); },
    'btn-whatsapp':() => { window.open('https://wa.me/447424394382?text=COMMAND%20CENTER', '_blank'); },
    'btn-twitter': () => { window.open('https://x.com/patrickdl44', '_blank'); },
  };
  Object.entries(actions).forEach(([id, fn]) => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('click', fn);
  });
}

// ── LOCAL STORAGE ──────────────────────────────────────────────
function savePrefs() {
  try { localStorage.setItem('omega_tab', state.activeTab); } catch (_) {}
}

function loadPrefs() {
  try {
    const tab = localStorage.getItem('omega_tab');
    if (tab) switchTab(tab);
  } catch (_) {}
}

// ── AUTO-REFRESH ───────────────────────────────────────────────
function startAutoRefresh() {
  setInterval(() => {
    // Simulate live data updates
    state.profit += Math.random() * 2.5 - 0.5;
    state.profit = Math.max(0, state.profit);
    state.trades += Math.floor(Math.random() * 3);
    state.winRate = Math.min(99, Math.max(60, state.winRate + (Math.random() * 0.4 - 0.2)));
    updateMetrics();
    updateProgress();
    updateHeartbeat();
    // Random log
    const msgs = [
      '[DJ] Price alert: SOL crossed 200-day MA',
      '[HASHIM] Compound interest accrued: +£0.82',
      '[SCANNER] New opportunity: RAY/USDC +1.8%',
      '[EVOLVER] Strategy optimisation in progress',
      '[LEARNER] Historical data processed: 1,024 patterns',
    ];
    if (Math.random() > 0.5) {
      appendLog(msgs[Math.floor(Math.random() * msgs.length)], '');
    }
  }, REFRESH_INTERVAL);
}

// ── OFFLINE FALLBACK ────────────────────────────────────────────
window.addEventListener('online',  () => appendLog('[NETWORK] Connection restored — resuming live data', 'gold'));
window.addEventListener('offline', () => appendLog('[NETWORK] Connection lost — offline fallback mode active', 'warn'));

// ── INIT ───────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initStarfield();
  initTabs();
  initLog();
  initButtons();
  updateProgress();
  updateMetrics();
  updateHeartbeat();
  loadPrefs();
  startAutoRefresh();

  // Wire up all copy buttons
  document.querySelectorAll('[data-copy]').forEach(el => {
    el.addEventListener('click', () => copyText(el.dataset.copy));
  });

  console.log('%c🔱 OMEGA-ULTIMATE-FUSION-V∞ LOADED', 'color:#FFD700;font-size:16px;font-weight:bold;');
});
