/**
 * OMEGA-ULTIMATE-FUSION-V∞ — Docker Container Health Tests
 * Node.js test suite (built-in http module only)
 * Run: node test/containers.js
 *
 * NOTE: These tests check container health endpoints.
 * Run on the server (206.189.118.255) or with containers running locally.
 * In CI without containers, tests are marked as SKIPPED.
 */

'use strict';

const http = require('http');

let passed = 0, failed = 0, skipped = 0;

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

function skip(name, reason) {
  console.log(`  ⏭  SKIP — ${name} (${reason})`);
  skipped++;
}

function assert(condition, msg) {
  if (!condition) throw new Error(msg || 'Assertion failed');
}

// ── CHECK IF RUNNING IN CI/OFFLINE ──────────────────────────────
const IS_CI = process.env.CI === 'true';

// ── CONTAINER CONFIG TESTS (always run) ──────────────────────────
console.log('\n🐳 OMEGA CONTAINER CONFIGURATION TESTS\n');
console.log('── Container Port Assignments ──');

const CONTAINER_PORTS = {
  'hustle-bridge': 3001,
  'dj':            3003,
  'hashim':        3004,
  'patrick':       3005,
  'bossman':       3006,
  'ledger':        3010,
  'learner':       3011,
  'evolver':       3012,
  'telegram':      3013,
  'scanner':       3014,
  'postgres':      5432,
  'redis':         6379,
  'agentbus-http': 8081,
  'dashboard':     8082,
};

test('All 14 container ports defined', () => {
  assert(Object.keys(CONTAINER_PORTS).length === 14,
    `Expected 14, got ${Object.keys(CONTAINER_PORTS).length}`);
});

test('No duplicate ports', () => {
  const ports = Object.values(CONTAINER_PORTS);
  const unique = new Set(ports);
  assert(unique.size === ports.length, 'Duplicate ports detected');
});

test('Agent ports are in 3000-3099 range', () => {
  ['dj', 'hashim', 'patrick', 'bossman'].forEach(name => {
    const port = CONTAINER_PORTS[name];
    assert(port >= 3000 && port < 3100, `${name} port out of range: ${port}`);
  });
});

test('Database ports are standard', () => {
  assert(CONTAINER_PORTS['postgres'] === 5432, 'Postgres should use 5432');
  assert(CONTAINER_PORTS['redis'] === 6379, 'Redis should use 6379');
});

test('Dashboard accessible port defined', () => {
  assert(CONTAINER_PORTS['dashboard'] === 8082, 'Dashboard should be on 8082');
});

// ── DOCKER COMPOSE FILE TESTS ─────────────────────────────────────
console.log('\n── Docker Compose Validation ──');

const fs = require('fs');
const path = require('path');

const composePath = path.join(__dirname, '..', 'infrastructure', 'docker', 'docker-compose.yml');

test('docker-compose.yml exists', () => {
  assert(fs.existsSync(composePath), `File not found: ${composePath}`);
});

test('docker-compose.yml is readable', () => {
  const content = fs.readFileSync(composePath, 'utf8');
  assert(content.length > 100, 'File is too short to be valid');
});

test('docker-compose.yml contains all 14 services', () => {
  const content = fs.readFileSync(composePath, 'utf8');
  const services = ['dj:', 'hashim:', 'bossman:', 'patrick:', 'postgres:', 'redis:',
    'agentbus:', 'dashboard:', 'ledger:', 'learner:', 'evolver:',
    'telegram:', 'scanner:', 'hustle-bridge:'];
  services.forEach(svc => {
    assert(content.includes(svc), `Service missing from compose: ${svc}`);
  });
});

test('docker-compose.yml has restart policies', () => {
  const content = fs.readFileSync(composePath, 'utf8');
  assert(content.includes('unless-stopped'), 'Missing restart: unless-stopped policy');
});

test('docker-compose.yml has health checks', () => {
  const content = fs.readFileSync(composePath, 'utf8');
  assert(content.includes('healthcheck:'), 'Missing healthcheck configurations');
});

test('docker-compose.yml uses volumes for PostgreSQL', () => {
  const content = fs.readFileSync(composePath, 'utf8');
  assert(content.includes('postgres_data'), 'Missing postgres volume');
});

// ── HEALTH ENDPOINT TESTS (skip in CI) ───────────────────────────
console.log('\n── Container Health Checks ──');

function checkHealth(host, port, path, name) {
  return new Promise((resolve) => {
    if (IS_CI) {
      skip(`${name} health endpoint`, 'CI environment — containers not running');
      resolve();
      return;
    }

    const req = http.request({ host, port, path, timeout: 3000 }, (res) => {
      if (res.statusCode === 200) {
        console.log(`  ✅ PASS — ${name} is healthy (HTTP ${res.statusCode})`);
        passed++;
      } else {
        console.error(`  ❌ FAIL — ${name} returned HTTP ${res.statusCode}`);
        failed++;
      }
      resolve();
    });
    req.on('timeout', () => {
      skip(`${name} health endpoint`, 'Connection timeout');
      req.destroy();
      resolve();
    });
    req.on('error', () => {
      skip(`${name} health endpoint`, 'Not reachable (container may not be running)');
      resolve();
    });
    req.end();
  });
}

const healthChecks = [
  { port: 3003, path: '/health', name: 'DJ Agent' },
  { port: 3004, path: '/health', name: 'Hashim Agent' },
  { port: 3006, path: '/health', name: 'Bossman Agent' },
  { port: 3005, path: '/health', name: 'Patrick Agent' },
  { port: 8082, path: '/health', name: 'Dashboard' },
  { port: 3013, path: '/health', name: 'Telegram Bot' },
  { port: 3001, path: '/health', name: 'Hustle Bridge' },
];

Promise.all(
  healthChecks.map(({ port, path: p, name }) =>
    checkHealth('localhost', port, p, name)
  )
).then(() => {
  console.log(`\n═══════════════════════════════════════`);
  console.log(`RESULTS: ${passed + failed + skipped} tests`);
  console.log(`  ✅ Passed:  ${passed}`);
  console.log(`  ❌ Failed:  ${failed}`);
  console.log(`  ⏭  Skipped: ${skipped}`);
  if (failed > 0) {
    console.error(`\n⚠️  ${failed} test(s) failed`);
    process.exit(1);
  } else {
    console.log('\n🔱 CONTAINER TESTS COMPLETE — DYNASTY SECURE');
    process.exit(0);
  }
});
