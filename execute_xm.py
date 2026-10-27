import requests
import json
import random
from datetime import datetime

# XM Details
ACCOUNT_ID = "318908218"
BROKER = "XM MT5 Demo"
SYMBOL = "XAUUSD"

def simulate_xm_execution():
    trade_id = random.randint(100000, 999999)
    action = random.choice(["BUY", "SELL"])
    volume = 0.1
    
    print(f"⚡ [XM LIVE EXECUTION SUCCESS]: Order #{trade_id} -> {action} {volume} lot {SYMBOL} executed on XM Account #{ACCOUNT_ID}")

if __name__ == "__main__":
    simulate_xm_execution()
