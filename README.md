# JetClaw

JetClaw gives a Waveshare JetBot 2GB a lightweight agent body with PicoClaw on a Jetson Nano 2GB.

This repo keeps the parts that should be versioned together:

- `jetbot/`: JetBot Python code and notebooks
- `scripts/jetbot_agent_bridge.py`: safe localhost bridge for motor control
- `picoclaw/`: PicoClaw service templates, config template, and workspace seed files

This layout was validated on:

- Jetson Nano 2GB Developer Kit
- Waveshare JetBot 2GB AI Kit
- Ubuntu 18.04 / L4T R32.7.1
- IMX219 camera
- PicoClaw `0.2.0`

## Architecture

```text
Discord
  -> PicoClaw gateway (/usr/bin/picoclaw)
  -> localhost JetBot bridge (scripts/jetbot_agent_bridge.py)
  -> jetbot Python package
  -> Waveshare expansion board, motors, OLED, INA219, camera
```

Important detail:

- PicoClaw itself is installed as a system binary
- this repo owns the service templates, bridge script, workspace seed, and config template
- runtime state lives in `~/.picoclaw`

## What This Repo Tracks

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
│  ├─ install_jetbot_agent_bridge_service.sh
│  ├─ install_native_services.sh
│  ├─ install_picoclaw_gateway_service.sh
│  ├─ jetbot_agent_bridge.py
│  ├─ sync_picoclaw_config.py
│  └─ verify_waveshare_i2c.sh
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

## Before You Start

This repo assumes:

- the Jetson Nano 2GB already boots normally
- the Waveshare expansion board is wired correctly
- the IMX219 camera is already recognized by the Jetson
- PicoClaw is installed from the official release page

If the robot is not proven yet, read [WAVESHARE_SETUP.md](./WAVESHARE_SETUP.md) first.

## 1. Clone The Repo

```bash
cd ~/Prj
git clone https://github.com/Sunwood-ai-labs/jetclaw.git
cd jetclaw
```

The install scripts template the current repo path into the systemd unit files, so cloning to a stable path is a good idea.

## 2. Verify The Waveshare Board

Use read-mode I2C probing. On this kit, plain `i2cdetect -y 1` can be misleading.

```bash
./scripts/verify_waveshare_i2c.sh
```

Expected addresses on a working board:

- `0x3c` OLED
- `0x41` INA219
- `0x60` motor controller
- `0x70` expansion board device

If this step fails, do not continue to PicoClaw yet. Fix the robot first.

## 3. Bring Up Native JetBot Services

Install the local Jupyter and stats services:

```bash
./scripts/install_native_services.sh
```

Default Jupyter password:

```text
jetbot
```

These services are optional for PicoClaw, but they are useful for validating the robot before adding the agent layer.

## 4. Install PicoClaw

Install PicoClaw from the official release page for your architecture, then verify the binary exists:

```bash
picoclaw --version
which picoclaw
```

Expected binary path:

```text
/usr/bin/picoclaw
```

This repo does not vendor PicoClaw source or build it locally.

## 5. Create The PicoClaw Runtime Directory

```bash
mkdir -p ~/.picoclaw/workspace
cp picoclaw/config/config.template.json ~/.picoclaw/config.json
cp picoclaw/config/picoclaw.env.example ~/.picoclaw/picoclaw.env
cp picoclaw/workspace/AGENT.md ~/.picoclaw/workspace/AGENT.md
cp picoclaw/workspace/jetbot_bridge.py ~/.picoclaw/workspace/jetbot_bridge.py
chmod +x ~/.picoclaw/workspace/jetbot_bridge.py
```

## 6. Fill In Secrets And Channel Settings

Edit `~/.picoclaw/picoclaw.env` and set:

- `PICOCLAW_ALIBABA_API_KEY`
- `PICOCLAW_CHANNELS_DISCORD_TOKEN`
- `JETBOT_AGENT_BRIDGE_URL`

Default bridge URL:

```text
http://127.0.0.1:8786
```

Then edit `~/.picoclaw/config.json` and review at least:

- `agents.defaults.model`
- `channels.discord.enabled`
- `channels.discord.allow_from`
- `channels.discord.mention_only`
- `gateway.host`
- `gateway.port`

`PICOCLAW_ALIBABA_API_KEY` is the expected key name here because `kimi-k2.5` is being called through Alibaba Cloud Model Studio / DashScope `coding-intl`.

`sync_picoclaw_config.py` injects the API key and Discord token from `~/.picoclaw/picoclaw.env` into `~/.picoclaw/config.json` when the service starts.

## 7. Install The Services

Install the JetBot bridge:

```bash
sudo ./scripts/install_jetbot_agent_bridge_service.sh
```

Install the PicoClaw gateway:

```bash
sudo ./scripts/install_picoclaw_gateway_service.sh
```

These scripts generate:

- `/etc/systemd/system/jetbot_agent_bridge.service`
- `/etc/systemd/system/picoclaw-gateway.service`

## 8. Verify The Services

Check service health:

```bash
systemctl status jetbot_agent_bridge.service --no-pager
systemctl status picoclaw-gateway.service --no-pager
```

Check that the installed unit files point to this repo:

```bash
systemctl cat jetbot_agent_bridge.service
systemctl cat picoclaw-gateway.service
```

You should see this repo path in the generated unit files:

- `<repo-root>/scripts/jetbot_agent_bridge.py`
- `<repo-root>/scripts/sync_picoclaw_config.py`

Check localhost health endpoints:

```bash
curl http://127.0.0.1:8786/health
curl http://127.0.0.1:18790/health
```

Check PicoClaw's view of the robot:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py status
```

## 9. Run A Safe Motion Test

Stop first:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py stop
```

Then send a short forward pulse:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse forward --speed 0.18 --duration 0.18
```

The bridge clamps motion to conservative limits:

- max speed: `0.35`
- max single duration: `1.50s`

## 10. Try Discord

If Discord is enabled in `~/.picoclaw/config.json`, mention the bot in an allowed channel and send a short message.

Recommended first check:

```text
@your-bot reply with only OK
```

If that works, the agent path is live.

## Troubleshooting

- `i2cdetect -y 1` is not enough on the Waveshare kit. Use `i2cdetect -y -r 1` or `./scripts/verify_waveshare_i2c.sh`.
- If `systemctl cat ...` still points at an old repo path, rerun both install scripts and then `sudo systemctl restart jetbot_agent_bridge picoclaw-gateway`.
- If `picoclaw-gateway` is running but Discord does not answer, check `channels.discord.allow_from`, `mention_only`, and the bot token in `~/.picoclaw/picoclaw.env`.
- If the bridge health check works but motion fails, run `python3 ~/.picoclaw/workspace/jetbot_bridge.py status` and inspect the reported error.

## Upstream

- NVIDIA JetBot: https://github.com/NVIDIA-AI-IOT/jetbot
- Sipeed PicoClaw: https://github.com/sipeed/picoclaw
