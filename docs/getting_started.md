# Getting Started

This is the shortest path for bringing up JetClaw on a real Waveshare JetBot 2GB.

For the full step-by-step commands, use the root [README](https://github.com/Sunwood-ai-labs/jetclaw/blob/main/README.md). This page stays shorter on purpose and points you at the right checks in the right order.

## 1. Confirm The Hardware First

Do not start with PicoClaw if the robot itself is not proven.

Run:

```bash
./scripts/verify_waveshare_i2c.sh
```

Expected addresses:

- `0x3c`
- `0x41`
- `0x60`
- `0x70`

If the board does not answer here, use [Waveshare JetBot 2GB](./jetclaw/waveshare-jetbot-2gb.md).

## 2. Bring Up Native JetBot Services

Install the local Jupyter and stats services:

```bash
./scripts/install_native_services.sh
```

Default Jupyter password:

```text
jetbot
```

## 3. Prepare PicoClaw Runtime

Create the runtime directory and copy the tracked templates:

```bash
mkdir -p ~/.picoclaw/workspace
cp picoclaw/config/config.template.json ~/.picoclaw/config.json
cp picoclaw/config/picoclaw.env.example ~/.picoclaw/picoclaw.env
cp picoclaw/workspace/AGENT.md ~/.picoclaw/workspace/AGENT.md
cp picoclaw/workspace/jetbot_bridge.py ~/.picoclaw/workspace/jetbot_bridge.py
chmod +x ~/.picoclaw/workspace/jetbot_bridge.py
```

Set these values in `~/.picoclaw/picoclaw.env`:

- `PICOCLAW_ALIBABA_API_KEY`
- `PICOCLAW_CHANNELS_DISCORD_TOKEN`
- `JETBOT_AGENT_BRIDGE_URL=http://127.0.0.1:8786`

The expected Kimi path in this repo is Alibaba Cloud Model Studio / DashScope `coding-intl`.

## 4. Install Services

```bash
sudo ./scripts/install_jetbot_agent_bridge_service.sh
sudo ./scripts/install_picoclaw_gateway_service.sh
```

## 5. Verify Service Paths And Health

```bash
systemctl cat jetbot_agent_bridge.service
systemctl cat picoclaw-gateway.service
curl http://127.0.0.1:8786/health
curl http://127.0.0.1:18790/health
python3 ~/.picoclaw/workspace/jetbot_bridge.py status
```

The installed unit files should point at this repo path, not an older checkout.

## 6. Use A Short Motion Test

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py stop
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse forward --speed 0.18 --duration 0.18
```

For deeper explanations, use:

- [README](https://github.com/Sunwood-ai-labs/jetclaw/blob/main/README.md)
- [Waveshare JetBot 2GB](./jetclaw/waveshare-jetbot-2gb.md)
- [PicoClaw Integration](./jetclaw/picoclaw.md)
- [Operations](./jetclaw/operations.md)
