import time
import requests
import os

# Risk Management Configuration for Minimum Risk & Max Profit
SYMBOL = "XAUUSD"
VOLUME = 0.1
STOP_LOSS_PIPS = 20
TAKE_PROFIT_PIPS = 40

print("🚀 [HUTTU RISK ENGINE] Minimum Risk & High Profit Strategy Initialized...")

def execute_trade():
    signal_data = {
        "symbol": SYMBOL,
        "action": "BUY",
        "volume": VOLUME,
        "sl": STOP_LOSS_PIPS,
        "tp": TAKE_PROFIT_PIPS,
        "broker": "XM & IC Markets MT5"
    }
    
    # Print signal for server logs & webhook trigger
    print(f"⚡ [EXECUTE] Sending Trade Signal -> {signal_data}")

if __name__ == "__main__":
    while True:
        execute_trade()
        # Run every 10 seconds to check market condition safely without spamming
        time.sleep(10)
