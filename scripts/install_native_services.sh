#!/usr/bin/env bash

set -euo pipefail

PASSWORD="${1:-jetbot}"
WORKDIR="${2:-$PWD/notebooks}"
CONFIG_DIR="${HOME}/.jupyter"
CONFIG_FILE="${CONFIG_DIR}/jupyter_notebook_config.json"

mkdir -p "${CONFIG_DIR}"

python3 - "$PASSWORD" "$CONFIG_FILE" <<'PY'
from notebook.auth import passwd
import json
import os
import sys

password = sys.argv[1]
config_path = sys.argv[2]

try:
    with open(config_path) as f:
        config = json.load(f)
except Exception:
    config = {}

config.pop("NotebookApp", None)
config.setdefault("ServerApp", {})["password"] = passwd(password)

with open(config_path, "w") as f:
    json.dump(config, f, indent=2)

print(config_path)
PY

python3 jetbot/utils/create_jupyter_service.py --working_directory "${WORKDIR}" --output /tmp/jetbot_jupyter.service
python3 jetbot/utils/create_stats_service.py --output /tmp/jetbot_stats.service

sudo cp /tmp/jetbot_jupyter.service /etc/systemd/system/jetbot_jupyter.service
sudo cp /tmp/jetbot_stats.service /etc/systemd/system/jetbot_stats.service
sudo systemctl daemon-reload
sudo systemctl enable --now jetbot_jupyter.service jetbot_stats.service

echo "Installed:"
echo "  /etc/systemd/system/jetbot_jupyter.service"
echo "  /etc/systemd/system/jetbot_stats.service"
