
# import logging
import threading
import json
from env import api_key, api_key_testnet, api_secret, api_secret_testnet
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError

# config_logging(logging, logging.DEBUG)


class Cancel(threading.Thread):
    def __init__(self, url, orderbook, symbol, clientOrderId):
        super().__init__()

        try:

            # with lock:
            key = api_key_testnet

            secret = api_secret_testnet

            url = f"https://{url}"

            client = Client(key, secret, base_url=url)

            response = client.cancel_order(
                symbol, origClientOrderId=clientOrderId)

            # orderbook[response['origClientOrderId']] = {
            #     "symbol": response["symbol"], "status": response['status'],
            # }
            orderbook[response['origClientOrderId']] = {"symbol": response["symbol"], "side": response["side"], "price": response["price"],
                                                        "quantity": response["origQty"], "orderId": response["orderId"], "type": response["type"],
                                                        "timeInForce": response["timeInForce"], "status": response['status']
                                                        }
            with open("websocket/project2/cancel_order.json", 'w', encoding='utf-8') as f:
                json.dump(orderbook, f, ensure_ascii=False, indent=2)
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
# {'symbol': 'BTCUSDT', 'origClientOrderId': 'trxXLSFk3ZCyv11RlrxgkV', 'orderId': 4359831, 'orderListId': -1, 'clientOrderId': '7TKHWRUCfuGck0BvqGXkut', 'price': '20450.12000000', 'origQty': '0.00212000', 'executedQty': '0.00000000', 'cummulativeQuoteQty': '0.00000000', 'status': 'CANCELED', 'timeInForce': 'GTC', 'type': 'LIMIT', 'side': 'SELL'}
