#!/usr/bin/env bash
# build-push.sh — Build Docker images and push them to Azure Container Registry.
#
# Run this AFTER `./run.sh apply` so the ACR exists. On the first deploy:
#   1. ./run.sh init && ./run.sh apply   (ACR + infra created, frontend URL unknown)
#   2. ./build-push.sh                   (images pushed to ACR)
#   3. Export NEXT_PUBLIC_BACKEND_URL from step 1 output, re-apply:
#        ./run.sh apply -var="next_public_backend_url=<backend_url>"
#
# Required environment variables:
#   ARM_CLIENT_ID / ARM_CLIENT_SECRET / ARM_SUBSCRIPTION_ID / ARM_TENANT_ID
#   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
#   NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID
#   NEXT_PUBLIC_BACKEND_URL   — public URL of the backend (from terraform output)
#
# Optional:
#   IMAGE_TAG               — Docker image tag (default: latest)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "${SCRIPT_DIR}")"
IMAGE_TAG="${IMAGE_TAG:-latest}"
TF_IMAGE="hashicorp/terraform:${TERRAFORM_VERSION:-latest}"

: "${ARM_CLIENT_ID:?ARM_CLIENT_ID is required}"
: "${ARM_CLIENT_SECRET:?ARM_CLIENT_SECRET is required}"
: "${ARM_SUBSCRIPTION_ID:?ARM_SUBSCRIPTION_ID is required}"
: "${ARM_TENANT_ID:?ARM_TENANT_ID is required}"
: "${NEXT_PUBLIC_GOOGLE_MAPS_API_KEY:?NEXT_PUBLIC_GOOGLE_MAPS_API_KEY is required}"
: "${NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID:?NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID is required}"
: "${NEXT_PUBLIC_BACKEND_URL:?NEXT_PUBLIC_BACKEND_URL is required}"

# ── Resolve ACR login server from Terraform output ────────────────────────────
echo "Fetching ACR login server from Terraform outputs..."
ACR_LOGIN_SERVER=$(docker run --rm \
  -v "${SCRIPT_DIR}:/workspace" \
  -w /workspace \
  -e ARM_CLIENT_ID="${ARM_CLIENT_ID}" \
  -e ARM_CLIENT_SECRET="${ARM_CLIENT_SECRET}" \
  -e ARM_SUBSCRIPTION_ID="${ARM_SUBSCRIPTION_ID}" \
  -e ARM_TENANT_ID="${ARM_TENANT_ID}" \
  "${TF_IMAGE}" output -raw acr_login_server)

ACR_NAME="${ACR_LOGIN_SERVER%%.*}"
echo "ACR: ${ACR_LOGIN_SERVER}"

# ── Log in to ACR ─────────────────────────────────────────────────────────────
echo "Logging in to ACR..."
az acr login --name "${ACR_NAME}"

# ── Build and push backend ────────────────────────────────────────────────────
echo "Building backend image..."
docker build \
  -t "${ACR_LOGIN_SERVER}/backend:${IMAGE_TAG}" \
  "${REPO_ROOT}/backend"

echo "Pushing backend image..."
docker push "${ACR_LOGIN_SERVER}/backend:${IMAGE_TAG}"

# ── Build and push frontend ───────────────────────────────────────────────────
echo "Building frontend image (NEXT_PUBLIC_BACKEND_URL=${NEXT_PUBLIC_BACKEND_URL})..."
docker build \
  --build-arg NEXT_PUBLIC_GOOGLE_MAPS_API_KEY="${NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}" \
  --build-arg NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID="${NEXT_PUBLIC_GOOGLE_MAPS_MAP_ID}" \
  --build-arg NEXT_PUBLIC_BACKEND_URL="${NEXT_PUBLIC_BACKEND_URL}" \
  -t "${ACR_LOGIN_SERVER}/frontend:${IMAGE_TAG}" \
  "${REPO_ROOT}/frontend"

echo "Pushing frontend image..."
docker push "${ACR_LOGIN_SERVER}/frontend:${IMAGE_TAG}"

echo ""
echo "Done. Images pushed:"
echo "  ${ACR_LOGIN_SERVER}/backend:${IMAGE_TAG}"
echo "  ${ACR_LOGIN_SERVER}/frontend:${IMAGE_TAG}"
echo ""
echo "To trigger the database migration job run:"
echo "  az containerapp job start \\"
echo "    --name \$(./run.sh output -raw backend_init_job_name 2>/dev/null) \\"
echo "    --resource-group \$(./run.sh output -raw resource_group_name 2>/dev/null)"
