#!/bin/sh
# OMEGA-ULTIMATE-FUSION-V∞ — Backup Script
# Brotherhood Omega Dynasty
# Runs hourly inside the backup container.

set -e

TIMESTAMP=$(date -u +"%Y%m%d_%H%M%S")
BACKUP_DIR="/backups"
DB_HOST="${DB_HOST:-postgres}"
DB_USER="${DB_USER:-omega}"
DB_NAME="${DB_NAME:-omega}"
SPACES_BUCKET="${DO_SPACES_BUCKET:-omega-backups}"
SPACES_ENDPOINT="${DO_SPACES_ENDPOINT:-nyc3.digitaloceanspaces.com}"

echo "[${TIMESTAMP}] OMEGA backup starting..."

# ── PostgreSQL dump ──────────────────────────────────────────────────
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump \
    -h "$DB_HOST" \
    -U "$DB_USER" \
    "$DB_NAME" \
    | gzip > "${BACKUP_DIR}/omega_db_${TIMESTAMP}.sql.gz"

echo "[${TIMESTAMP}] Database dump complete: omega_db_${TIMESTAMP}.sql.gz"

# ── Rotate old local backups (keep last 48) ──────────────────────────
ls -t "${BACKUP_DIR}"/omega_db_*.sql.gz | tail -n +49 | xargs -r rm -f
echo "[${TIMESTAMP}] Local rotation complete (keeping last 48)"

# ── Upload to DigitalOcean Spaces (if credentials available) ─────────
if [ -n "$DO_SPACES_KEY" ] && [ -n "$DO_SPACES_SECRET" ]; then
    # Use s3cmd or awscli-compatible tool
    if command -v s3cmd >/dev/null 2>&1; then
        s3cmd \
            --access_key="$DO_SPACES_KEY" \
            --secret_key="$DO_SPACES_SECRET" \
            --host="$SPACES_ENDPOINT" \
            --host-bucket="%(bucket)s.${SPACES_ENDPOINT}" \
            put "${BACKUP_DIR}/omega_db_${TIMESTAMP}.sql.gz" \
            "s3://${SPACES_BUCKET}/db/omega_db_${TIMESTAMP}.sql.gz"
        echo "[${TIMESTAMP}] Uploaded to DO Spaces: ${SPACES_BUCKET}/db/"
    fi
fi

echo "[${TIMESTAMP}] OMEGA backup complete. CHUKUA KONTROLI YOTE."

# ── Sleep until next run ─────────────────────────────────────────────
sleep "${BACKUP_INTERVAL:-3600}"
