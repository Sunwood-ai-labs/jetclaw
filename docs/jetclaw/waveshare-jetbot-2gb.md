# Waveshare JetBot 2GB

This page captures the hardware-specific behavior that matters for the Waveshare JetBot 2GB AI Kit.

## Why It Is Different

The Waveshare kit is not a drop-in match for upstream NVIDIA JetBot.

Key differences:

- the expansion board exposes a different I2C layout
- `qwiic.scan()` is not a reliable probe for this kit
- plain `i2cdetect -y 1` can appear empty even when the board is alive
- `i2cdetect -y -r 1` is the reliable probe

## Known Good I2C Addresses

Validated on the working kit:

- `0x3c` OLED
- `0x41` INA219 power monitor
- `0x60` motor controller
- `0x70` extra expansion board device

Use the helper script:

```bash
./scripts/verify_waveshare_i2c.sh
```

## Power And Wiring Notes

If the expansion board power switch turns the Jetson Nano on, the board power path is active.

The 6-pin cable between the Nano and the expansion board carries both power and I2C:

- `3V3`
- `SDA`
- `SCL`
- `5V`
- `5V`
- `GND`

If the Nano boots but I2C is empty, inspect that 6-pin cable first.

## Files Aligned For Waveshare

These files were matched to the Waveshare `jetbot_0.4.2` behavior:

- `jetbot/robot.py`
- `jetbot/motor.py`
- `jetbot/ads1115.py`
- `jetbot/ina219.py`
- `jetbot/apps/stats.py`

A small compatibility guard is also kept in `jetbot/__init__.py` so the package can still import when the object detection stack is not installed.

## Local Validation Flow

1. Run `./scripts/verify_waveshare_i2c.sh`.
2. Install Jupyter and stats with `./scripts/install_native_services.sh`.
3. Check the bridge with `curl http://127.0.0.1:8786/health`.
4. Run a short motion pulse.

Short pulse example:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py stop
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse forward --speed 0.18 --duration 0.18
```

For the end-to-end path, see the root [README](https://github.com/Sunwood-ai-labs/jetclaw/blob/main/README.md).
