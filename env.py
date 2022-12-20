import ccxt
import math
from env import api_key_testnet, api_secret_testnet, api_key, api_secret
from datetime import datetime
from filter import Filter
from chain import Chain
from order import Order
import threading
from binance.client import Client
from binance import Client
import requests
import math
from binance.enums import *
from json import load
from all_book_ticker import Chain
from user_data_test import Order
from cancel_orders import Cancel
import time



client = Client(api_key, api_secret)

test = {
    "apiKey": api_key_testnet,
    "secret": api_secret_testnet,
    'enableRateLimit': True,
    # "verbose": True,
}
main = {
    "apiKey": api_key,
    "secret": api_secret,
    'enableRateLimit': True,
    # "verbose": True,
}

#transactions = [{'s1': 'a', 's2': 'a', 's3': 'a','types': 'a', 'scrip1': 'a', 'scrip2': 'a', 'scrip3': 'a', 'profit_loss': 0.0000001}]
transactions = []
transactions2 = []


def sortcrypto(list):
    for i in range(0, len(list)-1):
        for j in range(0, len(list)-1):
            if list[j]["profit_loss"] > list[j+1]["profit_loss"]:
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp
    return list

def sortcrypto2(list1):
    for i in range(0,len(list1)-1):
        for i in range(0,len(list1)-1):
            if list1[i][0] < list1[i+1][0]:
                temp = list1[i]
                list1[i] = list1[i+1]
                list1[i+1] = temp
    return list1

def sortcrypto3(list1):
    for i in range(0,len(list1)-1):
        for i in range(0,len(list1)-1):
            if list1[i][1] > list1[i+1][1]:
                temp = list1[i]
                list1[i] = list1[i+1]
                list1[i+1] = temp
    return list1

# executar só as melhores transações mandar 3 para fazer depois só depois de 1s para fazer de volta, de 1 em 1 segundo transações viram [] e voltam 'usar time.sleep()'

# metodo para que possamos depois de já estar funcionando, implementarmos o algoritimo
# r = requests.get("https://api.binance.com/api/v3/depth",params=dict(symbol="ETHBUSD"))
# results = r.json()


exchange = ccxt.binance(main)

exchange.set_sandbox_mode(enabled=False)

params = {
    'test': True,  # test if it's valid, but don't actually place it
}

INVESTMENT_AMOUNT_DOLLARS = 100  # value
MIN_PROFIT_DOLLARS = 0.01
BROKERAGE_PER_TRANSACTION_PERCENT = 0.01  # 0.1 == 0.01% poncentagem


def getBOOK(symbol):
    return orderbooks[symbol]

def getBOOKask(symbol):
    if getBOOK(symbol) != None:
        ask = orderbooks[symbol]
        return ask['ask']
    else:
        None

def getBOOKbid(symbol):
   if getBOOK(symbol) != None:
       bid = orderbooks[symbol]
       return bid['bid']
   else:
       None

def process_updates(message):
    data = loads(message)
    print(1)
    print(data)
    # last = data["info"]
    # print(last)
    orderlast = {"clientOrderId": data["clientOrderId"]}
    Book[data["clientOrderId"]] = {"info": data["info"],
                                   "last": datetime.now()}
    print(orderlast)

def accuracy_buy(symbol):
    n = Book[symbol]['stepSize'].find('1')
    if n == 0:
        return 0
    elif n > 1:
        return (n - 1)


def accuracy_sell(symbol):
    n = Book[symbol]['tickSize'].find('1')
    if n == 0:
        return 0
    elif n > 1:
        return n - 1

def place_buy_order(scrip, quantity, price):
    Place("testnet.binance.vision", orderlast,scrip, "BUY", "MARKET", quantity, price)

def place_sell_order(scrip, quantity, price):
    Place("testnet.binance.vision", orderlast,scrip, "SELL", "MARKET", quantity, price)

def cancel_order(scrip, clientOrderId):
    Cancel("testnet.binance.vision", ordercancel,scrip, clientOrderId)
    

def saberask1(simbolo):
    ok = client.get_orderbook_ticker(symbol=simbolo)
    return ok['askPrice']

def saberbid1(simbolo):
    ok = client.get_orderbook_ticker(symbol=simbolo)
    return ok['bidPrice']

def check_if_float_zero(value):
    return math.isclose(value, 0.0, abs_tol=1e-3)

