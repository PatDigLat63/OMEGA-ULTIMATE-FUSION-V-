'use strict';

const express = require('express');
const app = express();
const PORT = process.env.PORT || 3003;
const SERVICE_NAME = 'dj_executor';

app.use(express.json());

// Health / readiness probe
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: SERVICE_NAME, timestamp: new Date().toISOString() });
});

// Metrics stub (scraped by Prometheus)
app.get('/metrics', (_req, res) => {
  res.set('Content-Type', 'text/plain');
  res.send(`# HELP ${SERVICE_NAME}_up Service availability\n# TYPE ${SERVICE_NAME}_up gauge\n${SERVICE_NAME}_up 1\n`);
});

app.listen(PORT, () => {
  console.log(`[${SERVICE_NAME}] Listening on port ${PORT}`);
});
