#!/usr/bin/env python3
import json
import os
import socketserver
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from jetbot import Robot


def _json_response(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class JetBotController:
    def __init__(self):
        self.lock = threading.Lock()
        self.robot = None
        self.last_command = None
        self.started_at = time.time()
        self.max_speed = float(os.environ.get("JETBOT_AGENT_BRIDGE_MAX_SPEED", "0.35"))
        self.max_duration = float(os.environ.get("JETBOT_AGENT_BRIDGE_MAX_DURATION", "1.50"))

    def _ensure_robot(self):
        if self.robot is None:
            self.robot = Robot()
        return self.robot

    def _clip_speed(self, value):
        return max(-self.max_speed, min(self.max_speed, float(value)))

    def _clip_duration(self, value):
        return max(0.0, min(self.max_duration, float(value)))

    def _set_last(self, command, payload):
        self.last_command = {
            "command": command,
            "payload": payload,
            "timestamp": time.time(),
        }

    def health(self):
        return {
            "ok": True,
            "uptime_seconds": round(time.time() - self.started_at, 3),
        }

    def status(self):
        ready = True
        error = None
        try:
            self._ensure_robot()
        except Exception as exc:
            ready = False
            error = str(exc)
        return {
            "ok": ready,
            "robot_ready": ready,
            "error": error,
            "limits": {
                "max_speed": self.max_speed,
                "max_duration": self.max_duration,
            },
            "last_command": self.last_command,
        }

    def stop(self):
        with self.lock:
            robot = self._ensure_robot()
            robot.stop()
            payload = {}
            self._set_last("stop", payload)
            return {"ok": True, "stopped": True}

    def move(self, left, right, duration):
        clipped = {
            "left": self._clip_speed(left),
            "right": self._clip_speed(right),
            "duration": self._clip_duration(duration),
        }
        with self.lock:
            robot = self._ensure_robot()
            robot.left_motor.value = clipped["left"]
            robot.right_motor.value = clipped["right"]
            time.sleep(clipped["duration"])
            robot.stop()
            self._set_last("move", clipped)
            return {"ok": True, "executed": clipped}

    def sequence(self, steps):
        executed = []
        total_duration = 0.0
        sanitized = []
        for step in steps:
            sanitized_step = {
                "left": self._clip_speed(step.get("left", 0.0)),
                "right": self._clip_speed(step.get("right", 0.0)),
                "duration": self._clip_duration(step.get("duration", 0.0)),
            }
            total_duration += sanitized_step["duration"]
            sanitized.append(sanitized_step)
        if total_duration > self.max_duration * 4:
            raise ValueError("sequence duration is too long")
        with self.lock:
            robot = self._ensure_robot()
            for step in sanitized:
                robot.left_motor.value = step["left"]
                robot.right_motor.value = step["right"]
                time.sleep(step["duration"])
                robot.stop()
                executed.append(step)
                time.sleep(0.05)
            self._set_last("sequence", {"steps": executed})
            return {"ok": True, "executed": executed}


CONTROLLER = JetBotController()


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True


class Handler(BaseHTTPRequestHandler):
    server_version = "JetBotAgentBridge/0.1"

    def log_message(self, fmt, *args):
        return

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        try:
            if self.path == "/health":
                _json_response(self, 200, CONTROLLER.health())
                return
            if self.path == "/status":
                status = CONTROLLER.status()
                _json_response(self, 200 if status["ok"] else 503, status)
                return
            _json_response(self, 404, {"ok": False, "error": "not found"})
        except Exception as exc:
            _json_response(self, 500, {"ok": False, "error": str(exc)})

    def do_POST(self):
        try:
            if self.path == "/stop":
                _json_response(self, 200, CONTROLLER.stop())
                return
            payload = self._read_json()
            if self.path == "/move":
                result = CONTROLLER.move(
                    payload.get("left", 0.0),
                    payload.get("right", 0.0),
                    payload.get("duration", 0.0),
                )
                _json_response(self, 200, result)
                return
            if self.path == "/sequence":
                steps = payload.get("steps", [])
                if not isinstance(steps, list) or not steps:
                    raise ValueError("steps must be a non-empty list")
                _json_response(self, 200, CONTROLLER.sequence(steps))
                return
            _json_response(self, 404, {"ok": False, "error": "not found"})
        except ValueError as exc:
            _json_response(self, 400, {"ok": False, "error": str(exc)})
        except Exception as exc:
            _json_response(self, 500, {"ok": False, "error": str(exc)})


def main():
    host = os.environ.get("JETBOT_AGENT_BRIDGE_HOST", "127.0.0.1")
    port = int(os.environ.get("JETBOT_AGENT_BRIDGE_PORT", "8786"))
    server = ThreadingHTTPServer((host, port), Handler)
    print("jetbot-agent-bridge listening on %s:%s" % (host, port))
    server.serve_forever()


if __name__ == "__main__":
    main()
