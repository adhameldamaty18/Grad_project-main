from core.event_bus import event_queue, containment_queue, dashboard_queue
from detection.risk_engine import RiskEngine
import datetime

class ThreatManager:
    def __init__(self):
        self.engine = RiskEngine()
        self.history = {}
        self.last_status = {}
        self.confirmed_rogues = set()

    def print_event(self, event_summary):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print("-" * 60)
        print(f"[{timestamp}] NEW ACCESS POINT DETECTED")
        print(f"SSID      : {event_summary['ssid']}")
        print(f"BSSID     : {event_summary['bssid']}")
        print(f"Channel   : {event_summary['channel']}")
        print(f"Status    : {event_summary['classification']}")
        print(f"Score     : {event_summary['score']}")
        print("-" * 60)

    def start(self):
        while True:
            event = event_queue.get()
            event_summary = self.engine.analyze(event)

            bssid = event_summary["bssid"]
            status = event_summary["classification"]
            score = event_summary["score"]
            reasons = event_summary["reasons"]

            if bssid not in self.history:
                self.history[bssid] = 1
            else:
                self.history[bssid] += 1

            if bssid not in self.last_status or self.last_status[bssid] != status:
                self.print_event(event_summary)
                self.last_status[bssid] = status

            # ✅ كل الكود داخل الـ if block بـ indentation صح
            if status in ["SUSPICIOUS", "ROGUE"]:
                threat = {
                    "status": status,
                    "score": score,
                    "reasons": reasons,
                    "event": event_summary
                }  # ✅ الـ closing brace جوه الـ if

                dashboard_queue.put(threat)  # ✅ جوه الـ if

                if status == "ROGUE" and bssid not in self.confirmed_rogues:
                    self.confirmed_rogues.add(bssid)
                    containment_queue.put(threat)  # ✅ مرة واحدة بس

                    print("\n🚨🚨🚨 ROGUE ACCESS POINT CONFIRMED 🚨🚨🚨")
                    print(f"SSID  : {event_summary['ssid']}")
                    print(f"BSSID : {event_summary['bssid']}")
                    print("=" * 60)