def place_trade_orders(s1, s2, s3, types, initial_amount):
    final_amount = 0.0

    if types == 'BUY_BUY_SELL':

        current_price1 = getBOOKbid(s1)

        s1_quantity = round((initial_amount / current_price1), accuracy_buy(s1))

        # print(current_price1, s1)
        place_buy_order(s1, s1_quantity, current_price1)

        # sleep(0.01)
        # print(current_price1)
        # print(s1_quantity)
        # print(orderlast)
        # # last = list(orderlast.keys())
        # # print(last)
        # # sleep(10)
        # print(orderlast[list(orderlast.keys())[0]])
        # print(orderlast[list(orderlast.keys())[0]]['status'])

        # if orderlast:
        # 0 // 1 ordem FILLED
        if orderlast[list(orderlast.keys())[0]]['status'] == 'FILLED':
            print(f"{s1}: Ordem ok 0")
            current_price2 = getBOOKbid(s2)

            s2_quantity = round(
                ((s1_quantity * 0.9989)/current_price2), accuracy_buy(s2))

            place_buy_order(s2, s2_quantity, current_price2)

            # sleep(0.01)
            # 00 // 2 ordem FILLED
            print(orderlast)
            print(orderlast[list(orderlast.keys())[1]])
            print(orderlast[list(orderlast.keys())[1]]['status'])
            if orderlast[list(orderlast.keys())[1]]['status'] == 'FILLED':
                print(f"{s2}: Ordem ok 00")
                current_price3 = getBOOKask(s3)

                s3_quantity = round(
                    (s2_quantity * 0.9989), accuracy_buy(s2))

                place_sell_order(s3, s3_quantity, current_price3)

                # sleep(0.01)
                print(orderlast)
                print(orderlast[list(orderlast.keys())[2]])
                print(orderlast[list(orderlast.keys())[2]]['status'])
                # 000 // 3 ordem FILLED
                if orderlast[list(orderlast.keys())[2]]['status'] == 'FILLED':
                    print(f"{s3}: Ordem ok 000")
                    final_amount = s3_quantity * current_price3

                    print(f'BUY_BUY_SELL => {s1}: {initial_amount} / {current_price1} = {s1_quantity} => '
                          f'{s2}: {s2_quantity} / {current_price2} => '
                          f'{s3}: {s3_quantity} * {current_price3} = {round(final_amount / 1, 8)}')

                    orderlast.clear()
                    # last.clear()
                    print("Lista limpa")

                    # return final_amount
                # 001 // 3 ordem NEW
                else:
                    for i in range(100000):
                        # 000 // 3 ordem FILLED
                        # print(orderexec)
                        orderexec[list(orderlast.keys())[2]] = {
                            'status': orderlast[list(orderlast.keys())[2]]['status']}
                        # print(orderexec)
                        if orderexec[list(orderlast.keys())[2]]['status'] == 'FILLED':
                            print(f"{s3}: Ordem ok 001")
                            final_amount = s3_quantity * current_price3

                            print(f'BUY_BUY_SELL => {s1}: {initial_amount} / {current_price1} = {s1_quantity} => '
                                  f'{s2}: {s2_quantity} / {current_price2} => '
                                  f'{s3}: {s3_quantity} * {current_price3} = {round(final_amount / 1, 8)}')

                            orderlast.clear()
                            # last.clear() 
                            print("Lista limpa")

                            break
                            # return final_amount
                        # 001 // 3 ordem NEW
                        else:
                            if i % 100 == 0:
                                print(orderexec[list(orderlast.keys())[2]])
                            if i > 10000:
                                
                                print(
                                    f"deu ruim na {s3}: 3° Ordem 001, Nâo executou, Cancelando ordem")
                                orderlast.clear()
                                # cancel_order(s3,list(orderlast.keys())[2])
                                # print(ordercancel[list(orderlast.keys())[2]])
                                break
                            time.sleep(0.001)

            # 01 // 2 ordem NEW
            else:
                orderexec[list(orderlast.keys())[1]] = {
                    'status': orderlast[list(orderlast.keys())[1]]['status']}
                for j in range(100000):
                    # 01 // 2 ordem FILLED
                    # print(orderexec)
                    # print(orderexec)
                    if orderexec[list(orderlast.keys())[1]]['status'] == 'FILLED':
                        print(f"{s2}: Ordem ok 01")
                        current_price3 = getBOOKask(s3)

                        s3_quantity = round(
                            (s2_quantity * 0.9989), accuracy_buy(s2))

                        place_sell_order(s3, s3_quantity, current_price3)

                        # sleep(0.01)
                        # 010 // 3 ordem FILLED
                        if orderlast[list(orderlast.keys())[2]]['status'] == 'FILLED':
                            print(f"{s3}: Ordem ok 010")
                            final_amount = s3_quantity * current_price3

                            print(f'BUY_BUY_SELL => {s1}: {initial_amount} / {current_price1} = {s1_quantity} => '
                                  f'{s2}: {s2_quantity} / {current_price2} => '
                                  f'{s3}: {s3_quantity} * {current_price3} = {round(final_amount / 1, 8)}')

                            orderlast.clear()
                            # last.clear()

                            print("Lista limpa")
                            break
                            # return final_amount
                        # 011 // 3 ordem NEW
                        else:
                            orderexec[list(orderlast.keys())[2]] = {
                                'status': orderlast[list(orderlast.keys())[2]]['status']}

                            for i in range(100000):
                                # 010 // 3 ordem FILLED
                                # print(orderexec)
                                # orderexec[list(orderlast.keys())[2]] = {'status' : orderlast[list(orderlast.keys())[2]]['status']}
                                # print(orderexec)
                                if orderexec[list(orderlast.keys())[2]]['status'] == 'FILLED':
                                    print(f"{s3}: Ordem ok 011")
                                    final_amount = s3_quantity * current_price3

                                    print(f'BUY_BUY_SELL => {s1}: {initial_amount} / {current_price1} = {s1_quantity} => '
                                          f'{s2}: {s2_quantity} / {current_price2} => '
                                          f'{s3}: {s3_quantity} * {current_price3} = {round(final_amount / 1, 8)}')

                                    orderlast.clear()
                                    # last.clear()

                                    print("Lista limpa")
                                    break
                                    # return final_amount
                                # 011 // 3 ordem NEW
                                else:
                                    if i % 100 == 0:
                                                print(orderexec[list(orderlast.keys())[2]])
                                    if i > 10000:
                                        print(
                                            f"deu ruim na {s3}: 3° Ordem 011, Nâo executou, Cancelando ordem")
                                        # cancel_order(s3,list(orderlast.keys())[2])
                                        # print(ordercancel[list(orderlast.keys())[2]])
                                        break
                                    sleep(0.001)
                            break

                    # 01 // 2 ordem NEW
                    else:
                        if j % 100 == 0:
                            print(orderexec[list(orderlast.keys())[1]])
                        if j > 10000:
                            print(
                                f"deu ruim na {s2}: 2° Ordem 01, Nâo executou, Cancelando ordem")
                            orderlast.clear()
                            # cancel_order(s2,list(orderlast.keys())[1])
                            # print(ordercancel[list(orderlast.keys())[1]])
                            break
                        time.sleep(0.001)
        # 1 // 1 ordem NEW
        else:
            # print("aqui")
            orderexec[list(orderlast.keys())[0]] = {
                'status': orderlast[list(orderlast.keys())[0]]['status']}

            for i in range(100000):
                # print(f"aqui + {i}")
                # 1 // 1 ordem FILLED
                # sleep(0.01)
                # print(orderexec)
                # print(orderexec)
                if orderexec[list(orderlast.keys())[0]]['status'] == 'FILLED':
                    print(f"{s1}: Ordem ok 1")
                    current_price2 = getBOOKbid(s2)

                    s2_quantity = round(
                        ((s1_quantity * 0.9989)/current_price2), accuracy_buy(s2))

                    place_buy_order(s2, s2_quantity, current_price2)

                    # sleep(0.01)
                    # 10 // 2 ordem FILLED
                    if orderlast[list(orderlast.keys())[1]]['status'] == 'FILLED':
                        print(f"{s2}: Ordem ok 10")
                        current_price3 = getBOOKask(s3)

                        s3_quantity = round(
                            (s2_quantity * 0.9989), accuracy_buy(s2))

                        place_sell_order(s3, s3_quantity, current_price3)

                        # sleep(0.01)
                        # 100 // 3 ordem FILLED
                        if orderlast[list(orderlast.keys())[2]]['status'] == 'FILLED':
                            print(f"{s3}: Ordem ok 100")
                            final_amount = s3_quantity * current_price3

                            print(f'BUY_BUY_SELL => {s1}: {initial_amount} / {current_price1} = {s1_quantity} => '
                                  f'{s2}: {s2_quantity} / {current_price2} => '
                                  f'{s3}: {s3_quantity} * {current_price3} = {round(final_amount / 1, 8)}')

                            orderlast.clear()
                            # last.clear()
                            print("Lista limpa")

                            break
                            # return final_amount

                        # 101 // 3 ordem NEW
                        else:
                            orderexec[list(orderlast.keys())[2]] = {
                                'status': orderlast[list(orderlast.keys())[2]]['status']}

                            for j in range(100000):
                                # 100 // 3 ordem FILLED
                                # print(orderexec)
                                # print(orderexec)
                                if orderexec[list(orderlast.keys())[2]]['status'] == 'FILLED':
                                    print(f"{s3}: Ordem ok 101")
                                    final_amount = s3_quantity * current_price3

                                    print(f'BUY_BUY_SELL => {s1}: {initial_amount} / {current_price1} = {s1_quantity} => '
                                          f'{s2}: {s2_quantity} / {current_price2} => '
                                          f'{s3}: {s3_quantity} * {current_price3} = {round(final_amount / 1, 8)}')

                                    orderlast.clear()
                                    # last.clear()
                                    print("Lista limpa")

                                    break
                                    # return final_amount

                                # 101 // 3 ordem NEW
                                else:
                                    if j % 100 == 0:
                                        print(orderexec[list(orderlast.keys())[2]])
                                    if j > 10000:
                                        print(
                                            f"deu ruim na {s3}: 3° Ordem 101, Nâo executou, Cancelando ordem")
                                        orderlast.clear()
                                        # cancel_order(s3,list(orderlast.keys())[2])
                                        # print(ordercancel[list(orderlast.keys())[2]])
                                        break
                                    time.sleep(0.001)
                            break

                    # 11 // 2 ordem NEW
                    else:
                        orderexec[list(orderlast.keys())[1]] = {
                            'status': orderlast[list(orderlast.keys())[1]]['status']}

                        for h in range(100000):
                            # 10 // 2 ordem FILLED
                            # print(orderexec)
                            # print(orderexec)
                            if orderexec[list(orderlast.keys())[1]]['status'] == 'FILLED':
                                print(f"{s2}: Ordem ok 11")
                                current_price3 = getBOOKask(s3)

                                s3_quantity = round(
                                    (s2_quantity * 0.9989), accuracy_buy(s2))

                                place_sell_order(
                                    s3, s3_quantity, current_price3)

                                # sleep(0.01)
                                # 110 // 3 ordem FILLED
                                if orderlast[list(orderlast.keys())[2]]['status'] == 'FILLED':
                                    print(f"{s3}: Ordem ok 110")
                                    final_amount = s3_quantity * current_price3

                                    print(f'BUY_BUY_SELL => {s1}: {initial_amount} / {current_price1} = {s1_quantity} => '
                                          f'{s2}: {s2_quantity} / {current_price2} => '
                                          f'{s3}: {s3_quantity} * {current_price3} = {round(final_amount / 1, 8)}')

                                    orderlast.clear()
                                    # last.clear()
                                    print("Lista limpa")

                                    break
                                    # return final_amount

                                # 111 // 3 ordem NEW
                                else:
                                    orderexec[list(orderlast.keys())[2]] = {
                                        'status': orderlast[list(orderlast.keys())[2]]['status']}

                                    for k in range(100000):
                                        # 110 // 3 ordem FILLED
                                        # print(orderexec)
                                        # print(orderexec)
                                        if orderexec[list(orderlast.keys())[2]]['status'] == 'FILLED':
                                            print(f"{s3}: Ordem ok 111")
                                            final_amount = s3_quantity * current_price3

                                            print(f'BUY_BUY_SELL => {s1}: {initial_amount} / {current_price1} = {s1_quantity} => '
                                                  f'{s2}: {s2_quantity} / {current_price2} => '
                                                  f'{s3}: {s3_quantity} * {current_price3} = {round(final_amount / 1, 8)}')

                                            orderlast.clear()
                                            print("Lista limpa")
                                            break
                                            # return final_amount

                                        # 111 // 3 ordem NEW
                                        else:
                                            if k % 100 == 0:
                                                print(orderexec[list(orderlast.keys())[2]])
                                            if k > 10000:
                                                
                                                print(
                                                    f"deu ruim na {s3}: 3° Ordem 111, Nâo executou, Cancelando ordem")
                                                orderlast.clear()
                                                # cancel_order(s3,list(orderlast.keys())[2])
                                                # print(ordercancel[list(orderlast.keys())[2]])
                                                break
                                            time.sleep(0.001)
                                    break
                            # 11 // 2 ordem NEW
                            else:
                                if h % 100 == 0:
                                    print(orderexec[list(orderlast.keys())[1]])
                                if h > 1000:
                                    print(
                                        f"deu ruim na {s2}: 2° Ordem 11, Nâo executou, Cancelando ordem")
                                    orderlast.clear()
                                    # cancel_order(s2,list(orderlast.keys())[1])
                                    # print(ordercancel[list(orderlast.keys())[1]])
                                    break
                                time.sleep(0.001)

                        break

                # 1 // 1 ordem NEW
                else:
                    # print(f"aqui + {i} {i}")
                    # print(orderexec)
                    if i % 100 == 0:
                        print(orderexec[list(orderlast.keys())[0]])
                    if i > 1000:
                        print(f"deu ruim na {s1}: 1° Ordem 1, Nâo executou, Cancelando ordem")
                        cancel_order(s1,list(orderlast.keys())[0])
                        print(ordercancel[list(orderlast.keys())[0]])
                        orderlast.clear()
                        break
                    time.sleep(0.001)
            # pass

    print("SAIU")

    sleep(4)
    return final_amount


