# Architecture

This page gives a rough view of the validated JetClaw stack and points at the editable draw.io source kept in the repository.

## Editable Diagram

Open the XML directly in draw.io or diagrams.net:

- [jetclaw-architecture.drawio](/diagrams/jetclaw-architecture.drawio)

## Stack Overview

```text
Discord operator
  -> PicoClaw gateway service
  -> ~/.picoclaw runtime config and workspace helper
  -> localhost JetBot bridge
  -> jetbot Python package
  -> Waveshare expansion board and robot hardware
```

## Main Layers

- Control entry: Discord reaches the PicoClaw gateway running as the system `picoclaw` binary.
- Runtime state: `~/.picoclaw` stores the generated config, secrets, workspace helper, and other runtime data that should stay out of git.
- Safe motion boundary: `scripts/jetbot_agent_bridge.py` exposes a localhost-only bridge and clamps motion to conservative limits.
- Robot software: the `jetbot/` package owns the Python behavior that talks to the Waveshare-compatible hardware stack.
- Hardware: the validated build uses a Jetson Nano 2GB Developer Kit inside a Waveshare JetBot 2GB AI Kit with the expansion board, motors, OLED, INA219, IMX219 camera, speaker, and microphone.

## Purchasing Context

If you are collecting parts for the same build, use [Waveshare JetBot 2GB](./waveshare-jetbot-2gb.md). That page includes the validated shopping notes for the Waveshare JetBot 2GB AI Kit and the Jetson Nano 2GB Developer Kit.
