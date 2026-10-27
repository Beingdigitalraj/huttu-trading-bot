import urllib.request
import json

url = "http://localhost:5000/api/execute-trade"
payload = {"symbol": "XAUUSD", "action": "BUY", "volume": 0.1}

req = urllib.request.Request(
    url, 
    data=json.dumps(payload).encode('utf-8'), 
    headers={'Content-Type': 'application/json'}
)

try:
    print("🧪 [TESTING]: Sending trade request to server...")
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        print("✅ [TEST SUCCESS]: Server responded perfectly!")
        print(json.dumps(res, indent=2))
except Exception as e:
    print(f"❌ [TEST FAILED]: {e}")