#def place_buy_order(scrip, quantity, limit):
#    order = exchange.create_limit_buy_order(scrip, quantity, limit, params)
#    print(order)

#def place_sell_order(scrip, quantity, limit):
#    order = exchange.create_limit_sell_order(scrip, quantity, limit, params)
#    print(order)

#place_trade_orders(list1['s1'], list1['s2'], list1['s3'], list1['types'],list1['scrip1'], list1['scrip2'], list1['scrip3'], first_amount)

# ----------------------------------------------------------------------
# buy buy buy (CHECK)
# sell sell sell (CHECK)
# buy sell buy (CHECK)
# sell buy sell (CHECK)
# buy buy sell (CHECK)
# sell sell buy (CHECK)
# buy sell sell (CHECK)
# sell buy buy (CHECK)

# fazer transações funcionando
# melhorar o filtro das transações
# melhorar pegar transações
# implementar algoritimo de henrique
# optimizazr o codigo
# implementar algoritimo para outras corretoras


def check_buy_buy_buy(s1, s2, s3,initial_investment):
    final_price = 0
    current_price1 = getBOOKbid(s1)
    investment_amount1 = initial_investment
    if current_price1 is not None and not check_if_float_zero(current_price1):
        buy_quantity1 = round(investment_amount1 / current_price1, 8)
        investment_amount2 = buy_quantity1
        current_price2 = getBOOKbid(s2)
        if current_price2 is not None and not check_if_float_zero(current_price2):
            buy_quantity2 = round(investment_amount2 / current_price2, 8)
            investment_amount3 = buy_quantity2
            current_price3 = getBOOKbid(s3)
            if current_price3 is not None and not check_if_float_zero(current_price3):
                final_price = round(investment_amount3 / current_price3, 8)
    return final_price

