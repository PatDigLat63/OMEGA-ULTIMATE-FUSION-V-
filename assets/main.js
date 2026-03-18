/* ── Starfield ── */
(function () {
  const canvas = document.getElementById('starfield');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let stars = [];
  const N = 180;

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function init() {
    stars = Array.from({ length: N }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      r: Math.random() * 1.2 + 0.2,
      alpha: Math.random() * 0.6 + 0.1,
      speed: Math.random() * 0.15 + 0.03,
      twinkle: Math.random() * Math.PI * 2,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const t = Date.now() / 1000;
    stars.forEach(s => {
      const alpha = s.alpha * (0.6 + 0.4 * Math.sin(t * 1.2 + s.twinkle));
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(200, 230, 255, ${alpha})`;
      ctx.fill();
      s.y -= s.speed;
      if (s.y < -2) {
        s.y = canvas.height + 2;
        s.x = Math.random() * canvas.width;
      }
    });
    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', () => { resize(); init(); });
  resize();
  init();
  draw();
})();

/* ── Intersection observer fade-in ── */
(function () {
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => io.observe(el));
})();

/* ── Live terminal feed ── */
(function () {
  const body = document.getElementById('terminal-body');
  if (!body) return;

  const AGENTS = [
    'ALPHA-SCANNER', 'BETA-EXECUTOR', 'GAMMA-RISK', 'DELTA-ARB',
    'EPSILON-SENTIMENT', 'ZETA-MOMENTUM', 'ETA-LIQUIDITY', 'THETA-REBALANCER',
  ];
  const CHAINS = [
    'ETH', 'BSC', 'ARB', 'SOL', 'AVAX', 'MATIC', 'BASE', 'OP', 'FANTOM', 'APTOS', 'SUI', 'INJ',
  ];
  const PAIRS  = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ARB/USDT', 'AVAX/USDT', 'MATIC/USDT'];
  const ACTIONS = [
    ['t-ok',   () => `[${pick(AGENTS)}] ✓ TRADE EXECUTED  ${pick(PAIRS)}  +${(Math.random()*4+0.5).toFixed(3)}%`],
    ['t-sys',  () => `[TEMPORAL]  Workflow step COMPLETED  latency ${(Math.random()*12+2).toFixed(1)}ms`],
    ['t-warn', () => `[${pick(AGENTS)}] ⚠ Slippage guard triggered on ${pick(CHAINS)}  retry in 200ms`],
    ['t-ok',   () => `[CIRCUIT-BREAKER] Drawdown ${(Math.random()*14+0.5).toFixed(2)}% — within 15% limit ✓`],
    ['t-sys',  () => `[HEALTHCHECK] Container ${Math.floor(Math.random()*32)+1}/32  status: HEALTHY`],
    ['t-ok',   () => `[${pick(AGENTS)}] ARB detected  ${pick(CHAINS)}↔${pick(CHAINS)}  spread ${(Math.random()*0.8+0.1).toFixed(3)}%`],
    ['t-line', () => `[ORACLE] Price feed updated  block ${(17000000 + Math.floor(Math.random()*1000000)).toLocaleString()}`],
    ['t-ok',   () => `[REBALANCER] Portfolio drift corrected  Sharpe→${(1.8+Math.random()*0.8).toFixed(2)}`],
    ['t-sys',  () => `[TEMPORAL]  Heartbeat OK  next tick in ${(Math.random()*500+100).toFixed(0)}ms`],
    ['t-prompt',() => `[OMEGA-BRAIN] Strat evaluated in ${(Math.random()*8+1).toFixed(1)}ms  confidence ${(Math.random()*20+80).toFixed(1)}%`],
  ];

  function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

  function addLine() {
    const [cls, gen] = pick(ACTIONS);
    const ts = new Date().toISOString().replace('T', ' ').slice(0, 23);
    const div = document.createElement('div');
    div.className = `t-line ${cls}`;
    div.textContent = `${ts}  ${gen()}`;
    body.appendChild(div);
    while (body.children.length > 60) body.removeChild(body.firstChild);
    body.scrollTop = body.scrollHeight;
  }

  /* Bootstrap lines */
  const BOOT = [
    ['t-sys', '  ███████╗██╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗'],
    ['t-sys', '  ██╔════╝██║   ██║██╔════╝██║██╔═══██╗████╗  ██║'],
    ['t-sys', '  █████╗  ██║   ██║███████╗██║██║   ██║██╔██╗ ██║'],
    ['t-sys', '  ██╔══╝  ██║   ██║╚════██║██║██║   ██║██║╚██╗██║'],
    ['t-sys', '  ██║     ╚██████╔╝███████║██║╚██████╔╝██║ ╚████║'],
    ['t-sys', '  ╚═╝      ╚═════╝ ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝'],
    ['t-sys', ''],
    ['t-sys', '  OMEGA-ULTIMATE-FUSION-V∞  —  THE FINAL FORM'],
    ['t-sys', ''],
    ['t-ok',  '[BOOT] Initializing 32 containers...'],
    ['t-ok',  '[BOOT] Loading 8 autonomous agents...'],
    ['t-ok',  '[BOOT] Connecting to 12 chains...'],
    ['t-ok',  '[BOOT] Temporal.io workflow engine ONLINE'],
    ['t-ok',  '[BOOT] Circuit breaker armed at 15%'],
    ['t-ok',  '[BOOT] YOLO multiplier set to 150X'],
    ['t-ok',  '[BOOT] All systems operational — CHUKUA KONTROLI YOTE 🔱'],
    ['t-sys', ''],
    ['t-line','─────────────────── LIVE FEED ───────────────────────────'],
  ];

  let i = 0;
  function bootLine() {
    if (i < BOOT.length) {
      const [cls, txt] = BOOT[i++];
      const div = document.createElement('div');
      div.className = `t-line ${cls}`;
      div.style.whiteSpace = 'pre';
      div.textContent = txt;
      body.appendChild(div);
      body.scrollTop = body.scrollHeight;
      setTimeout(bootLine, 60);
    } else {
      setInterval(addLine, 900);
    }
  }
  bootLine();
})();

/* ── Uptime counter ── */
(function () {
  const el = document.getElementById('uptime-counter');
  if (!el) return;
  const START = Date.now() - (Math.random() * 1e10 + 5e9);
  function tick() {
    const d = Math.floor((Date.now() - START) / 86400000);
    const h = Math.floor(((Date.now() - START) % 86400000) / 3600000);
    const m = Math.floor(((Date.now() - START) % 3600000) / 60000);
    const s = Math.floor(((Date.now() - START) % 60000) / 1000);
    el.textContent = `${d}d ${String(h).padStart(2,'0')}h ${String(m).padStart(2,'0')}m ${String(s).padStart(2,'0')}s`;
  }
  tick();
  setInterval(tick, 1000);
})();

/* ── Live PnL ticker ── */
(function () {
  const el = document.getElementById('pnl-live');
  if (!el) return;
  let base = 14820143;
  function tick() {
    base += Math.random() * 4000 - 200;
    el.textContent = '$' + base.toLocaleString('en-US', { maximumFractionDigits: 0 });
    el.style.color = base > 14820143 ? 'var(--accent-green)' : 'var(--accent-red)';
  }
  tick();
  setInterval(tick, 2000);
})();
