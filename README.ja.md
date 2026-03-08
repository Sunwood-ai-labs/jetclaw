<div align="center">
  <img src="docs/public/images/jetclaw_icon.webp" alt="JetClaw icon" width="320">
  <h1>JetClaw</h1>
  <p>Waveshare JetBot 2GB に PicoClaw を載せて、Jetson Nano 2GB 上で軽量なエージェント制御を行うための統合リポジトリです。</p>
  <p>
    <img src="https://img.shields.io/badge/Waveshare-JetBot%202GB-222222?logo=databricks&logoColor=white" alt="Waveshare JetBot 2GB">
    <img src="https://img.shields.io/badge/Jetson%20Nano-2GB-76B900?logo=nvidia&logoColor=white" alt="Jetson Nano 2GB">
    <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python 3.x">
    <img src="https://img.shields.io/badge/PicoClaw-Agent%20Runtime-111827" alt="PicoClaw">
    <img src="https://img.shields.io/badge/VitePress-Docs-646CFF?logo=vite&logoColor=white" alt="VitePress Docs">
    <img src="https://img.shields.io/badge/GitHub%20Pages-Deployed-121013?logo=github&logoColor=white" alt="GitHub Pages">
  </p>
  <p>
    <a href="./README.md"><img src="https://img.shields.io/badge/Language-English-0F766E?style=for-the-badge" alt="English"></a>
    <a href="./README.ja.md"><img src="https://img.shields.io/badge/言語-日本語-B91C1C?style=for-the-badge" alt="日本語"></a>
  </p>
</div>

## 概要

JetClaw は次の 3 層をまとめて管理します。

- `jetbot/`: Waveshare 互換に調整した JetBot Python コードと notebooks
- `scripts/jetbot_agent_bridge.py`: モータ制御を安全に絞った localhost bridge
- `picoclaw/`: PicoClaw 用 systemd template、config template、workspace seed

検証環境:

- Jetson Nano 2GB Developer Kit
- Waveshare JetBot 2GB AI Kit
- Ubuntu 18.04 / L4T R32.7.1
- IMX219 camera
- PicoClaw `0.2.0`

## 構成

```text
Discord
  -> PicoClaw gateway (/usr/bin/picoclaw)
  -> localhost JetBot bridge (scripts/jetbot_agent_bridge.py)
  -> jetbot Python package
  -> Waveshare expansion board, motors, OLED, INA219, camera
```

重要事項:

- PicoClaw 本体は system binary として導入します
- この repo では service template、bridge、workspace seed、docs を管理します
- runtime state は `~/.picoclaw` に置きます

## ドキュメント

- セットアップ全体: [README.md](./README.md)
- Getting Started: [docs/getting_started.md](./docs/getting_started.md)
- Waveshare 固有情報: [docs/jetclaw/waveshare-jetbot-2gb.md](./docs/jetclaw/waveshare-jetbot-2gb.md)
- PicoClaw 連携: [docs/jetclaw/picoclaw.md](./docs/jetclaw/picoclaw.md)
- 運用手順: [docs/jetclaw/operations.md](./docs/jetclaw/operations.md)
- 公開 docs: https://sunwood-ai-labs.github.io/jetclaw/

## 最短手順

1. `./scripts/verify_waveshare_i2c.sh` で拡張ボードを確認
2. `./scripts/install_native_services.sh` で Jupyter / stats service を導入
3. `~/.picoclaw/` に config と workspace を展開
4. `sudo ./scripts/install_jetbot_agent_bridge_service.sh`
5. `sudo ./scripts/install_picoclaw_gateway_service.sh`
6. `python3 ~/.picoclaw/workspace/jetbot_bridge.py status` でロボット状態を確認
7. `python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse forward --speed 0.18 --duration 0.18` で短い動作確認

## 補足

- `kimi-k2.5` は Alibaba Cloud Model Studio / DashScope `coding-intl` 経由で使う想定です
- API key は `PICOCLAW_ALIBABA_API_KEY` を使います
- 詳細な手順と service path の確認方法は英語版 README と VitePress docs に揃えています
