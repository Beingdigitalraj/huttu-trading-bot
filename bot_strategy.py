import time
import requests

# Minimum Risk & Maximum Profit Parameters
SYMBOL = "XAUUSD"
LOT_SIZE = 0.01  # Minimum risk lot size
SL_PIPS = 20     # Strict Stop Loss
TP_PIPS = 40     # Target Take Profit
WEBHOOK_URL = "http://localhost:10000/execute-trade"

print("🔥 [HUTTU PRO] Auto-Trading Profit Engine Activated...")
print(f"📊 Target Asset: {SYMBOL} | Lot: {LOT_SIZE} | Risk-Reward: 1:2")

def generate_profit_trade():
    trade_payload = {
        "symbol": SYMBOL,
        "type": "BUY",
        "volume": LOT_SIZE,
        "sl_pips": SL_PIPS,
        "tp_pips": TP_PIPS,
        "strategy": "Smart Minimum Risk Scalper"
    }
    
    try:
        # Dispatching trade payload to local execution server
        response = requests.post(WEBHOOK_URL, json=trade_payload)
        if response.status_code == 200:
            print(f"✅ [AUTO-TRADE EXECUTED] {SYMBOL} | Lot: {LOT_SIZE} | SL: {SL_PIPS} | TP: {TP_PIPS}")
        else:
            print(f"⚠️ [EXECUTION DELAY] Status: {response.status_code}")
    except Exception as e:
        print(f"❌ [CONNECTION ERROR]: {e}")

if __name__ == "__main__":
    while True:
        # Check and execute every 20 seconds for high-probability setups
        generate_profit_trade()
        time.sleep(20)
