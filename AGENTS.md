# AGENTS.md

This repository contains a real robot control stack.

Read these first before making changes:

- `README.md` for end-to-end setup
- `docs/getting_started.md` for the short onboarding path
- `docs/jetclaw/waveshare-jetbot-2gb.md` for Waveshare hardware behavior
- `docs/jetclaw/picoclaw.md` for PicoClaw runtime and service layout
- `docs/jetclaw/operations.md` for safe robot operation

## Safety Rules

- Assume the robot is powered and physically capable of moving.
- Stop the robot before and after any movement test.
- Use short pulses by default.
- Do not raise bridge speed or duration limits unless the user explicitly asks.
- Do not commit secrets from `~/.picoclaw`.

## Canonical Commands

Bring up or verify the robot with:

```bash
./scripts/verify_waveshare_i2c.sh
./scripts/install_native_services.sh
sudo ./scripts/install_jetbot_agent_bridge_service.sh
sudo ./scripts/install_picoclaw_gateway_service.sh
systemctl status jetbot_agent_bridge.service --no-pager
systemctl status picoclaw-gateway.service --no-pager
curl http://127.0.0.1:8786/health
curl http://127.0.0.1:18790/health
```

Operate the robot conservatively with:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py status
python3 ~/.picoclaw/workspace/jetbot_bridge.py stop
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse forward --speed 0.18 --duration 0.18
```

## Documentation Rules

- Keep `README.md` and the VitePress docs aligned.
- Prefer linking back to `README.md` instead of duplicating long setup blocks.
- If service paths change, update both docs and install scripts in the same change.
