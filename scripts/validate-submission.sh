#!/usr/bin/env bash
set -euo pipefail

PING_URL="${1:-}"
REPO_DIR="${2:-.}"

if [ -z "$PING_URL" ]; then
  echo "Usage: ./validate-submission.sh <ping_url> [repo_dir]"
  exit 1
fi

REPO_DIR="$(cd "$REPO_DIR" && pwd)"
PING_URL="${PING_URL%/}"

echo "========================================"
echo " OpenEnv Submission Validator"
echo "========================================"
echo "Repo: $REPO_DIR"
echo "Ping URL: $PING_URL"
echo ""

echo "Step 1: Checking Space..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$PING_URL/reset")
if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ Space is live"
else
  echo "❌ Space not reachable"
  exit 1
fi

echo ""
echo "Step 2: Docker build..."
docker build "$REPO_DIR" || exit 1
echo "✅ Docker build success"

echo ""
echo "Step 3: openenv validate..."
openenv validate || exit 1
echo "✅ openenv validate passed"

echo ""
echo "🎉 ALL CHECKS PASSED!"