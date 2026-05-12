#!/usr/bin/env bash
# Builds backend and frontend Docker images, pushes them to ACR, and updates
# the running Container Apps to the new image.
#
# Prerequisites:
#   1. terraform apply already ran (Container Apps exist with hello-world image)
#   2. Azure CLI authenticated: az login
#   3. Docker running
#
# Usage (from the repo root or infraestructura/ directory):
#
#   export NEXT_PUBLIC_GOOGLE_MAPS_API_KEY="your_key"
#   export NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID="your_map_id"
#   ./scripts/build_and_push.sh [IMAGE_TAG]
#
# IMAGE_TAG defaults to "latest".
#
# IMPORTANT — NEXT_PUBLIC_* variables:
#   Next.js inlines NEXT_PUBLIC_* values into the JS bundle at *build time*.
#   Rebuild and push the frontend image whenever these values change.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${INFRA_DIR}/.." && pwd)"

IMAGE_TAG="${1:-latest}"

# ── Load variables from .env file ────────────────────────────────────────────
if [[ -f "${REPO_ROOT}/.env" ]]; then
  echo "==> Loading env vars from ${REPO_ROOT}/.env"
  set -a
  # shellcheck source=/dev/null
  source "${REPO_ROOT}/.env"
  set +a
fi

cd "${INFRA_DIR}"

# ── Validate required env vars ────────────────────────────────────────────────
: "${NEXT_PUBLIC_GOOGLE_MAPS_API_KEY:?NEXT_PUBLIC_GOOGLE_MAPS_API_KEY is not set.}"
: "${NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID:?NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID is not set.}"

# ── Read Terraform outputs ────────────────────────────────────────────────────
echo "==> Reading Terraform outputs..."
ACR_LOGIN_SERVER=$(terraform output -raw acr_login_server)
ACR_NAME=$(terraform output -raw acr_name)
RG=$(terraform output -raw resource_group_name)
BACKEND_NAME=$(terraform output -raw backend_name)
FRONTEND_NAME=$(terraform output -raw frontend_name)

echo "    ACR:      ${ACR_LOGIN_SERVER}"
echo "    Tag:      ${IMAGE_TAG}"
echo "    Backend:  ${BACKEND_NAME}"
echo "    Frontend: ${FRONTEND_NAME}"

# ── Login to ACR ──────────────────────────────────────────────────────────────
echo ""
echo "==> Logging in to ACR..."
az acr login --name "${ACR_NAME}"

# ── Build & push backend ──────────────────────────────────────────────────────
BACKEND_IMAGE="${ACR_LOGIN_SERVER}/backend:${IMAGE_TAG}"
echo ""
echo "==> Building backend → ${BACKEND_IMAGE}"
docker build \
  --platform linux/amd64 \
  -t "${BACKEND_IMAGE}" \
  "${REPO_ROOT}/backend"

echo "==> Pushing backend..."
docker push "${BACKEND_IMAGE}"

# ── Build & push frontend ─────────────────────────────────────────────────────
FRONTEND_IMAGE="${ACR_LOGIN_SERVER}/frontend:${IMAGE_TAG}"
echo ""
echo "==> Building frontend → ${FRONTEND_IMAGE}"
docker build \
  --platform linux/amd64 \
  --build-arg NEXT_PUBLIC_GOOGLE_MAPS_API_KEY="${NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}" \
  --build-arg NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID="${NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID}" \
  -t "${FRONTEND_IMAGE}" \
  "${REPO_ROOT}/frontend"

echo "==> Pushing frontend..."
docker push "${FRONTEND_IMAGE}"

# ── Update Container Apps to the new image ────────────────────────────────────
echo ""
echo "==> Updating Container Apps..."
az containerapp update \
  --name "${BACKEND_NAME}" \
  --resource-group "${RG}" \
  --image "${BACKEND_IMAGE}" \
  --output none

az containerapp update \
  --name "${FRONTEND_NAME}" \
  --resource-group "${RG}" \
  --image "${FRONTEND_IMAGE}" \
  --output none

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo "=== Done ==="
echo "  Backend:  https://$(az containerapp show --name "${BACKEND_NAME}" --resource-group "${RG}" --query 'properties.latestRevisionFqdn' -o tsv)"
echo "  Frontend: https://$(az containerapp show --name "${FRONTEND_NAME}" --resource-group "${RG}" --query 'properties.latestRevisionFqdn' -o tsv)"
