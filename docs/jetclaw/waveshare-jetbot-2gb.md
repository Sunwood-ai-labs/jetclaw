# Waveshare JetBot 2GB

This page captures the hardware-specific behavior that matters for the Waveshare JetBot 2GB AI Kit.

## Validated Purchase Notes

The validated JetClaw build in this repository uses this two-part hardware set:

### Waveshare JetBot 2GB AI Kit

This is the main robot kit. It includes the expansion board, camera, OLED, speaker, microphone, and the main robot chassis parts for a Jetson Nano 2GB build.

Before ordering:

- Jetson Nano 2GB only; this kit is not for the 4GB developer kit.
- Three `18650` cells are sold separately.
- Keep battery length under `67 mm`; protected cells may not fit.
- The Jetson Nano 2GB board is sold separately.

| Item | Details |
| --- | --- |
| Reference price | `JPY 26,182` (tax included) |
| Seller | EIKO SHOP via Amazon Japan |
| Stock note | Sometimes low stock |

Link:

- [Waveshare JetBot 2GB AI Kit on Amazon Japan](https://www.amazon.jp/dp/B08R5WNSYR?ref=ppx_pop_mob_ap_share)

### NVIDIA Jetson Nano 2GB Developer Kit

This is the compute board used as the controller for the robot.

Before ordering:

- A `microSD` card is sold separately; `64 GB` or larger is recommended.
- A `5V/4A` power adapter is sold separately, although you may not need it when powering through the expansion board path.
- Jetson Nano 2GB is discontinued, so stock can be limited.

| Item | Details |
| --- | --- |
| Reference price | `JPY 25,800` (tax included) |
| Note | Discontinued product with limited stock |

Link:

- [Jetson Nano 2GB Developer Kit on Amazon Japan](https://amzn.asia/d/068WVBvj)

These price and availability notes are reference values from the validated shopping list and may change.

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

For the editable system overview, open [Architecture](./architecture.md). For the end-to-end path, see the root [README](https://github.com/Sunwood-ai-labs/jetclaw/blob/main/README.md).