def check_sell_sell_sell(s1, s2, s3, initial_investment):
    final_price = 0
    current_price1 = getBOOKask(s1)
    print(current_price1)
    investment_amount1 = initial_investment
    if current_price1 is not None and not check_if_float_zero(current_price1):
        sell_quantity1 = investment_amount1
        sell_price1 = round(sell_quantity1 * current_price1, 8)
        investment_amount2 = sell_price1
        current_price2 = getBOOKask(s2)
        if current_price2 is not None and not check_if_float_zero(current_price2):
            sell_quantity2 = investment_amount2
            sell_price2 = round(sell_quantity2 * current_price2)
            investment_amount3 = sell_price2
            current_price3 = getBOOKask(s3)
            if current_price3 is not None and not check_if_float_zero(current_price3):
                sell_quantity3 = investment_amount3
                final_price = round(sell_quantity3 * current_price3, 3)
    return final_price

def check_buy_sell_buy(s1, s2, s3, initial_investment):
    final_price = 0
    current_price1 = getBOOKbid(s1)
    investment_amount1 = initial_investment
    if current_price1 is not None and not check_if_float_zero(current_price1):
        buy_quantity1 = round(investment_amount1 / current_price1, 8)
        investment_amount2 = buy_quantity1
        current_price2 = getBOOKask(s2)
        if current_price2 is not None and not check_if_float_zero(current_price2):
            sell_quantity2 = buy_quantity1
            sell_price2 = round(sell_quantity2 * current_price2, 8)
            investment_amount3 = sell_quantity2
            current_price3 = getBOOKbid(s3)
            if current_price3 is not None and not check_if_float_zero(current_price3):
                buy_quantity3 = sell_quantity2
                final_price = round(buy_quantity3 / current_price3, 3)
    return final_price

