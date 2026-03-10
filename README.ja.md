<div align="center">
  <img src="docs/public/images/jetclaw_icon.webp" alt="JetClaw icon" width="320">
  <h1>JetClaw</h1>
  <p>Waveshare JetBot 2GB を Jetson Nano 2GB 上で PicoClaw と統合し、軽量なエージェントとして運用するためのリポジトリです。</p>
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

JetClaw は、実機の JetBot 制御と PicoClaw エージェント実行を同じ構成で扱えるようにするための統合リポジトリです。

この repo で管理しているのは主に次の 3 層です。

- `jetbot/`: Waveshare JetBot 2GB 向けに調整した JetBot Python コードと notebooks
- `scripts/jetbot_agent_bridge.py`: モータ制御を安全な範囲に制限した localhost bridge
- `picoclaw/`: PicoClaw の service template、config template、workspace seed

検証済み構成:

- Jetson Nano 2GB Developer Kit
- Waveshare JetBot 2GB AI Kit
- Ubuntu 18.04 / L4T R32.7.1
- IMX219 camera
- PicoClaw `0.2.0`

## アーキテクチャ

```text
Discord
  -> PicoClaw gateway (/usr/bin/picoclaw)
  -> localhost JetBot bridge (scripts/jetbot_agent_bridge.py)
  -> jetbot Python package
  -> Waveshare expansion board, motors, OLED, INA219, camera
```

重要な前提:

- PicoClaw 本体は repo に同梱せず、system binary として導入します
- この repo は service、bridge、workspace seed、docs を管理します
- runtime state は `~/.picoclaw` に置きます
- 秘密情報やセッション状態は repo に commit しません

## 検証済みハードウェア構成

今回の構成では、次の 2 点を主役のハードウェアとして使っています。

### 1. Waveshare JetBot 2GB AI Kit

今回のセットアップの主役です。Jetson Nano 2GB 専用のロボットキットで、拡張ボード、カメラ、OLED、スピーカー、マイクなどが一式入っています。

購入前の注意:

- Jetson Nano 2GB 専用です。4GB 版には対応していません。
- `18650` 電池 3 本は別売りです。
- 電池の長さは `67 mm` 未満を推奨します。保護回路付きセルは長すぎて入らない場合があります。
- Jetson Nano 2GB 本体も別売りです。

| 項目 | 内容 |
| --- | --- |
| 参考価格 | `¥26,182`（税込） |
| 出品者 | Amazon 経由 EIKO SHOP |
| 在庫 | 残りわずかになる場合あり |

購入リンク:

- [Waveshare JetBot 2GB AI Kit を Amazon.co.jp で見る](https://www.amazon.jp/dp/B08R5WNSYR?ref=ppx_pop_mob_ap_share)

### 2. NVIDIA Jetson Nano 2GB 開発者キット

JetBot の頭脳部分です。Jetson Nano 2GB を別途用意して、上のキットと組み合わせます。

購入前の注意:

- `microSD` カードは別売りです。`64GB` 以上を推奨します。
- `5V/4A` の電源アダプタも別売りです。ただし拡張ボード経由で給電する構成では不要な場合があります。
- Jetson Nano 2GB は生産終了品なので、在庫状況は要確認です。

| 項目 | 内容 |
| --- | --- |
| 参考価格 | `¥25,800`（税込） |
| 備考 | 生産終了品のため在庫が限られる場合あり |

購入リンク:

- [Jetson Nano 2GB 開発者キットを Amazon.co.jp で見る](https://amzn.asia/d/068WVBvj)

上の価格と在庫メモは、今回の検証構成に使った購入メモをそのまま残した参考情報です。実際の価格や在庫は変動する前提で見てください。

## 編集可能な構成図

draw.io でそのまま開ける XML はここに置いてあります。

- [docs/public/diagrams/jetclaw-architecture.drawio](./docs/public/diagrams/jetclaw-architecture.drawio)

ブラウザで見やすい説明ページは次です。

- [docs/jetclaw/architecture.md](./docs/jetclaw/architecture.md)

## ドキュメント

詳細は以下を見てください。

- 全体手順: [README.md](./README.md)
- クイックスタート: [docs/getting_started.md](./docs/getting_started.md)
- 構成図: [docs/jetclaw/architecture.md](./docs/jetclaw/architecture.md)
- Waveshare JetBot 2GB 固有情報: [docs/jetclaw/waveshare-jetbot-2gb.md](./docs/jetclaw/waveshare-jetbot-2gb.md)
- PicoClaw 連携: [docs/jetclaw/picoclaw.md](./docs/jetclaw/picoclaw.md)
- 運用手順: [docs/jetclaw/operations.md](./docs/jetclaw/operations.md)
- 公開ドキュメント: https://sunwood-ai-labs.github.io/jetclaw/

## 最短セットアップ

1. Waveshare 拡張ボードの I2C を確認

```bash
./scripts/verify_waveshare_i2c.sh
```

2. JetBot の native service を導入

```bash
./scripts/install_native_services.sh
```

3. PicoClaw の runtime ディレクトリを準備

```bash
mkdir -p ~/.picoclaw/workspace
cp picoclaw/config/config.template.json ~/.picoclaw/config.json
cp picoclaw/config/picoclaw.env.example ~/.picoclaw/picoclaw.env
cp picoclaw/workspace/AGENT.md ~/.picoclaw/workspace/AGENT.md
cp picoclaw/workspace/jetbot_bridge.py ~/.picoclaw/workspace/jetbot_bridge.py
chmod +x ~/.picoclaw/workspace/jetbot_bridge.py
```

4. PicoClaw 用の環境変数を設定

- `PICOCLAW_ALIBABA_API_KEY`
- `PICOCLAW_CHANNELS_DISCORD_TOKEN`
- `JETBOT_AGENT_BRIDGE_URL=http://127.0.0.1:8786`

5. service をインストール

```bash
sudo ./scripts/install_jetbot_agent_bridge_service.sh
sudo ./scripts/install_picoclaw_gateway_service.sh
```

6. health check と状態確認

```bash
systemctl status jetbot_agent_bridge.service --no-pager
systemctl status picoclaw-gateway.service --no-pager
curl http://127.0.0.1:8786/health
curl http://127.0.0.1:18790/health
python3 ~/.picoclaw/workspace/jetbot_bridge.py status
```

## 安全な動作確認

まず停止:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py stop
```

短い前進パルス:

```bash
python3 ~/.picoclaw/workspace/jetbot_bridge.py pulse forward --speed 0.18 --duration 0.18
```

bridge 側の制限:

- 最大速度: `0.35`
- 1 回あたりの最大時間: `1.50s`

## 補足

- `kimi-k2.5` は Alibaba Cloud Model Studio / DashScope `coding-intl` 経由で使う前提です
- 使う API key 名は `PICOCLAW_ALIBABA_API_KEY` です
- docs は VitePress で管理し、GitHub Pages へ自動デプロイしています
