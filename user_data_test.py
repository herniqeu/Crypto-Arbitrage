#!/usr/bin/env python3

import time
import json
# import logging
import threading
# from binance.lib.utils import config_logging
from binance.spot import Spot as Client
from env import api_key_testnet
from binance.websocket.spot.websocket_client import SpotWebsocketClient
from binance.error import ClientError
import os, certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# config_logging(logging, logging.DEBUG)

class Order(threading.Thread):
    def __init__(self, url, orderbook, lock):
        super().__init__()

        def process_updates(message):
            # with lock: 
                aux = len(list(message.keys()))
                if aux > 2:
                    if message["e"] == "executionReport":  # event type
                        # with lock: 
                        orderbook[message['c']] = {#"id" : message["c"], 
                                                        "symbol": message["s"], "side": message["S"], "status": message["X"],
                                                        "price": message["p"],"quantity": message["q"], "quote ": message["Z"], 
                                                        # "fee": message["n"],"execution": message["x"], "reject": message["r"],
                                                        # "event": message["E"], "transaction": message["T"], "creation": message["O"],
                                                        }
                        
                        # with open("websocket/project2/get_order.json", 'w', encoding='utf-8') as f:
                        #     json.dump(orderbook, f, ensure_ascii=False, indent=2)

        
        client = Client(api_key_testnet, base_url="https://testnet.binance.vision")

        response = client.new_listen_key()

        # logging.info(f"Receving listen key : {response['listenKey']} ")
        # print()

        # ws_client = SpotWebsocketClient(stream_url=url)
        # ws_client.start()

        # ws_client.user_data(
        #     listen_key=response["listenKey"],
        #     id=1,
        #     callback=process_updates,)
        try:
            with lock: 
                ws_client = SpotWebsocketClient(stream_url=url)
                ws_client.start()
                print(f'Connected to User Stream')
                ws_client.user_data(listen_key=response["listenKey"],id=1,callback=process_updates)
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
            # ws_client.stop()
            # print(f'Close to User Stream\n')