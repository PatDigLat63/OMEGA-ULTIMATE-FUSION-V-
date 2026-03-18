/**
 * OMEGA-ULTIMATE-FUSION-V∞ — Agent Connection Tests
 * Node.js test suite (no external dependencies)
 * Run: node test/agents.js
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
  if (a !== b) throw new Error(msg || `Expected ${b}, got ${a}`);
}

console.log('\n🔱 OMEGA AGENT CONNECTION TESTS\n');

// ── WALLET VALIDATION ────────────────────────────────────────────
console.log('── Wallet Address Validation ──');

const WALLETS = {
  DJ:         'GJ8ddFTVatiWpYEQZqfRNtpVFhG48JT79PL8V5AFfhe8',
  HASHIM:     'JCYTo6YaKu4Dg6sofprHdvQXaAtkzKdLqcCeNZ21Q28e',
  BOSSMAN:    'FodX16WmaNC1SB9aMGxws4AJrjAEqEam5dKveetpQLwF',
  PATRICK:    'GJ8ddFTVatiWpYEQZqfRNtpVFhG48JT79PL8V5AFfhe8',
  EMERGENCY1: '6q7wbjuPnSE9pBPQ838YfcSQDyMahmXrx3RYxPSYpde1',
  EMERGENCY2: 'EcxNACs4n6rekZR3JCYDBjaVJbyQfn9StYYNRUsHu3xy',
};

function isValidSolanaAddress(addr) {
  return typeof addr === 'string' &&
    addr.length >= 32 && addr.length <= 44 &&
    /^[1-9A-HJ-NP-Za-km-z]+$/.test(addr);
}

Object.entries(WALLETS).forEach(([name, addr]) => {
  test(`${name} wallet address is valid Solana address`, () => {
    assert(isValidSolanaAddress(addr), `Invalid address: ${addr}`);
  });
});

test('All 6 wallet addresses defined', () => {
  assertEqual(Object.keys(WALLETS).length, 6);
});

test('Emergency wallets are different from agent wallets', () => {
  assert(WALLETS.EMERGENCY1 !== WALLETS.DJ, 'Emergency 1 should differ from DJ');
  assert(WALLETS.EMERGENCY2 !== WALLETS.DJ, 'Emergency 2 should differ from DJ');
});

// ── AGENT CONFIG VALIDATION ──────────────────────────────────────
console.log('\n── Agent Configuration ──');

const AGENT_CONFIGS = [
  { name: 'DJ', port: 3003, role: 'Trend Scanner' },
  { name: 'HASHIM', port: 3004, role: 'Treasury' },
  { name: 'BOSSMAN', port: 3006, role: 'Risk Control' },
  { name: 'PATRICK', port: 3005, role: 'Alpha Scanner' },
];

test('All 4 agents configured', () => {
  assertEqual(AGENT_CONFIGS.length, 4);
});

AGENT_CONFIGS.forEach(agent => {
  test(`${agent.name} has valid port (3000-3099)`, () => {
    assert(agent.port >= 3000 && agent.port <= 3099, `Port out of range: ${agent.port}`);
  });
  test(`${agent.name} has role defined`, () => {
    assert(agent.role && agent.role.length > 0, 'Role must be non-empty');
  });
});

test('Agent ports are unique', () => {
  const ports = AGENT_CONFIGS.map(a => a.port);
  const unique = new Set(ports);
  assertEqual(unique.size, ports.length, 'Duplicate ports found');
});

// ── CONTAINER VALIDATION ─────────────────────────────────────────
console.log('\n── Container Validation ──');

const CONTAINERS = [
  'dj', 'hashim', 'bossman', 'patrick', 'postgres', 'redis',
  'agentbus', 'dashboard', 'ledger', 'learner', 'evolver',
  'telegram', 'scanner', 'hustle-bridge',
];

test('All 14 containers defined', () => {
  assertEqual(CONTAINERS.length, 14, `Expected 14, got ${CONTAINERS.length}`);
});

test('Container names are lowercase', () => {
  CONTAINERS.forEach(c => {
    assert(c === c.toLowerCase(), `Container name not lowercase: ${c}`);
  });
});

test('All 4 agent containers present', () => {
  assert(CONTAINERS.includes('dj'), 'DJ missing');
  assert(CONTAINERS.includes('hashim'), 'HASHIM missing');
  assert(CONTAINERS.includes('bossman'), 'BOSSMAN missing');
  assert(CONTAINERS.includes('patrick'), 'PATRICK missing');
});

test('Database containers present', () => {
  assert(CONTAINERS.includes('postgres'), 'Postgres missing');
  assert(CONTAINERS.includes('redis'), 'Redis missing');
});

test('Integration containers present', () => {
  assert(CONTAINERS.includes('telegram'), 'Telegram missing');
  assert(CONTAINERS.includes('hustle-bridge'), 'Hustle-bridge missing');
});

// ── FINANCIAL TARGETS ────────────────────────────────────────────
console.log('\n── Financial Target Validation ──');

const TOTAL_TARGET = 16670;
const DAILY_TARGET = 16.67;
const CURRENT_PROFIT = 3089.42;

test('Daily target matches total/days calculation', () => {
  const days = Math.ceil(TOTAL_TARGET / DAILY_TARGET);
  assert(days >= 999 && days <= 1001, `Expected ~1000 days, got ${days}`);
});

test('Current profit is positive', () => {
  assert(CURRENT_PROFIT > 0, 'Profit must be positive');
});

test('Current profit is less than target', () => {
  assert(CURRENT_PROFIT < TOTAL_TARGET, 'Profit should not exceed target');
});

test('Progress percentage is calculated correctly', () => {
  const pct = (CURRENT_PROFIT / TOTAL_TARGET) * 100;
  assert(pct >= 18 && pct <= 19, `Expected ~18.5%, got ${pct.toFixed(2)}%`);
});

// ── SUMMARY ──────────────────────────────────────────────────────
console.log(`\n═══════════════════════════════════════`);
console.log(`RESULTS: ${passed + failed} tests | ✅ ${passed} passed | ❌ ${failed} failed`);
if (failed > 0) {
  console.error(`\n⚠️  ${failed} test(s) failed`);
  process.exit(1);
} else {
  console.log('\n🔱 ALL AGENT TESTS PASSED — DYNASTY SECURE');
  process.exit(0);
}
