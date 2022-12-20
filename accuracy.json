#!/usr/bin/env python3

import threading
import logging
from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client
from binance.error import ClientError

# config_logging(logging, logging.DEBUG)


class Chain(threading.Thread):
    def __init__(self, url, orderbook, lock):
        super().__init__()

        def process_updates(message):
            with lock: 
                data = message.copy()
                data = len(list(data.keys()))
                if data >= 5:
                    orderbook[message["s"]] = {"bid": float(
                    message["b"]), "ask": float(message["a"])}


        # my_client = Client(stream_url=url)
            # my_client = Client()
        # my_client.start()
        # my_client.book_ticker(
        #         id=1,
        #         callback=process_updates,
        #         symbol="BTCUSDT")
                # logging.info(response)


        try:
            my_client = Client(stream_url=url)
            my_client.start()
            print(f'Connected to Binance')
            my_client.book_ticker(id=1,callback=process_updates)
        except ClientError as error:
            # logging.error(
            #     "Found error. status: {}, error code: {}, error message: {}".format(
            #         error.status_code, error.error_code, error.error_message
            #     )
            # )
            print(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )
            my_client.stop()
            print(f'Close to Binance\n')

