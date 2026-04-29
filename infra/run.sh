#!/usr/bin/env bash
# run.sh — Run Terraform commands using the official hashicorp/terraform Docker image.
#
# Usage:
#   ./run.sh init
#   ./run.sh plan
#   ./run.sh apply
#   ./run.sh apply -auto-approve
#   ./run.sh output -raw backend_url
#   ./run.sh destroy
#
# Required environment variables (Azure Service Principal):
#   ARM_CLIENT_ID       — Service Principal Application (client) ID
#   ARM_CLIENT_SECRET   — Service Principal secret
#   ARM_SUBSCRIPTION_ID — Azure Subscription ID
#   ARM_TENANT_ID       — Azure Tenant ID
#
# Optional:
#   TERRAFORM_VERSION   — Image tag to use (default: latest)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE="hashicorp/terraform:${TERRAFORM_VERSION:-latest}"

: "${ARM_CLIENT_ID:?ARM_CLIENT_ID is required}"
: "${ARM_CLIENT_SECRET:?ARM_CLIENT_SECRET is required}"
: "${ARM_SUBSCRIPTION_ID:?ARM_SUBSCRIPTION_ID is required}"
: "${ARM_TENANT_ID:?ARM_TENANT_ID is required}"

docker run --rm \
  -v "${SCRIPT_DIR}:/workspace" \
  -w /workspace \
  -e ARM_CLIENT_ID="${ARM_CLIENT_ID}" \
  -e ARM_CLIENT_SECRET="${ARM_CLIENT_SECRET}" \
  -e ARM_SUBSCRIPTION_ID="${ARM_SUBSCRIPTION_ID}" \
  -e ARM_TENANT_ID="${ARM_TENANT_ID}" \
  "${IMAGE}" "$@"
