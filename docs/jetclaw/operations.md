# Operations

This page focuses on safe day-to-day operation once the robot and services are already installed.

## Before You Move The Robot

Always check:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py status
python3 ~/.picoclaw/workspace/jetbot_bridge.py stop
```

If the bridge reports an error, fix that before any movement command.

## Safe Motion Primitives

Short forward pulse:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse forward --speed 0.18 --duration 0.18
```

Other directions:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse backward --speed 0.18 --duration 0.18
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse left --speed 0.18 --duration 0.18
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse right --speed 0.18 --duration 0.18
```

Stop immediately:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py stop
```

The bridge clamps motion to:

- max speed `0.35`
- max single duration `1.50s`

## Service Management

Restart services after changing repo paths, templates, or runtime config:

```bash
sudo systemctl restart jetbot_agent_bridge.service
sudo systemctl restart picoclaw-gateway.service
```

Check the generated unit files:

```bash
systemctl cat jetbot_agent_bridge.service
systemctl cat picoclaw-gateway.service
```

If they still point at an old checkout, rerun the install scripts.

## Recovery Path

If anything feels off:

1. stop the robot
2. check bridge health
3. check gateway health
4. rerun the I2C probe
5. restart services

Commands:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py stop
curl http://127.0.0.1:8786/health
curl http://127.0.0.1:18790/health
./scripts/verify_waveshare_i2c.sh
sudo systemctl restart jetbot_agent_bridge.service picoclaw-gateway.service
```

## Where To Edit What

- hardware behavior: [Waveshare JetBot 2GB](./waveshare-jetbot-2gb.md)
- agent/runtime behavior: [PicoClaw Integration](./picoclaw.md)
- full install path: [README](https://github.com/Sunwood-ai-labs/jetclaw/blob/main/README.md)
