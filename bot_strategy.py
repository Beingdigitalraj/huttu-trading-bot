import os
import time
import MetaTrader5 as mt5

account = os.environ.get("MT5_ACCOUNT")
password = os.environ.get("MT5_PASSWORD")
server = os.environ.get("MT5_SERVER")

print("Starting Huttu Autonomous Market Scanner & Trader...")

# 1. Initialize MT5 Terminal properly
if not mt5.initialize():
    print(f"MT5 Initialize Failed, error code: {mt5.last_error()}")
    exit()
else:
    print("MT5 Terminal initialized successfully.")
    
    if account and password and server:
        account_id = int(account)
        authorized = mt5.login(login=account_id, password=password, server=server)
        if not authorized:
            print(f"Failed to connect to account, error code: {mt5.last_error()}")
        else:
            print(f"Successfully logged into MT5 Account: {account_id}")
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
    print("Error: Gold symbol (XAUUSD/XAUUSDm/GOLD) not found on this broker server.")
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

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scanning {SYMBOL} on M5... Bullish Signal: {is_bullish}")

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
            print("Order send failed, returned None")
        elif result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"Order failed with retcode: {result.retcode}")
        else:
            print(f"LIVE TRADE SUCCESS! Ticket ID: {result.order} | Entry: {price} | Symbol: {SYMBOL}")
    else:
        print("No trade condition met in this candle. Waiting...")

if __name__ == "__main__":
    try:
        while True:
            check_market_and_trade()
            # 5 minute (300 seconds) ka wait karega agle scan ke liye
            print("Waiting 5 minutes for the next market check...\n")
            time.sleep(300)
    except KeyboardInterrupt:
        mt5.shutdown()
        print("Autonomous bot stopped safely.")