def check_sell_buy_sell(s1, s2, s3,initial_investment):
    final_price = 0
    current_price1 = getBOOKask(s1)
    invesment_amount1 = initial_investment
    if current_price1 is not None:
        sell_quantity1 = round(invesment_amount1 * current_price1, 8)

        investment_amount2 = sell_quantity1
        current_price2 = getBOOKbid(s2)
        if current_price2 is not None:
            buy_quantity2 = round(investment_amount2 / current_price2, 8)

            investment_amount3 = buy_quantity2
            current_price3 = getBOOKask(s3)
            if current_price3 is not None and not check_if_float_zero(current_price3):
                final_price = round(investment_amount3 * current_price3, 3)
    return final_price

def check_buy_buy_sell(s1, s2, s3,initial_investment):
    final_price = 0
    current_price1 = getBOOKbid(s1)
    investment_amount1 = initial_investment
    if current_price1 is not None:
        buy_quantity1 = round(investment_amount1 / current_price1, 8)
        # SCRIP2
        investment_amount2 = buy_quantity1
        current_price2 = getBOOKbid(s2)
        if current_price2 is not None:
            buy_quantity2 = round(investment_amount2 / current_price2, 8)
            # SCRIP3
            current_price3 = getBOOKask(s3)
            if current_price3 is not None:
                sell_quantity3 = buy_quantity2
                final_price = round(sell_quantity3 * current_price3, 3)
    return final_price

def check_sell_sell_buy(s1, s2, s3,initial_investment):
    final_price = 0
    current_price1 = getBOOKask(s1)
    print(current_price1)
    investment_amount1 = initial_investment
    if current_price1 is not None:
        sell_quantity1 = round(investment_amount1 * current_price1, 8)

        investment_amount2 = sell_quantity1
        current_price2 = getBOOKask(s2)
        if current_price2 is not None:
            sell_quantity2 = round(investment_amount2 * current_price2)

            investment_amount3 = sell_quantity2
            current_price3 = getBOOKbid(s3)
            if current_price3 is not None:
                final_price = round(investment_amount3 / current_price3, 3)
    return final_price

def check_buy_sell_sell(s1, s2, s3,initial_investment):
    final_price = 0
    # SCRIP1
    print("Buy_sell_sell")
    print(s1)
    print(s2)
    print(s3)
    print(getBOOKask(s1))
    print(getBOOKbid(s2))
    print(getBOOKbid(s3))
    print("------")
    time.sleep(1.0)
    investment_amount1 = initial_investment
    current_price1 = getBOOKbid(s1)
    if current_price1 is not None:
        buy_quantity1 = round(investment_amount1 / current_price1, 8)
        # SCRIP2
        current_price2 = getBOOKask(s2)
        if current_price2 is not None:
            sell_quantity2 = buy_quantity1
            sell_price2 = round(sell_quantity2 * current_price2, 8)
            # SCRIP3
            current_price3 = getBOOKask(s3)
            if current_price3 is not None:
                sell_quantity3 = sell_price2
                final_price = round(sell_quantity3 * current_price3, 3)

                # print(f'BUY_SELL_SELL => {scrip1}: {round(investment_amount1 / 1, 6)} / {round(current_price1 / 1, 6)} = {round(buy_quantity1 / 1, 6)} => '
                #       f'{scrip2}: {round(sell_quantity2 / 1, 6)} / {round(current_price2 / 1, 6)} = {round(sell_price2 / 1, 6)} => '
                #       f'{scrip3}: {round(sell_quantity3 / 1, 6)} * {round(current_price3 / 1, 6)} = {round(final_price / 1, 3)} ')
    return final_price

def check_sell_buy_buy(s1, s2, s3,initial_investment):

    final_price = 0
    current_price1 = getBOOKask(s1)
    investment_amount1 = initial_investment
    if current_price1 is not None:
        sell_quantity1 = round(investment_amount1 * current_price1, 8)

        investment_amount2 = sell_quantity1
        current_price2 = getBOOKbid(s2)
        if current_price2 is not None:
            buy_quantity2 = round(investment_amount2 / current_price2, 8)

            investment_amount3 = buy_quantity2
            current_price3 = getBOOKbid(s3)
            if current_price3 is not None:
                final_price = round(investment_amount3 / current_price3, 3)
    return final_price

