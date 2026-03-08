#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVICE_SRC="$ROOT_DIR/picoclaw/picoclaw-gateway.service"
SERVICE_DST="/etc/systemd/system/picoclaw-gateway.service"
USER_NAME="${SUDO_USER:-$USER}"
GROUP_NAME="$(id -gn "$USER_NAME")"
HOME_DIR="$(getent passwd "$USER_NAME" | cut -d: -f6)"

TMP_FILE="$(mktemp)"
sed \
  -e "s|__USER__|$USER_NAME|g" \
  -e "s|__GROUP__|$GROUP_NAME|g" \
  -e "s|__HOME_DIR__|$HOME_DIR|g" \
  -e "s|__ROOT_DIR__|$ROOT_DIR|g" \
  "$SERVICE_SRC" > "$TMP_FILE"

install -m 644 "$TMP_FILE" "$SERVICE_DST"
rm -f "$TMP_FILE"
systemctl daemon-reload
systemctl enable --now picoclaw-gateway.service
systemctl --no-pager --full status picoclaw-gateway.service
