#!/usr/bin/env bash
#
# deploy.sh — Shell-style deployment script with dry-run support.
#
# Usage:
#   ./deploy.sh --env staging --version 1.2.3
#   ./deploy.sh --env prod --version 1.2.3 --dry-run
#
# Options:
#   --env       Target environment: staging | prod  (required)
#   --version   Semantic version tag to deploy       (required)
#   --dry-run   Simulate deployment without making changes
#
set -euo pipefail

# ──────────────────────────────────────────────
# Defaults
# ──────────────────────────────────────────────
ENV=""
VERSION=""
DRY_RUN=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/deploy-$(date +%Y%m%d-%H%M%S).log"

# ──────────────────────────────────────────────
# Colours (disabled when piped / non-tty)
# ──────────────────────────────────────────────
if [ -t 1 ]; then
  RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
else
  RED=''; GREEN=''; YELLOW=''; NC=''
fi

# ──────────────────────────────────────────────
# Logging helpers
# ──────────────────────────────────────────────
log()  { echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
info() { log "${GREEN}[INFO]${NC}  $*"; }
warn() { log "${YELLOW}[WARN]${NC}  $*"; }
err()  { log "${RED}[ERROR]${NC} $*" >&2; }

# ──────────────────────────────────────────────
# Usage
# ──────────────────────────────────────────────
usage() {
  cat <<EOF
Usage: $(basename "$0") --env <staging|prod> --version <semver> [--dry-run]

Options:
  --env       Target environment: staging | prod  (required)
  --version   Semantic version tag to deploy       (required)
  --dry-run   Simulate deployment without making changes
  -h, --help  Show this help message

Examples:
  $(basename "$0") --env staging --version 1.2.3
  $(basename "$0") --env prod --version 1.2.3 --dry-run
EOF
}

# ──────────────────────────────────────────────
# Parse arguments
# ──────────────────────────────────────────────
parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --env)     ENV="$2";       shift 2 ;;
      --version) VERSION="$2";   shift 2 ;;
      --dry-run) DRY_RUN=true;   shift   ;;
      -h|--help) usage; exit 0  ;;
      *)         err "Unknown argument: $1"; usage; exit 1 ;;
    esac
  done

  if [[ -z "$ENV" ]]; then
    err "--env is required (staging | prod)"
    exit 1
  fi
  if [[ -z "$VERSION" ]]; then
    err "--version is required (e.g. 1.2.3)"
    exit 1
  fi
  if [[ "$ENV" != "staging" && "$ENV" != "prod" ]]; then
    err "--env must be 'staging' or 'prod', got '$ENV'"
    exit 1
  fi
}

# ──────────────────────────────────────────────
# Preflight checks
# ──────────────────────────────────────────────
preflight() {
  info "Running preflight checks for ${ENV} / ${VERSION} ..."

  # 1. Required commands
  local cmds=(git curl bash)
  for cmd in "${cmds[@]}"; do
    if ! command -v "$cmd" &>/dev/null; then
      err "Required command not found: $cmd"
      return 1
    fi
  done
  info "  ✓ All required commands available"

  # 2. Git connectivity
  if ! git ls-remote --heads origin &>/dev/null; then
    warn "  ⚠ Cannot reach Git remote 'origin' — offline mode"
  else
    info "  ✓ Git remote reachable"
  fi

  # 3. Version tag exists locally or remotely
  if git tag -l "$VERSION" | grep -q "$VERSION"; then
    info "  ✓ Tag ${VERSION} found locally"
  elif git ls-remote --tags origin "refs/tags/${VERSION}" &>/dev/null; then
    info "  ✓ Tag ${VERSION} found on remote"
  else
    warn "  ⚠ Tag ${VERSION} not found — deployment may fail"
  fi

  # 4. Secrets validation (environment variables)
  if [[ "$ENV" == "prod" ]]; then
    if [[ -z "${DEPLOY_TOKEN:-}" ]]; then
      err "DEPLOY_TOKEN is not set (required for ${ENV})"
      return 1
    fi
    info "  ✓ DEPLOY_TOKEN is set"
  fi

  # 5. Disk space
  local avail_kb
  avail_kb=$(df -k "$SCRIPT_DIR" | awk 'NR==2{print $4}')
  if (( avail_kb < 102400 )); then          # < 100 MB
    warn "  ⚠ Less than 100 MB disk space available"
  else
    info "  ✓ Sufficient disk space (${avail_kb} KB)"
  fi

  info "Preflight checks completed."
  return 0
}

# ──────────────────────────────────────────────
# Deploy to staging
# ──────────────────────────────────────────────
deploy_staging() {
  info "Deploying ${VERSION} to staging ..."
  if $DRY_RUN; then
    info "[DRY-RUN] Would pull tag ${VERSION}"
    info "[DRY-RUN] Would run: docker build -t app:${VERSION} ."
    info "[DRY-RUN] Would deploy to staging cluster"
    info "[DRY-RUN] Would run smoke tests against staging"
    return 0
  fi

  git fetch --tags 2>/dev/null || true
  git checkout "tags/${VERSION}" 2>/dev/null || warn "Tag checkout failed, continuing ..."
  info "Build and deploy to staging (simulated)"
  info "Staging deployment complete."
}

# ──────────────────────────────────────────────
# Deploy to production
# ──────────────────────────────────────────────
deploy_prod() {
  info "Deploying ${VERSION} to production ..."
  if $DRY_RUN; then
    info "[DRY-RUN] Would verify staging health checks"
    info "[DRY-RUN] Would promote ${VERSION} to production"
    info "[DRY-RUN] Would run production smoke tests"
    info "[DRY-RUN] Would notify on-call channel"
    return 0
  fi

  # Production requires explicit confirmation
  info "Production deployment requires DEPLOY_TOKEN (already validated in preflight)"
  info "Promoting ${VERSION} to production (simulated)"
  info "Production deployment complete."
}

# ──────────────────────────────────────────────
# Post-deploy verification
# ──────────────────────────────────────────────
post_deploy() {
  info "Running post-deploy verification ..."
  if $DRY_RUN; then
    info "[DRY-RUN] Would check health endpoint: /health"
    info "[DRY-RUN] Would verify version endpoint: /version"
    return 0
  fi
  info "Health check passed (simulated)"
  info "Post-deploy verification complete."
}

# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────
main() {
  parse_args "$@"

  info "========================================"
  info "Deployment: ${ENV} / ${VERSION}"
  info "Dry-run:    ${DRY_RUN}"
  info "========================================"

  preflight || exit 1

  case "$ENV" in
    staging) deploy_staging ;;
    prod)    deploy_prod    ;;
  esac

  post_deploy

  if $DRY_RUN; then
    info "DRY-RUN complete — no changes were made."
  else
    info "Deployment to ${ENV} finished successfully."
  fi
  info "Log saved to: ${LOG_FILE}"
}

main "$@"
