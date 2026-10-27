import time
import requests
import json

SERVER_URL = "http://localhost:5000/api/execute-trade"

print("🤖 [24/7 HUTTU PRO DUAL-BROKER BOT]: Automated Engine Started...")

while True:
    try:
        # Simulate market signal generation
        signal_data = {
            "symbol": "XAUUSD",
            "action": "BUY",
            "volume": 0.1,
            "broker": "XM MT5 (#318908218) & IC Markets"
        }

        print(f"📊 [SIGNAL GENERATED]: Sending {signal_data['action']} order for {signal_data['symbol']}...")
        
        response = requests.post(SERVER_URL, json=signal_data)
        if response.status_code == 200:
            print(f"⚡ [DUAL TRADE EXECUTED]: Successfully dispatched to brokers & Telegram!")
        else:
            print(f"❌ [EXECUTION FAILED]: Status {response.status_code}")

    except Exception as e:
        print(f"❌ [BOT ERROR]: {e}")

    # Har 30 seconds mein automatic trade trigger karega (Testing ke liye)
    time.sleep(30)
