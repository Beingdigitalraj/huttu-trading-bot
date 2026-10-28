import os
import MetaTrader5 as mt5

account = os.environ.get("MT5_ACCOUNT")
password = os.environ.get("MT5_PASSWORD")
server = os.environ.get("MT5_SERVER")

print("Starting Huttu Windows Auto-Trader Engine...")

# 1. Initialize MT5 Terminal properly
if not mt5.initialize():
    print(f"MT5 Initialize Failed, error code: {mt5.last_error()}")
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

LOT = 0.01
SL_PIPS = 20
TP_PIPS = 40

def send_live_order():
    if SYMBOL is None:
        print("Error: Gold symbol (XAUUSD/XAUUSDm/GOLD) not found on this broker server.")
        return

    symbol_info = mt5.symbol_info(SYMBOL)
    if not symbol_info.visible:
        if not mt5.symbol_select(SYMBOL, True):
            print(f"Failed to select symbol {SYMBOL}")
            return

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
        "comment": "Huttu GitHub AutoTrade",
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

if __name__ == "__main__":
    send_live_order()
    mt5.shutdown()