def check_buy_buy_sell2(s1, s2, s3, initial_investment):
    final_price2 = 0
    # SCRIP1
    current_price1 = float(saberask1(s1))
    investment_amount1 = initial_investment
    if current_price1 is not None and not check_if_float_zero(current_price1):
        buy_quantity1 = round(investment_amount1 / current_price1, 8)
        # SCRIP2
        investment_amount2 = buy_quantity1
        current_price2 = float(saberask1(s2))
        if current_price2 is not None and not check_if_float_zero(current_price2):
            buy_quantity2 = round(investment_amount2 / current_price2, 8)
            # SCRIP3
            current_price3 = float(saberbid1(s3))
            if current_price3 is not None and not check_if_float_zero(current_price3):
                sell_quantity3 = buy_quantity2
                final_price2 = round(sell_quantity3 * current_price3, 3)
    return final_price2

def check_profit_loss(total_price_after_sell, initial_investment, transaction_brokerage, min_profit):
    apprx_brokerage = transaction_brokerage * initial_investment/100 * 3
    min_profitable_price = initial_investment + apprx_brokerage + min_profit
    profit_loss = round(total_price_after_sell - min_profitable_price, 3)
    return profit_loss

def in_check_buy_buy_sell(price1, price2, price3, initial_investment):
    final_price = 0
    # SCRIP1
    current_price1 = price1
    investment_amount1 = initial_investment
    if current_price1 is not None:
        buy_quantity1 = round(investment_amount1 / current_price1, 8)
        # SCRIP2
        investment_amount2 = buy_quantity1
        current_price2 = price2
        if current_price2 is not None:
            buy_quantity2 = round(investment_amount2 / current_price2, 8)
            # SCRIP3
            current_price3 = price3
            if current_price3 is not None:
                sell_quantity3 = buy_quantity2
                final_price = round(sell_quantity3 * current_price3, 3)
    return final_price

boleano = True
soma = 0
momento = []

