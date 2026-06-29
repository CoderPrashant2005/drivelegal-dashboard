# simulate.py
import requests
import time
import random

API_URL = "http://127.0.0.1:8000/api/v1/violations/trigger"

# Updated to send your new custom project password
HEADERS = {
    "X-API-KEY": "DriveLegal_Project",
    "Content-Type": "application/json"
}

OFFENSES = [
    {"type": "Overspeeding", "sec": "Sec 112", "amt": 2000.0, "loc": "Connaught Place Bypass"},
    {"type": "Red Light Jump", "sec": "Sec 119", "amt": 3000.0, "loc": "Karol Bagh Intersection"},
    {"type": "Seat Belt Violation", "sec": "Sec 194B", "amt": 1000.0, "loc": "AIIMS Flyover Metro Zone"}
]

print("📡 Connecting to DriveLegal IoT Telematics Core (Authenticated)...")
while True:
    print(" waiting for new events...")
    time.sleep(5) # Wait a few seconds before triggering a new event
    offense = random.choice(OFFENSES)
    print(f"🚨 Simulating offense: {offense['type']} at {offense['loc']}")
    
    payload = {
        "vehicle_id": "DL01AB1234",
        "type": offense["type"],
        "sec": offense["sec"],
        "loc": offense["loc"],
        "lat": 28.61 + random.uniform(-0.05, 0.05),
        "lon": 77.20 + random.uniform(-0.05, 0.05),
        "amt": offense["amt"]
    }
    
    try:
        # Fires request cleanly with the updated passkey
        res = requests.post(API_URL, json=payload, headers=HEADERS, timeout=5)
    
        print("Status:", res.status_code)
        print("Response:", res.json())
    except Exception as e:
        import traceback
        traceback.print_exc()