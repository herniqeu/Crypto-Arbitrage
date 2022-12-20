from json import loads
from requests import post
from datetime import datetime
from env import api_key
import websocket
import threading

class Order(threading.Thread):
    def __init__(self, url, exchange, orderbook,last, lock):
        super().__init__()
        # create websocket connection
        # self.ws = websocket.WebSocketApp(
        #     url=spot_connection_url,
        #     on_message=on_message,
        #     on_error=on_error,
        #     on_close=on_close,
        #     on_open=on_open
        # )
        # convert message to dict, process update
        self.orderbook = orderbook
         # self.update = orderbook
        self.lock = lock
        self.last_update = last
        
        def on_message(sefl, message): 
            data = loads(message)
            process_updates(data)
            
        # catch errors
        def process_updates(data):
            if data["e"] == "executionReport":  # event type
                with self.lock:
                    self.orderbook[data['c']] = {#"id" : data["i"], 
                                            "symbol": data["s"], "side": data["S"], "price": data["p"],
                                            "quantity": data["q"], "quote ": data["Z"], "fee": data["n"],
                                            "execution": data["x"], "status": data["X"], "reject": data["r"],
                                            "event": data["E"], "transaction": data["T"], "creation": data["O"],
                                            }
                    # print(self.orderbook)
                    # self.last_update['last_update'] = datetime.now()

        def on_error(self, error):
            print(error)
    
        # run when websocket is closed
        def on_close(sefl, close_status_code, close_msg):
            print(f"Close: {close_status_code} {close_msg}")

        # exchange name
        def on_open(self):
            print(f'Connected to {exchange}\n')

        def on_ping(self, message):
            # logging.DEBUG("Responded Pong to server")
            # print(f"{str(datetime.datetime.now())} Received Ping from server")
            print(f"{exchange}: Received Ping from server")
            # print(f"{str(datetime.datetime.now())} Responded Pong to server")
            print(f"{exchange}: Responded Pong to server")

        def on_pong(self, message):
            # logging.DEBUG("Responded Pong to server")
            # print(f"{str(datetime.datetime.now())} Received Pong from server")
            print(f"{exchange}: Received Pong from server")

        def create_spot_listen_key(api_key):
            response = post(url='https://api.binance.com/api/v3/userDataStream', headers={'X-MBX-APIKEY': api_key})
            return response.json()['listenKey']

        listen_key = create_spot_listen_key(api_key)
        # print(listen_key)
        spot_connection_url = f"{url}/ws/{listen_key}"

        self.ws = websocket.WebSocketApp(
            url=spot_connection_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open,
            on_ping=on_ping,
            on_pong=on_pong
        )

        # keep connection alive
        # self.ws.run_forever(ping_interval=300)

    def run(self):
        # while True:
            self.ws.run_forever()



    

        

    
   


