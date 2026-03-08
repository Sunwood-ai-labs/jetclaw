#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_SRC="$ROOT_DIR/picoclaw/services/jetbot_agent_bridge.service"
SERVICE_DST="/etc/systemd/system/jetbot_agent_bridge.service"
USER_NAME="${SUDO_USER:-$USER}"

TMP_FILE="$(mktemp)"
sed \
  -e "s|__USER__|$USER_NAME|g" \
  -e "s|__ROOT_DIR__|$ROOT_DIR|g" \
  "$SERVICE_SRC" > "$TMP_FILE"

install -m 644 "$TMP_FILE" "$SERVICE_DST"
rm -f "$TMP_FILE"
systemctl daemon-reload
systemctl enable --now jetbot_agent_bridge.service
systemctl --no-pager --full status jetbot_agent_bridge.service
