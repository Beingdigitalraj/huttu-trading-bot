import os
import time
import requests
import MetaTrader5 as mt5

account = os.environ.get("MT5_ACCOUNT")
password = os.environ.get("MT5_PASSWORD")
server = os.environ.get("MT5_SERVER")

# Telegram Credentials (Apna Bot Token aur Chat ID yahan daal do ya Environment Variable se lo)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

def send_telegram_alert(message):
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Alert Failed: {e}")

print("Starting Huttu Autonomous Market Scanner & Trader...")
send_telegram_alert("🚀 *Huttu Autonomous Bot Started* and scanning market!")

# 1. Initialize MT5 Terminal properly
if not mt5.initialize():
    err_msg = f"❌ MT5 Initialize Failed, error code: {mt5.last_error()}"
    print(err_msg)
    send_telegram_alert(err_msg)
    exit()
else:
    print("MT5 Terminal initialized successfully.")
    
    if account and password and server:
        account_id = int(account)
        authorized = mt5.login(login=account_id, password=password, server=server)
        if not authorized:
            err_msg = f"❌ Failed to connect to MT5 account, error code: {mt5.last_error()}"
            print(err_msg)
            send_telegram_alert(err_msg)
        else:
            success_msg = f"✅ Successfully logged into MT5 Account: {account_id}"
            print(success_msg)
            send_telegram_alert(success_msg)
    else:
        print("Running in simulation mode (Secrets missing)")

# 2. Automatically detect correct Gold symbol for XM/IC Markets
POSSIBLE_SYMBOLS = ["XAUUSD", "XAUUSDm", "XAUUSD.a", "GOLD"]
SYMBOL = None

for s in POSSIBLE_SYMBOLS:
    symbol_info = mt5.symbol_info(s)
    if symbol_info is not None:
        SYMBOL = s
        break

if SYMBOL is None:
    err_msg = "❌ Error: Gold symbol (XAUUSD/XAUUSDm/GOLD) not found on this broker server."
    print(err_msg)
    send_telegram_alert(err_msg)
    mt5.shutdown()
    exit()

LOT = 0.01
SL_PIPS = 20
TP_PIPS = 40

def check_market_and_trade():
    symbol_info = mt5.symbol_info(SYMBOL)
    if not symbol_info.visible:
        if not mt5.symbol_select(SYMBOL, True):
            print(f"Failed to select symbol {SYMBOL}")
            return

    # 5 Minute timeframe par last candles fetch karo
    rates = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_M5, 0, 3)
    if rates is None or len(rates) < 3:
        print("Failed to fetch market rates data.")
        return

    # Simple Strategy Condition (Jaise: Agar last candle bullish hai)
    last_candle = rates[-1]
    is_bullish = last_candle['close'] > last_candle['open']

    log_msg = f"[{time.strftime('%Y-%m-%d %H:%M:%S' )}] Scanning {SYMBOL} on M5... Bullish Signal: {is_bullish}"
    print(log_msg)

    if is_bullish:
        point = mt5.symbol_info(SYMBOL).point
        price = mt5.symbol_info_tick(SYMBOL).ask
        sl = price - (SL_PIPS * 10 * point)
        tp = price + (TP_PIPS * 10 * point)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": SYMBOL,
            "volume": LOT,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 100200,
            "comment": "Huttu Autonomous Scanner",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)
        if result is None:
            msg = "⚠️ Order send failed, returned None"
            print(msg)
            send_telegram_alert(msg)
        elif result.retcode != mt5.TRADE_RETCODE_DONE:
            msg = f"⚠️ Order failed with retcode: {result.retcode}"
            print(msg)
            send_telegram_alert(msg)
        else:
            success_trade = f"🎯 *LIVE TRADE SUCCESS!*\nTicket ID: `{result.order}`\nSymbol: `{SYMBOL}`\nEntry Price: `{price}`"
            print(f"LIVE TRADE SUCCESS! Ticket ID: {result.order} | Entry: {price} | Symbol: {SYMBOL}")
            send_telegram_alert(success_trade)
    else:
        print("No trade condition met in this candle. Waiting...")

if __name__ == "__main__":
    try:
        while True:
            check_market_and_trade()
            print("Waiting 5 minutes for the next market check...\n")
            time.sleep(300)
    except KeyboardInterrupt:
        mt5.shutdown()
        print("Autonomous bot stopped safely.")
