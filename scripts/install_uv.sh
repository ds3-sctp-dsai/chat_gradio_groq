#!/usr/bin/env bash
set -euo pipefail

if ! command -v curl >/dev/null 2>&1; then
  echo "Error: curl is required to install uv." >&2
  exit 1
fi

echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "uv installation script completed."
echo "If 'uv' is not yet available, restart your shell or run:"
echo "  source \"$HOME/.local/bin/env\" 2>/dev/null || true"
