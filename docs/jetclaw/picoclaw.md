# PicoClaw Integration

JetClaw uses PicoClaw as the lightweight agent layer on top of the native JetBot stack.

## Runtime Layout

Tracked in this repo:

- `picoclaw/picoclaw-gateway.service`
- `picoclaw/services/jetbot_agent_bridge.service`
- `picoclaw/config/config.template.json`
- `picoclaw/config/picoclaw.env.example`
- `picoclaw/workspace/AGENT.md`
- `picoclaw/workspace/jetbot_bridge.py`

Runtime outside the repo:

- `~/.picoclaw/config.json`
- `~/.picoclaw/picoclaw.env`
- `~/.picoclaw/workspace/`
- sessions, memory, and state

## Model And Key Layout

The working `kimi-k2.5` path in this repo uses Alibaba Cloud Model Studio / DashScope `coding-intl`.

Set this in `~/.picoclaw/picoclaw.env`:

```text
PICOCLAW_ALIBABA_API_KEY=...
PICOCLAW_CHANNELS_DISCORD_TOKEN=...
JETBOT_AGENT_BRIDGE_URL=http://127.0.0.1:8786
```

`scripts/sync_picoclaw_config.py` injects the Alibaba key into every model entry that points at a `dashscope.aliyuncs.com` endpoint.

## Services

Install or refresh the generated unit files with:

```bash
sudo ./scripts/install_jetbot_agent_bridge_service.sh
sudo ./scripts/install_picoclaw_gateway_service.sh
```

The generated systemd units should point at this repo checkout:

- `.../scripts/jetbot_agent_bridge.py`
- `.../scripts/sync_picoclaw_config.py`

## Health Checks

Check service state:

```bash
systemctl status jetbot_agent_bridge.service --no-pager
systemctl status picoclaw-gateway.service --no-pager
```

Check HTTP health:

```bash
curl http://127.0.0.1:8786/health
curl http://127.0.0.1:18790/health
```

Check robot state as seen from the workspace helper:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py status
```

## Discord

The runtime config supports Discord through the PicoClaw gateway.

Review these fields in `~/.picoclaw/config.json`:

- `channels.discord.enabled`
- `channels.discord.allow_from`
- `channels.discord.mention_only`
- `gateway.host`
- `gateway.port`

Recommended first message:

```text
@your-bot reply with only OK
```

If Discord replies but the robot does not move, jump to [Operations](./operations.md).
