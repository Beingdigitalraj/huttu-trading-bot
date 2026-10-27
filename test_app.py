import urllib.request
import json

url = "http://localhost:5000/api/execute-trade"
payload = {
    "symbol": "XAUUSD",
    "action": "BUY",
    "volume": 0.1
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    url, 
    data=data, 
    headers={'Content-Type': 'application/json'}
)

try:
    print("🧪 [TESTING]: Sending test trade request to Huttu Pro Server...")
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode())
        print("✅ [TEST SUCCESS]: Server Response Received!")
        print(json.dumps(res_data, indent=2))
except Exception as e:
    print(f"❌ [TEST FAILED]: {e}")
