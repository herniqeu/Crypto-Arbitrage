
import websocket
import threading
from datetime import datetime
from json import loads


class Chain(threading.Thread):
    def __init__(self, url, exchange, orderbook, lock, last):
        super().__init__()
        # create websocket connection
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
            with self.lock: 
                self.orderbook[data["s"]] = {"bid": float(
                    data["b"]), "ask": float(data["a"])}
                # print(self.orderbook)
                self.last_update['last_update'] = datetime.now()

        # catch errors

        def on_error(self, error):
            print(f"Error: {error}")

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
        self.ws = websocket.WebSocketApp(
            url=url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close,
            on_open=on_open,
            on_ping=on_ping,
            on_pong=on_pong
        )

        # keep connection alive
        # self.ws.run_forever()
    def run(self):
        while True:
            self.ws.run_forever()
