#!/usr/bin/env bash

set -euo pipefail

echo "[i2c] read-mode scan on bus 1"
sudo i2cdetect -y -r 1

echo
echo "[i2c] direct address probes"
python3 - <<'PY'
import smbus

expected = [0x3c, 0x41, 0x60, 0x70]
bus = smbus.SMBus(1)

seen = []
for addr in expected:
    try:
        bus.read_byte(addr)
        seen.append(addr)
        print(f"{hex(addr)} ACK")
    except OSError:
        print(f"{hex(addr)} missing")

missing = [addr for addr in expected if addr not in seen]
if missing:
    raise SystemExit("Missing expected I2C addresses: " + ", ".join(hex(addr) for addr in missing))
PY
