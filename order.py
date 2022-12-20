
# import logging
import threading
from env import api_key, api_key_testnet, api_secret, api_secret_testnet
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError

# config_logging(logging, logging.DEBUG)


class Place(threading.Thread):
    def __init__(self, url, orderbook, symbol, type, limit, qty, price):
        super().__init__()
        
        try:
            
            # with lock:
                key = api_key

                secret = api_secret

                params = {
                    "symbol": symbol,
                    "side": type,
                    "type": limit,
                    # "timeInForce": "GTC",
                    "quantity": qty,
                    # "price": price,
                }

                # url = f"https://{url}"

                # client = Client(key, secret, base_url=url)
                client = Client(key, secret)

                response = client.new_order(**params)

                orderbook[response['clientOrderId']] = {
                    "status": response['status']
                }
                # logging.info(response)
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