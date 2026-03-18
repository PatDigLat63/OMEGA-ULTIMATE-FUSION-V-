#!/usr/bin/env bash
# ═══════════════════════════════════════════════════
# OMEGA-ULTIMATE-FUSION-V∞ — Backup Script
# Backs up database and config to GitHub
# ═══════════════════════════════════════════════════

set -euo pipefail

BACKUP_DIR="/opt/omega/backup/logs"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPO_DIR="/opt/omega"

echo "[${TIMESTAMP}] Starting OMEGA backup..."

# Backup PostgreSQL
echo "Backing up database..."
docker exec omega-postgres pg_dump \
  -U "${POSTGRES_USER:-omega_user}" \
  "${POSTGRES_DB:-omega_db}" \
  | gzip > "${BACKUP_DIR}/db_${TIMESTAMP}.sql.gz"

# Backup Redis snapshot — use env var to avoid password in process list
echo "Backing up Redis..."
docker exec -e REDISCLI_AUTH="${REDIS_PASSWORD}" omega-redis redis-cli BGSAVE
sleep 5
docker cp omega-redis:/data/dump.rdb "${BACKUP_DIR}/redis_${TIMESTAMP}.rdb"

# Git commit and push latest files
echo "Pushing to GitHub..."
cd "${REPO_DIR}"
git add -A
git commit -m "auto-backup: ${TIMESTAMP}" --allow-empty
git push origin main

echo "[${TIMESTAMP}] Backup complete."
