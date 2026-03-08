#!/usr/bin/env python3
import json
import os
from pathlib import Path


HOME_DIR = Path(os.environ.get("HOME", str(Path.home())))
PICOCLAW_HOME = Path(os.environ.get("PICOCLAW_HOME", str(HOME_DIR / ".picoclaw")))
ENV_PATH = Path(os.environ.get("PICOCLAW_ENV_PATH", str(PICOCLAW_HOME / "picoclaw.env")))
CONFIG_PATH = Path(os.environ.get("PICOCLAW_CONFIG", str(PICOCLAW_HOME / "config.json")))


def read_env(path: Path):
    data = {}
    if not path.exists():
        return data
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key] = value
    return data


def main():
    env = read_env(ENV_PATH)
    config = json.loads(CONFIG_PATH.read_text())

    alibaba_key = env.get("PICOCLAW_ALIBABA_API_KEY", "")
    discord_token = env.get("PICOCLAW_CHANNELS_DISCORD_TOKEN", "")

    for item in config.get("model_list", []):
        api_base = item.get("api_base", "")
        if "dashscope.aliyuncs.com" in api_base:
            item["api_key"] = alibaba_key

    discord_cfg = config.setdefault("channels", {}).setdefault("discord", {})
    if discord_token:
        discord_cfg["token"] = discord_token

    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")


if __name__ == "__main__":
    main()
