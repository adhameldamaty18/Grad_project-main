import os
import socketio
import threading
import time
from core.event_bus import dashboard_queue

class WSClient:


 def __init__(self, backend_url=None, token=None):

    self.backend_url = backend_url or os.getenv("BACKEND_URL", "http://127.0.0.1:5000")

    # token optional
    self.token = token or os.getenv("SENSOR_TOKEN", None)

    self.is_running = False

    self.sio = socketio.Client(
        logger=True,
        engineio_logger=True,
        reconnection=True,
        reconnection_attempts=5,
        reconnection_delay=2
    )

    @self.sio.event
    def connect():
        print("\n[WebSocket] 🟢 Connected to ZeinaGuard Backend!")

    @self.sio.event
    def disconnect():
        print("\n[WebSocket] 🔴 Disconnected from server.")

def connect_to_server(self):

    try:

        print(f"[WebSocket] Connecting to {self.backend_url} ...")

        self.sio.connect(
            self.backend_url,
            transports=["websocket"]
        )

        self.is_running = True

        listener_thread = threading.Thread(
            target=self._threat_listener,
            daemon=True
        )

        listener_thread.start()

        self.sio.wait()

    except Exception as e:
        print(f"[WebSocket] Connection Error: {e}")

def _threat_listener(self):

    print("[WebSocket] Listening for threats...")

    while self.is_running:

        threat = dashboard_queue.get()

        try:
            self.sio.emit("new_threat", threat)
            print(f"[WebSocket] 🚀 Threat sent: {threat['event']['ssid']}")
        except Exception as e:
            print(f"[WebSocket] Failed to send threat: {e}")

        time.sleep(0.05)

def disconnect_server(self):

    self.is_running = False
    self.sio.disconnect()