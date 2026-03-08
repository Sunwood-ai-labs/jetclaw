# JetClaw

JetClaw is a local integration repo for giving a Waveshare JetBot 2GB a lightweight agent body with PicoClaw on Jetson Nano 2GB.

It combines:

- `jetbot/`: the JetBot Python stack and notebooks
- `scripts/jetbot_agent_bridge.py`: a safe localhost bridge for motor control
- `picoclaw/`: PicoClaw service templates, config templates, and workspace seed files

This layout was validated on:

- Jetson Nano 2GB
- Waveshare JetBot 2GB AI Kit
- IMX219 camera
- PicoClaw `0.2.0`

## What Lives Where

Tracked in this repo:

- JetBot source and notebooks
- Waveshare-specific notes
- PicoClaw systemd templates
- PicoClaw config template
- PicoClaw workspace seed files

Not tracked in this repo:

- `~/.picoclaw/config.json`
- `~/.picoclaw/picoclaw.env`
- PicoClaw sessions, memory, and runtime state
- Discord tokens or API keys

## Repository Layout

```text
jetclaw/
├─ jetbot/
├─ notebooks/
├─ scripts/
│  ├─ jetbot_agent_bridge.py
│  ├─ install_jetbot_agent_bridge_service.sh
│  ├─ install_picoclaw_gateway_service.sh
│  └─ sync_picoclaw_config.py
├─ picoclaw/
│  ├─ config/
│  │  ├─ config.template.json
│  │  └─ picoclaw.env.example
│  ├─ services/
│  │  └─ jetbot_agent_bridge.service
│  ├─ workspace/
│  │  ├─ AGENT.md
│  │  └─ jetbot_bridge.py
│  └─ picoclaw-gateway.service
└─ WAVESHARE_SETUP.md
```

## Quick Start

1. Install and validate the JetBot Python stack in this repo.
2. Install PicoClaw from the official release page.
3. Copy `picoclaw/config/config.template.json` to `~/.picoclaw/config.json`.
4. Copy `picoclaw/config/picoclaw.env.example` to `~/.picoclaw/picoclaw.env` and set:
   - `PICOCLAW_PROVIDERS_QWEN_API_KEY`
   - `PICOCLAW_CHANNELS_DISCORD_TOKEN`
   - `JETBOT_AGENT_BRIDGE_URL`
5. Copy `picoclaw/workspace/*` into `~/.picoclaw/workspace/`.
6. Install the bridge service:

```bash
sudo ./scripts/install_jetbot_agent_bridge_service.sh
```

7. Install the PicoClaw gateway service:

```bash
sudo ./scripts/install_picoclaw_gateway_service.sh
```

## Notes

- The Waveshare expansion board should be checked with `i2cdetect -y -r 1`.
- JetBot motion is intentionally clamped by the localhost bridge.
- PicoClaw runtime stays outside the repo so secrets and sessions do not get committed.

## Upstream

- NVIDIA JetBot: https://github.com/NVIDIA-AI-IOT/jetbot
- Sipeed PicoClaw: https://github.com/sipeed/picoclaw
