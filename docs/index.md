---
layout: home

hero:
  name: JetClaw
  text: Waveshare JetBot 2GB with a lightweight agent body
  tagline: VitePress docs for JetBot, PicoClaw, Waveshare bring-up, and safe robot operations on Jetson Nano 2GB.
  image:
    src: /images/jetclaw_icon.webp
    alt: JetClaw icon
  actions:
    - theme: brand
      text: Get Started
      link: /getting_started
    - theme: alt
      text: Waveshare Guide
      link: /jetclaw/waveshare-jetbot-2gb
    - theme: alt
      text: PicoClaw Guide
      link: /jetclaw/picoclaw

features:
  - title: Waveshare-aware bring-up
    details: Validate the 2GB AI Kit with read-mode I2C probing, the known device addresses, and the 6-pin cable checks that matter on this hardware.
  - title: Safe local robot control
    details: Use the localhost bridge and the workspace helper to stop, inspect, and pulse the robot without exposing raw motor control directly to the agent.
  - title: PicoClaw on low-RAM Jetson
    details: Keep PicoClaw as a system binary and runtime data under ~/.picoclaw while versioning the service templates, bridge script, and docs in this repo.
---

## What You Get Here

JetClaw combines three layers that have to stay aligned:

- the Waveshare-compatible JetBot Python stack
- the PicoClaw service and runtime glue
- the docs and operational rules for a real robot

If you are new to the project, start with [Getting Started](/getting_started). If the robot hardware is already on your desk, go straight to [Waveshare JetBot 2GB](/jetclaw/waveshare-jetbot-2gb). If PicoClaw is the missing piece, use [PicoClaw Integration](/jetclaw/picoclaw).
