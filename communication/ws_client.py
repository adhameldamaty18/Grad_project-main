import socketio
import threading
import time
from core.event_bus import threat_queue

class WSClient:
    def __init__(self, backend_url="http://192.168.1.100:5000", token=None):
        self.sio = socketio.Client()
        self.backend_url = backend_url
        self.token = token
        self.is_running = False

        # إعداد الأحداث (Events)
        @self.sio.event
        def connect():
            print("\n[WebSocket] 🟢 Connected to ZeinaGuard Dashboard!")

        @self.sio.event
        def disconnect():
            print("\n[WebSocket] 🔴 Disconnected from server.")

    def connect_to_server(self):
        if not self.token:
            print("[WebSocket] Cannot connect without JWT Token.")
            return

        try:
            # بنبعت الـ Token في الـ Headers عشان الـ Backend يتأكد من هويتنا
            self.sio.connect(
                self.backend_url, 
                headers={'Authorization': f'Bearer {self.token}'}
            )
            self.is_running = True
            
            # بنشغل Thread يفضل يراقب الطابور ويبعت التهديدات
            listener_thread = threading.Thread(target=self._threat_listener, daemon=True)
            listener_thread.start()
            
            # بنخلي الـ Client شغال
            self.sio.wait()
            
        except Exception as e:
            print(f"[WebSocket] Connection Error: {e}")

    def _threat_listener(self):
        """Thread منفصل بيسحب من الـ Queue ويبعت للسيرفر"""
        print("[WebSocket] Started listening for threats to broadcast...")
        while self.is_running:
            if not threat_queue.empty():
                threat = threat_queue.get()
                
                # بنبعت الـ Threat للـ Backend على Event اسمه 'new_threat'
                try:
                    self.sio.emit('new_threat', threat)
                    print(f"[WebSocket] 🚀 Threat sent to Dashboard: {threat['event']['ssid']}")
                except Exception as e:
                    print(f"[WebSocket] Failed to send threat: {e}")
            
            time.sleep(0.1) # عشان ما نستهلكش البروسيسور (CPU)

    def disconnect_server(self):
        self.is_running = False
        self.sio.disconnect()