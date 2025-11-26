#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper around generate_aprilgrid_from_yaml.py
# Usage:
#   ./run.sh                      # default config, no text on target
#   ./run.sh --with-text          # default config, WITH text + YAML caption
#   ./run.sh path/to/config.yaml  # custom config, no text
#   ./run.sh path/to/config.yaml --with-text

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

DEFAULT_CONFIG="april_24x24_size20mm_space0.3.yaml"

CONFIG="${1:-${DEFAULT_CONFIG}}"
WITH_TEXT_FLAG=""

if [[ "$CONFIG" == "--with-text" ]]; then
  CONFIG="${DEFAULT_CONFIG}"
  WITH_TEXT_FLAG="--with-text"
elif [[ "${2:-}" == "--with-text" ]]; then
  WITH_TEXT_FLAG="--with-text"
fi

echo "[run.sh] Using config: ${CONFIG}"
if [[ -n "${WITH_TEXT_FLAG}" ]]; then
  echo "[run.sh] Enabling text labels and YAML caption"
else
  echo "[run.sh] Using no-text default"
fi

uv run generate_aprilgrid_from_yaml.py "${CONFIG}" ${WITH_TEXT_FLAG}
