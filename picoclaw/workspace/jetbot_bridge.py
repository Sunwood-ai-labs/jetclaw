#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request


BRIDGE_URL = os.environ.get("JETBOT_AGENT_BRIDGE_URL", "http://127.0.0.1:8786")


def request(path, payload=None):
    url = BRIDGE_URL + path
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(resp.read().decode())
            return 0
    except urllib.error.HTTPError as exc:
        body = exc.read().decode()
        print(body or str(exc), file=sys.stderr)
        return 1
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1


def clamp_speed(value):
    return max(min(value, 0.35), -0.35)


def clamp_duration(value):
    return max(min(value, 1.5), 0.0)


def build_parser():
    parser = argparse.ArgumentParser(description="JetBot bridge helper")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status")
    sub.add_parser("stop")

    move = sub.add_parser("move")
    move.add_argument("--left", type=float, required=True)
    move.add_argument("--right", type=float, required=True)
    move.add_argument("--duration", type=float, required=True)

    pulse = sub.add_parser("pulse")
    pulse.add_argument("direction", choices=["forward", "backward", "left", "right"])
    pulse.add_argument("--speed", type=float, default=0.18)
    pulse.add_argument("--duration", type=float, default=0.18)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "command", None):
        parser.print_help(sys.stderr)
        return 2

    if args.command == "status":
        return request("/status")
    if args.command == "stop":
        return request("/stop", {})
    if args.command == "move":
        payload = {
            "left": clamp_speed(args.left),
            "right": clamp_speed(args.right),
            "duration": clamp_duration(args.duration),
        }
        return request("/move", payload)

    speed = clamp_speed(args.speed)
    duration = clamp_duration(args.duration)
    directions = {
        "forward": (speed, speed),
        "backward": (-speed, -speed),
        "left": (-speed, speed),
        "right": (speed, -speed),
    }
    left, right = directions[args.direction]
    payload = {"left": left, "right": right, "duration": duration}
    return request("/move", payload)


if __name__ == "__main__":
    sys.exit(main())
