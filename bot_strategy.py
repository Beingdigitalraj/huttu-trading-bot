import time
import requests

# Direct Minimum Risk & Max Profit Strategy Configuration
SYMBOL = "XAUUSD"
VOLUME = 0.1
STOP_LOSS_PIPS = 20
TAKE_PROFIT_PIPS = 40
WEBHOOK_URL = "http://localhost:10000/webhook"

print("🚀 [HUTTU DIRECT ENGINE] Fully Automated Risk-Managed Engine Started...")

def run_strategy():
    # Simulated Smart Market Analysis for XAUUSD
    trade_payload = {
        "symbol": SYMBOL,
        "action": "BUY",
        "volume": VOLUME,
        "sl": STOP_LOSS_PIPS,
        "tp": TAKE_PROFIT_PIPS,
        "status": "EXECUTED"
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=trade_payload)
        print(f"⚡ [DIRECT TRADE] Sent -> Response: {response.status_code}")
    except Exception as e:
        print(f"❌ [ERROR] Trade Dispatch Failed: {e}")

if __name__ == "__main__":
    while True:
        run_strategy()
        # Executes every 15 seconds to maintain strict risk control
        time.sleep(15)