def mandar(list1):
    intransactions = []
    intransactions1 = []

    profit_loss1 = 0
    profit_lossg = 0
    parou1 = 0
    parou2 = 0
    parou3 = 0
    final_pricex = 0

    global boleano
    global soma
    global transactions
    global transactions2

    print("send")

    initial_investment = 100  # value
    min_profit = 0.1  
    transaction_brokerage = 0.001

    # x = len(sortcrypto2(saberask(list1['s1'])))

    # # comecar com 

    # i = 0
    # j = 50 
    # k = 100
    # while (x > 0):
    #     final_pricex = in_check_buy_buy_sell(float((sortcrypto2(saberask(list1['s1']))[j][0])), float((sortcrypto2(saberask(list1['s2']))[0][0])), float((sortcrypto2(saberbid(list1['s3']))[0][0])), initial_investment)
    #     profit_loss1 = check_profit_loss(final_pricex, initial_investment, transaction_brokerage, min_profit)
    #     if (profit_loss1 >= 0 ):
    #         i = j 
    #         j = math.ceil((j+k)/2)
    #     else:
    #         k = j
    #         j = math.ceil((i+j)/2)
    #     if (i == j) or (j == k): 
    #         break
    #     x -= 1
    
    # parou1 = j 

    # x = len(sortcrypto2(saberask(list1['s1'])))
    # i = 0
    # j = 50 
    # k = 100
    # while (x > 0):
    #     final_pricex = in_check_buy_buy_sell(float((sortcrypto2(saberask(list1['s1'])))[0][0]), float((sortcrypto2(saberask(list1['s2'])))[j][0]), float((sortcrypto2(saberbid(list1['s3'])))[0][0]), initial_investment)
    #     profit_loss1 = check_profit_loss(final_pricex, initial_investment, transaction_brokerage, min_profit)
    #     if (profit_loss1 >= 0):
    #         i = j 
    #         j = math.ceil((j+k)/2)
    #     else:
    #         k = j
    #         j = math.ceil((i+j)/2)
    #     if (i == j) or (j == k): 
    #         break
    #     x -= 1
    
    # parou2 = j

    # x = len(sortcrypto2(saberask(list1['s1'])))
    # i = 0
    # j = 50 
    # k = 100
    # while (x > 0):
    #     final_pricex = in_check_buy_buy_sell(float((sortcrypto2(saberask(list1['s1'])))[0][0]), float((sortcrypto2(saberask(list1['s2'])))[0][0]), float((sortcrypto2(saberbid(list1['s3'])))[j][0]), initial_investment)
    #     profit_loss1 = check_profit_loss(final_pricex, initial_investment, transaction_brokerage, min_profit)
    #     if (profit_loss1 >= 0):
    #         i = j 
    #         j = math.ceil((j+k)/2)
    #     else:
    #         k = j
    #         j = math.ceil((i+j)/2)
    #     if (i == j) or (j == k): 
    #         break
    #     x -= 1
    
    # parou3 = j
    # print(parou1,parou2,parou3)
    # print("parou")

    # for h1 in range(0, parou1):
    #     for h2 in range(0, parou2): 
    #         for h3 in range(0, parou3): 
    #             final_pricex = in_check_buy_buy_sell(float((sortcrypto2(saberask(list1['s1']))[h1][0])), float((sortcrypto2(saberask(list1['s2']))[h2][0])), float((sortcrypto2(saberbid(list1['s3']))[h3][0])), initial_investment)
    #             profit_lossg = check_profit_loss(final_pricex, initial_investment, transaction_brokerage, min_profit)
    #             print(profit_lossg)
    #             if profit_lossg > 0: 
    #                 intransactions.append({'s1':i,'s2': j,'s3': k, 'profit_loss': profit_lossg})
    
    # print(intransactions)

    # for i in range(0, len(intransactions)): 
    #     a = (float((sortcrypto2(saberask(list1['s1'])))[intransactions[i]['s1']][0])*(float(sortcrypto3(saberask(list1['s1']))[intransactions[i]['s1']][1])))
    #     b = (float((sortcrypto2(saberask(list1['s2'])))[intransactions[i]['s2']][0])*(float(sortcrypto3(saberask(list1['s2']))[intransactions[i]['s2']][1]))) * float(saberbid(b11)[99][0])
    #     c = (float((sortcrypto2(saberask(list1['s3'])))[intransactions[i]['s3']][0])*(float(sortcrypto3(saberask(list1['s3']))[intransactions[i]['s3']][1]))) * float(saberbid(b22)[99][0])
    #     if (a > b):
    #         min = b 
    #         if b > c:
    #             min = c
    #         else: 
    #             min = b
    #     else:
    #         min = a 
    #         if a > c: 
    #             min = c
    #         else: 
    #             min = a
    #     intransactions1.append({'posicaolista':intransactions[i],'amount': min})
 
    #     #fazer um sort
    #     #mandar para ordem

    #RECEBER TODOS ALTERAÇÕES DE BUY/SELL / BUY/SELL / BUY/SELL E TRATAR ISSO
    #COMPARAR A QUANTIDADE DO DE CERTA TRANSAÇÃO COMO GETBOOK TANTO ASK QUANTO BID
    #MANDAR A ORDEM COM QUANTIDADE CORRETA

    for i in range(0,len(list1['scrip2'])):
        if (list1['scrip2'])[i] == "/":
            x = i
        
    b1 = (list1['scrip2'])[0:x]
    b11 = b1 + 'BUSD'

    for j in range(0,len(list1['scrip3'])):
        if (list1['scrip3'])[j] == "/":
            k = j
    
    b2 = (list1['scrip3'])[0:x]
    b22 = b2 + 'BUSD'

    print(list1)

    # a = (float((sortcrypto2(saberask(list1['s1'])))[0][0])*(float(sortcrypto3(saberask(list1['s1']))[0][1])))
    # b = (float((sortcrypto2(saberask(list1['s2'])))[0][0])*(float(sortcrypto3(saberask(list1['s2']))[0][1]))) * float(saberbid(b11)[99][0])
    # c = (float((sortcrypto2(saberask(list1['s3'])))[0][0])*(float(sortcrypto3(saberask(list1['s3']))[0][1]))) * float(saberbid(b22)[99][0])
    # print((sortcrypto3(saberask(list1['s1'])))[0][0])
    # print(getBOOKask(list1['s1'])) 

    # if min > 15:
    #     min = 15
    #     place_trade_orders(list1['s1'], list1['s2'], list1['s3'], list1['types'], min)
        
    #print(first_amount)s
    #print(list1)
    #soma += list1["profit_loss"]
    #print(list1)
    #print(transactions)
    print("-----------------------------")
    transactions = []
    transactions2 = []
    boleano = True


