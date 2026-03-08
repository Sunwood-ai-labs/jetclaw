# Waveshare JetBot 2GB Setup Notes

These notes capture the working setup that was validated on:

- Jetson Nano 2GB Developer Kit
- Waveshare JetBot 2GB AI Kit
- Ubuntu 18.04 / L4T R32.7.1

## Key differences from upstream JetBot

The Waveshare kit is not a drop-in match for the upstream NVIDIA JetBot repository.

- The Waveshare expansion board exposes devices that are expected by the Waveshare fork.
- `qwiic.scan()` based detection is not a reliable probe for this kit.
- `i2cdetect -y 1` can appear empty on this kit because of the SMBus quick-write probe.
- `i2cdetect -y -r 1` is the reliable check.

Validated addresses on the working kit:

- `0x3c` OLED
- `0x41` INA219 power monitor
- `0x60` motor controller
- `0x70` additional I2C device on the expansion board

## Power notes

If the expansion board power switch turns the Jetson Nano on, the board power path is active.

The 6-pin cable between the Jetson Nano and the expansion board carries both power rails and I2C:

- `3V3`
- `SDA`
- `SCL`
- `5V`
- `5V`
- `GND`

If the Nano boots but I2C is empty, inspect that 6-pin cable first.

## Repository state

These files were aligned with the Waveshare `jetbot_0.4.2` branch:

- `jetbot/robot.py`
- `jetbot/motor.py`
- `jetbot/ads1115.py`
- `jetbot/ina219.py`
- `jetbot/apps/stats.py`

This repository also keeps a small local compatibility guard in `jetbot/__init__.py` so JetBot can still import when the TensorRT / PyTorch object detection stack is not installed.

## Jupyter and stats services

The working setup uses:

- `jetbot_jupyter.service`
- `jetbot_stats.service`

The helper script below regenerates and installs both services:

```bash
./scripts/install_native_services.sh
```

Default Jupyter password:

```text
jetbot
```

## Verify the board

Run:

```bash
./scripts/verify_waveshare_i2c.sh
```

Expected output includes:

- `0x3c`
- `0x41`
- `0x60`

## Quick motor pulse

Use a short pulse first:

```bash
python3 - <<'PY'
import time
from jetbot import Robot

robot = Robot()
try:
    robot.set_motors(0.18, 0.18)
    time.sleep(0.15)
finally:
    robot.stop()
PY
```
