import os
import MetaTrader5 as mt5

# Retrieve credentials securely from GitHub Secrets
account = os.environ.get("MT5_ACCOUNT")
password = os.environ.get("MT5_PASSWORD")
server = os.environ.get("MT5_SERVER")

print("🚀 Starting Huttu Windows Auto-Trader Engine...")

if account and password and server:
    account = int(account)
    initialized = mt5.initialize(login=account, password=password, server=server)
    if not initialized:
        print(f"❌ MT5 Initialize Failed, error code: {mt5.last_error()}")
    else:
        print(f"✅ Successfully logged into MT5 Account: {account}")
else:
    print("ℹ️ Running in simulation mode (Set MT5 Secrets in GitHub for Live Orders).")

# Strategy Parameters
SYMBOL = "XAUUSD"
LOT = 0.01
SL_PIPS = 20
TP_PIPS = 40

def send_live_order():
    if not mt5.terminal_info():
        print("⚠️ MT5 Terminal not active/connected.")
        return

    symbol_info = mt5.symbol_info(SYMBOL)
    if symbol_info is None:
        print(f"❌ Symbol {SYMBOL} not found.")
        return

    if not symbol_info.visible:
        mt5.symbol_select(SYMBOL, True)

    point = mt5.symbol_info(SYMBOL).point
    price = mt5.symbol_info_out(SYMBOL).ask
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
        print("❌ Order send failed, returned None")
    elif result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Order failed with retcode: {result.retcode}")
    else:
        print(f"🎉 LIVE TRADE SUCCESS! Ticket ID: {result.order} | Entry: {price}")

if __name__ == "__main__":
    send_live_order()
    mt5.shutdown()