def perform_triangular_arbitrage(s1, s2, s3, scrip1, scrip2, scrip3, arbitrage_type, initial_investment,
                                 transaction_brokerage, min_profit):
    global boleano

    if (getBOOKask(s1)) == None:
        return
    if (getBOOKbid(s1)) == None:
        return
    if (getBOOKask(s2)) == None:
        return
    if (getBOOKbid(s2)) == None:
        return
    if (getBOOKask(s3)) == None:
        return
    if (getBOOKbid(s3)) == None:
        return

    final_price = 0.0

    if (arbitrage_type == 'BUY_BUY_BUY'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_buy_buy_buy(
            s1, s2, s3,initial_investment)
    if (arbitrage_type == 'BUY_BUY_SELL'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_buy_buy_sell(
            s1, s2, s3,initial_investment)
    if (arbitrage_type == 'BUY_SELL_BUY'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_buy_sell_buy(
            s1, s2, s3,initial_investment)
    if (arbitrage_type == 'BUY_SELL_SELL'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_buy_sell_sell(
            s1, s2, s3,initial_investment)
    if (arbitrage_type == 'SELL_BUY_BUY'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_sell_buy_buy(
            s1, s2, s3,initial_investment)
    if (arbitrage_type == 'SELL_BUY_SELL'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_sell_buy_sell(
            s1, s2, s3, initial_investment)
    if (arbitrage_type == 'SELL_SELL_BUY'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_sell_sell_buy(
            s1, s2, s3, initial_investment)
    if (arbitrage_type == 'SELL_SELL_SELL'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_sell_sell_sell(
            s1, s2, s3, initial_investment)

    profit_loss = check_profit_loss(
        final_price, initial_investment, transaction_brokerage, min_profit)
            
    if profit_loss > 0:
        print(arbitrage_type)
        print(s1,s2,s3)
        print(profit_loss)
        time.sleep(0.1)
        # print("foi")
        # time.sleep(2.0)
        # # print(profit_loss)
        # transactions.append({'s1': s1, 's2': s2, 's3': s3, 'types': arbitrage_type,
        #                     'scrip1': scrip1, 'scrip2': scrip2, 'scrip3': scrip3, 'profit_loss': profit_loss})
        # #print(sortcrypto(transactions)[len(transactions)-1])
        # if boleano == True:
        #     if transactions[0] != None: 
        #         boleano = False 
        #         mandar(sortcrypto(transactions)[0])
                
        # h = len(transactions)

        # while(h > 0):
        #     h = h-1
        #     final_price2 = check_buy_buy_sell2(sortcrypto(transactions)[h]['s1'],sortcrypto(transactions)[h]['s2'],sortcrypto(transactions)[h]['s3'],initial_investment)
        #     profit_loss2 = check_profit_loss(final_price2, initial_investment, transaction_brokerage, min_profit)
        #     print(profit_loss2)
        #     if profit_loss2 > 0:
        #         transactions2.append({'s1': s1, 's2': s2, 's3': s3, 'types': arbitrage_type,
        #                     'scrip1': scrip1, 'scrip2': scrip2, 'scrip3': scrip3, 'profit_loss': profit_loss})
        #         print(transactions2)
        #         if boleano == True:
        #             if transactions2[0] != None:
        #                 boleano = False
        #                 mandar(sortcrypto(transactions2)[0])
        #                 h = 0

        #transactions são as que tão rolando

# ---------------------------------------------------
def profit_combinations(combination):
    base = combination['base']
    intermediate = combination['intermediate']
    ticker = combination['ticker']

    s1compra = f'{intermediate}{base}'    # Eg: BTCUSDT
    s2compra = f'{ticker}{intermediate}'  # Eg: ETHBTC
    s3compra = f'{base}{ticker}'          # Eg: ETHUSDT

    s1venda = f'{base}{intermediate}'    # Eg: BTCUSDT
    s2venda = f'{intermediate}{ticker}'  # Eg: ETHBTC
    s3venda = f'{ticker}{base}'          # Eg: ETHUSDT

    scrip1 = f'{intermediate}/{base}'    # Eg: BTC/USDT
    scrip2 = f'{ticker}/{intermediate}'  # Eg: ETH/BTC
    scrip3 = f'{ticker}/{base}'          # Eg: ETH/USDT

    # perform_triangular_arbitrage(s1compra, s2compra, s3compra, scrip1, scrip2, scrip3, 'BUY_BUY_BUY', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1compra, s2compra, s3venda, scrip1, scrip2, scrip3, 'BUY_BUY_SELL', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1compra, s2venda, s3venda, scrip1, scrip2, scrip3, 'BUY_SELL_SELL', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1venda, s2venda, s3venda, scrip1, scrip2, scrip3, 'SELL_SELL_SELL', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1compra, s2venda, s3compra, scrip1, scrip2, scrip3, 'BUY_SELL_BUY', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1compra, s2venda, s3venda, scrip1, scrip2, scrip3, 'BUY_SELL_SELL', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1venda, s2compra, s3compra, scrip1, scrip2, scrip3, 'SELL_BUY_BUY', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1venda, s2compra, s3venda, scrip1, scrip2, scrip3, 'SELL_BUY_SELL', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1venda, s2venda, s3compra, scrip1, scrip2, scrip3, 'SELL_SELL_BUY', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    perform_triangular_arbitrage(s1venda, s2venda, s3venda, scrip1, scrip2, scrip3, 'SELL_SELL_SELL', INVESTMENT_AMOUNT_DOLLARS,BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
    

    # time.sleep(1)  nn necessario
# time.sleep(1)
# ---------------------------------------------------
def run(orderbooks, update, orderexec, symbolfilter, lock):
    current_time = datetime.now()
    while True:
        # print(boleano)
        for combinations in symbolfilter:
            try:
                # print(combinations)
                profit_combinations(combinations)  # erro do except print,
                current_time = update['last_update']
                time.sleep(0.01)
            except Exception:
                continue
# ---------------------------------------------------
if __name__ == "__main__":
    # data management
    lock = threading.Lock()
    orderbooks = {}
    orderexec = {}
    orderlast = {}
    ordercancel = {}
    symbolfilter = []
    update = {
        "last_update": None,
    }
    # create websocket threads
    filter = Filter(
        Vmin= 0,
        coin=["BUSD","USDT","USDC"],
        exchange="Filter",
        orderbook=symbolfilter,
        lock=lock,
        main=main
    )
    chain = Chain(
        url="wss://stream.binance.com:9443/ws/!bookTicker",
        orderbook=orderbooks,
        lock=lock
    )
    orders = Order(
        url="wss://stream.binance.com:9443",
        orderbook=orderexec,
        lock=lock
    )

    # start threads
    chain.start()
    # time.sleep(10)
    orders.start()
    time.sleep(1)

    # thread.start_new_thread(binance, ())
    run(orderbooks, update, orderexec, symbolfilter, lock)
