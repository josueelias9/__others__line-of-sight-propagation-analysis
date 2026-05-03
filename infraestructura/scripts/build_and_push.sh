#!/usr/bin/env bash
# Builds backend and frontend Docker images and pushes them to Azure Container Registry.
#
# Usage (run from the infraestructura/ directory after `terraform apply`):
#
#   export NEXT_PUBLIC_GOOGLE_MAPS_API_KEY="your_key"
#   export NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID="your_map_id"
#   ./scripts/build_and_push.sh [IMAGE_TAG]
#
# The IMAGE_TAG argument defaults to "latest".
#
# Requirements:
#   - Azure CLI (az) installed and authenticated: az login
#   - Docker installed and running
#   - terraform apply already executed at least once (outputs must exist)
#
# IMPORTANT — NEXT_PUBLIC_* variables:
#   Next.js inlines NEXT_PUBLIC_* values into the JS bundle at *build time*.
#   They cannot be overridden at runtime via App Service env vars.
#   Always rebuild and push the frontend image when these values change.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPO_ROOT="$(cd "${INFRA_DIR}/.." && pwd)"

IMAGE_TAG="${1:-latest}"

# ── Resolve Terraform outputs ─────────────────────────────────────────────────
echo "==> Reading Terraform outputs..."
cd "${INFRA_DIR}"

ACR_LOGIN_SERVER=$(terraform output -raw acr_login_server)
ACR_NAME=$(terraform output -raw acr_name)
BACKEND_URL=$(terraform output -raw backend_url)

echo "    ACR:         ${ACR_LOGIN_SERVER}"
echo "    Image tag:   ${IMAGE_TAG}"
echo "    Backend URL: ${BACKEND_URL}"

# ── Validate required env vars for frontend build ────────────────────────────
: "${NEXT_PUBLIC_GOOGLE_MAPS_API_KEY:?NEXT_PUBLIC_GOOGLE_MAPS_API_KEY is not set. Export it before running this script.}"
: "${NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID:?NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID is not set. Export it before running this script.}"

# ── Login to ACR ──────────────────────────────────────────────────────────────
echo ""
echo "==> Logging in to ACR (${ACR_NAME})..."
az acr login --name "${ACR_NAME}"

# ── Backend ───────────────────────────────────────────────────────────────────
BACKEND_IMAGE="${ACR_LOGIN_SERVER}/backend:${IMAGE_TAG}"
echo ""
echo "==> Building backend → ${BACKEND_IMAGE}"
docker build \
  --platform linux/amd64 \
  -t "${BACKEND_IMAGE}" \
  "${REPO_ROOT}/backend"

echo "==> Pushing backend..."
docker push "${BACKEND_IMAGE}"

# ── Frontend ──────────────────────────────────────────────────────────────────
FRONTEND_IMAGE="${ACR_LOGIN_SERVER}/frontend:${IMAGE_TAG}"
echo ""
echo "==> Building frontend → ${FRONTEND_IMAGE}"
echo "    (NEXT_PUBLIC_* values are baked in at build time)"
docker build \
  --platform linux/amd64 \
  --build-arg NEXT_PUBLIC_GOOGLE_MAPS_API_KEY="${NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}" \
  --build-arg NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID="${NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID}" \
  --build-arg NEXT_PUBLIC_BACKEND_URL="${BACKEND_URL}" \
  -t "${FRONTEND_IMAGE}" \
  "${REPO_ROOT}/frontend"

echo "==> Pushing frontend..."
docker push "${FRONTEND_IMAGE}"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "=== Images pushed to ACR ==="
echo "  Backend:  ${BACKEND_IMAGE}"
echo "  Frontend: ${FRONTEND_IMAGE}"
echo ""
echo "To restart the App Service containers and pull the new images:"
RG=$(terraform output -raw resource_group_name)
echo "  az webapp restart --name ${INFRA_DIR##*/}-backend  --resource-group ${RG}"
echo "  az webapp restart --name ${INFRA_DIR##*/}-frontend --resource-group ${RG}"
echo ""
echo "Or use the ACR webhook (DOCKER_ENABLE_CI=true) for automatic restarts."
