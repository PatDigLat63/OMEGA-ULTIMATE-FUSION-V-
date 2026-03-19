#!/bin/bash
# =============================================================================
# 🔱 OMEGA FORTRESS — DEPLOYMENT SCRIPT
# =============================================================================
# Deploys the OMEGA trading fortress to the configured DigitalOcean droplet.
# All secrets are loaded from .env — never hardcoded here.
# =============================================================================

set -euo pipefail

# ── Colours ──────────────────────────────────────────────────────────────────
readonly GOLD='\033[0;33m'
readonly GREEN='\033[0;32m'
readonly CYAN='\033[0;34m'
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

log()  { echo -e "${CYAN}${BOLD}[OMEGA]${NC} $*"; }
ok()   { echo -e "${GREEN}  ✓ $*${NC}"; }
warn() { echo -e "${YELLOW}  ⚠ $*${NC}"; }
die()  { echo -e "${RED}  ✗ $*${NC}"; exit 1; }

# ── Load environment ──────────────────────────────────────────────────────────
if [ ! -f .env ]; then
  die ".env file not found. Run: cp .env.example .env && nano .env"
fi
# shellcheck source=/dev/null
source .env

: "${DROPLET_IP:?DROPLET_IP must be set in .env}"
: "${DROPLET_USER:=root}"
: "${DEPLOY_DIR:=/opt/omega-fortress}"

# ── Phase 1: Validate prerequisites ──────────────────────────────────────────
log "[1/4] Validating prerequisites..."
command -v git  >/dev/null 2>&1 || die "git is required"
command -v ssh  >/dev/null 2>&1 || die "ssh is required"
command -v rsync>/dev/null 2>&1 || die "rsync is required"
ok "All prerequisites satisfied."

if [ ! -f ~/.ssh/id_rsa ] && [ ! -f ~/.ssh/id_ed25519 ]; then
  warn "No SSH key found. Generating ed25519 key..."
  ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
fi
ok "SSH key confirmed."

# ── Phase 2: Prepare remote server ──────────────────────────────────────────
log "[2/4] Preparing remote server at ${DROPLET_IP}..."
ssh "${DROPLET_USER}@${DROPLET_IP}" bash << REMOTE
  set -e
  # Install Docker if missing
  if ! command -v docker >/dev/null 2>&1; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    usermod -aG docker root
  fi
  # Install Docker Compose plugin if missing
  if ! docker compose version >/dev/null 2>&1; then
    echo "Installing Docker Compose plugin..."
    apt-get update -qq && apt-get install -y -qq docker-compose-plugin
  fi
  mkdir -p "${DEPLOY_DIR}"
  echo "Server ready."
REMOTE
ok "Remote server is ready."

# ── Phase 3: Sync repository ─────────────────────────────────────────────────
log "[3/4] Syncing repository to ${DROPLET_IP}:${DEPLOY_DIR}..."
rsync -az --delete \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='node_modules' \
  ./ "${DROPLET_USER}@${DROPLET_IP}:${DEPLOY_DIR}/"
ok "Repository synced."

# ── Phase 4: Deploy containers ───────────────────────────────────────────────
log "[4/4] Deploying containers..."
# shellcheck disable=SC2087
ssh "${DROPLET_USER}@${DROPLET_IP}" bash << REMOTE
  set -e
  cd "${DEPLOY_DIR}"

  # The .env file must already exist on the server with all secrets filled in
  if [ ! -f .env ]; then
    echo "ERROR: .env not found on server. Upload it manually:"
    echo "  scp .env ${DROPLET_USER}@${DROPLET_IP}:${DEPLOY_DIR}/.env"
    exit 1
  fi

  docker compose pull --quiet
  docker compose build --pull
  docker compose up -d --remove-orphans
  echo "Deployment complete."
REMOTE

ok "All containers deployed."
echo ""
echo -e "${GOLD}${BOLD}🔱 OMEGA FORTRESS IS LIVE 🔱${NC}"
echo -e "${GREEN}  Dashboard:   http://${DROPLET_IP}${NC}"
echo -e "${GREEN}  Grafana:     http://${DROPLET_IP}:3000${NC}"
echo -e "${GREEN}  Prometheus:  http://${DROPLET_IP}:9090${NC}"
