import requests

class APIClient:
    def __init__(self, backend_url="http://192.168.1.100:5000"):
        # حط هنا الـ IP بتاع السيرفر اللي عليه Flask
        self.backend_url = backend_url
        self.token = None

    def authenticate_sensor(self, sensor_id="sensor_01", secret_key="super_secret"):
        """بيسجل دخول السنسور وياخد الـ JWT Token"""
        url = f"{self.backend_url}/api/auth/login"
        payload = {"username": sensor_id, "password": secret_key} # عدلها حسب الـ Backend بتاعكم
        
        try:
            print(f"[API] Authenticating with {url}...")
            response = requests.post(url, json=payload, timeout=5)
            
            if response.status_code == 200:
                self.token = response.json().get("access_token")
                print("[API] Authentication Successful! Token received.")
                return self.token
            else:
                print(f"[API] Auth Failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"[API] Connection Error: {e}")
            return None

    def get_trusted_aps(self):
        """بنجيب بيها الشبكات الموثوقة من الداتا بيز"""
        if not self.token:
            return {}
            
        url = f"{self.backend_url}/api/sensors/trusted_aps"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[API] Failed to fetch Trusted APs: {e}")
        return {}
