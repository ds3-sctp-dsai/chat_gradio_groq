#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]]; then
  echo "Error: TELEGRAM_BOT_TOKEN is required." >&2
  exit 1
fi

if [[ -z "${WEBHOOK_URL:-}" ]]; then
  echo "Error: WEBHOOK_URL is required (e.g. https://example.com/webhook/telegram)." >&2
  exit 1
fi

payload=(
  -d "url=${WEBHOOK_URL}"
)

if [[ -n "${TELEGRAM_WEBHOOK_SECRET:-}" ]]; then
  payload+=( -d "secret_token=${TELEGRAM_WEBHOOK_SECRET}" )
fi

curl -sS "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" "${payload[@]}"
echo
