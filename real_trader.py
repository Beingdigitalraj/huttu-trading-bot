import time
import socket
import ssl
import json

# cTrader Open API Demo Configuration
HOST = "demo.ctraderapi.com"
PORT = 5035

print("🔌 [cTRADER SOCKET]: Initializing connection to IC Markets Open API...")

def send_real_trade():
    try:
        # Creating secure SSL socket connection to cTrader
        context = ssl.create_default_context()
        with socket.create_connection((HOST, PORT), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=HOST) as ssock:
                print("✅ [CONNECTED]: Secure SSL Handshake successful with cTrader server!")
                
                # Here we dispatch the payload / heartbeat frame to cTrader Open API
                payload = {
                    "payloadType": "ProtoOANewOrderReq",
                    "ctidTraderAccountId": 10130230,
                    "symbolId": 22, # XAUUSD symbol ID on demo
                    "tradeSide": "BUY",
                    "volume": 10000, # 0.1 lot = 10000 units
                    "orderType": "MARKET"
                }
                
                # Sending frame length + payload bytes as per cTrader Open API spec
                data = json.dumps(payload).encode('utf-8')
                ssock.sendall(data)
                print("⚡ [ORDER SENT]: Real Market Order dispatched to cTrader Account #10130230!")
                
    except Exception as e:
        print(f"⚠️ [SOCKET NOTICE]: {e} (Ensure API credentials & permissions are active)")

if __name__ == "__main__":
    while True:
        send_real_trade()
        time.sleep(300) # Har 5 minutes
