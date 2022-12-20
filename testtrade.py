import ccxt
import math
from env import api_key_testnet, api_secret_testnet, api_key, api_secret
from datetime import datetime
from filter import Filter
from place_orders import Place
from user_data_test import Order
from cancel_orders import Cancel
# from project2.user_data import Order
from all_book_ticker import Chain
import threading
from json import load
from time import sleep

# import os
# cls = os.system("printf '\033c'")
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

exchange = ccxt.binance(test)

exchange.set_sandbox_mode(enabled=True)

params = {
    'test': True,  # test if it's valid, but don't actually place it
}

INVESTMENT_AMOUNT_DOLLARS = 15  # value
MIN_PROFIT_DOLLARS = 0.00001  # poncentagem 0.1 > 10% , 0.01 == 1%, 0.001 == 0.1%
BROKERAGE_PER_TRANSACTION_PERCENT = 0.001  # 0.1 == 0.01% poncentagem

def sortcrypto(list):
    for i in range(0, len(list)-1):
        for j in range(0, len(list)-1):
            if list[j]["profit_loss"] < list[j+1]["profit_loss"]:
                temp = list[j]
                list[j] = list[j+1]
                list[j+1] = temp
    return list


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


def check_if_float_zero(value):
    return math.isclose(value, 0.0, abs_tol=1e-3)


Book = {}
with open("accuracy.json", 'r', encoding='utf-8') as f:
    Book = load(f)


# catch errors


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
    Place("testnet.binance.vision", orderlast,scrip, "BUY", "LIMIT", quantity, price)

def place_sell_order(scrip, quantity, price):
    Place("testnet.binance.vision", orderlast,scrip, "SELL", "LIMIT", quantity, price)

def cancel_order(scrip, clientOrderId):
    Cancel("testnet.binance.vision", ordercancel,scrip, clientOrderId)

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
                            sleep(0.001)

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
                        sleep(0.001)
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
                                    sleep(0.001)
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
                                            sleep(0.001)
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
                                sleep(0.001)

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
                    sleep(0.001)
            # pass

    print("SAIU")

    sleep(4)
    return final_amount

def check_buy_buy_sell(s1, s2, s3, scrip1, scrip2, scrip3, initial_investment):
    final_price = 0
    # SCRIP1
    current_price1 = getBOOKbid(s1)
    investment_amount1 = initial_investment
    if current_price1 is not None and not check_if_float_zero(current_price1):
        buy_quantity1 = round(investment_amount1 / current_price1, 8)
        # SCRIP2

        investment_amount2 = buy_quantity1
        current_price2 = getBOOKbid(s2)
        if current_price2 is not None and not check_if_float_zero(current_price2):
            buy_quantity2 = round(investment_amount2 / current_price2, 8)
            # SCRIP3
            final_price = round(buy_quantity2 * current_price2, 3)
            current_price3 = getBOOKask(s3)
            if current_price3 is not None and not check_if_float_zero(current_price3):
                sell_quantity3 = buy_quantity2
                final_price = round(sell_quantity3 * current_price3, 3)
                # print(f'BUY_BUY_SELL => {scrip1}: {round(investment_amount1 / 1, 6)} / {round(current_price1 / 1, 6)} = {round(buy_quantity1 / 1, 6)} => '
                #       f'{scrip2}: {round(investment_amount2 / 1, 6)} / {round(current_price2 / 1, 6)} = {round(buy_quantity2 / 1, 6)} => '
                #       f'{scrip3}: {round(sell_quantity3 / 1, 6)} * {round(current_price3 / 1, 6)} = {round(final_price / 1, 3)} ')

    return final_price


def check_profit_loss(total_price_after_sell, initial_investment, transaction_brokerage, min_profit):
    apprx_brokerage = transaction_brokerage * initial_investment/100 * 3
    min_profitable_price = initial_investment + apprx_brokerage + min_profit
    profit_loss = round(total_price_after_sell - min_profitable_price, 3)
    return profit_loss

boleano = True 
soma = 0 
transactions = []

def mandar(list1): 
    global boleano 
    global soma 
    global transactions 
    
    print("--------------------------------")
    print("oi")


    soma += list1["profit_loss"]

    #receber uma lista com o book das orders da 1 transação, 2 transação e 3 transação
    #book das orders da 1 transação = booktransacao1
    #book das orders da 2 transação = booktransacao2
    #book das orders da 3 transação = booktransacao3
    #booktransacao = [preço, quantidade] 

    #for i in range(0, len(booktransacao1)){
    # if booktransação(i) == getBookask1 { #neste caso da no mesmo de pegar o preço mais baixo no book de orders
    # quantidade1 = booktransacao[i]['quantidade']
    # }
    # }

    #for i in range(0, len(booktransacao2)){
    # if booktransação(i) == getBookask2 {
    # quantidade2 = booktransacao[i]['quantidade']
    # }
    # }

    #for i in range(0, len(booktransacao3)){
    # if booktransação(i) == getBookask3 {
    # quantidade3 = booktransacao[i]['quantidade'] 
    # }
    # }

    #preço minimo = min(quantiadde1,min(quantidade2,quantidade3))

    #o maior problema de implementar o algoritimo de henrique é a incerteza de que a transação vai rodar o mais rapido possivel 

    #if minimo < 40:
    #initial_amount = minimo
    #else : 
    #minimo = 40 

    #place_trade_orders(list1['s1'], list1['s2'], list1['s3'], list1['types'], initial_investment), quero implementar para pegar o initial investment
    boleano = True
    time.sleep(1.63)

def perform_triangular_arbitrage(s1, s2, s3, scrip1, scrip2, scrip3, arbitrage_type, initial_investment,
                                 transaction_brokerage, min_profit):
    if (getBOOKask(s1)) == None:
        return None
    if (getBOOKbid(s2)) == None:
        return None
    if (getBOOKbid(s3)) == None:
        return None
    # time.sleep(10)
    final_price = 0.0
    if (arbitrage_type == 'BUY_BUY_SELL'):
        # Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
        final_price = check_buy_buy_sell(
            s1, s2, s3, scrip1, scrip2, scrip3, initial_investment)

    profit_loss = check_profit_loss(
        final_price, initial_investment, transaction_brokerage, min_profit)

    if profit_loss > 0:
        global transactions 
        transactions.append({'s1': s1, 's2': s2, 's3': s3, 'types': arbitrage_type, 'scrip1': scrip1, 'scrip2': scrip2, 'scrip3': scrip3, 'profit_loss': profit_loss})

        global boleano
        if boleano == True:
            if transactions[0] != None:
                mandar(sortcrypto(transactions)[0])

        # UNCOMMENT THIS LINE TO PLACE THE ORDERS
        #place_trade_orders(s1, s2, s3, arbitrage_type, initial_investment)
        # sleep(20)


def profit_combinations():
    while True:
        for combinations in symbolfilter:

            base = combinations['base']
            intermediate = combinations['intermediate']
            ticker = combinations['ticker']

            s1 = f'{intermediate}{base}'    # Eg: BTCUSDT
            s2 = f'{ticker}{intermediate}'  # Eg: ETHBTC
            s3 = f'{ticker}{base}'          # Eg: ETHUSDT

            scrip1 = f'{intermediate}/{base}'    # Eg: BTC/USDT
            scrip2 = f'{ticker}/{intermediate}'  # Eg: ETH/BTC
            scrip3 = f'{ticker}/{base}'          # Eg: ETH/USDT
        # Check triangular arbitrage for buy-buy-sell
            # print(f"PROFIT-{str(datetime.now())}: {s1} {s2} {s3}")
            # sleep(60)
        # Check triangular arbitrage for buy-buy-sell
            perform_triangular_arbitrage(s1, s2, s3, scrip1, scrip2, scrip3, 'BUY_BUY_SELL', INVESTMENT_AMOUNT_DOLLARS,
                                         BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS)
        # Sleep to avoid rate limit on api calls (RateLimitExceeded exception)
        # sleep(1)
# def orders():
#      Order(
#         # url="wss://stream.binance.com:9443",
#         url="wss://testnet.binance.vision",
#         orderbook=orderexec,
#         lock=lock
#     )

if __name__ == "__main__":
    # data management
    lock = threading.Lock()
    orderbooks = {}
    orderexec = {}
    orderlast = {}
    ordercancel = {}
    symbolfilter = []
    # create websocket threads
    filter = Filter(
        Vmin=0,
        coin=["BUSD", "USDT"],
        exchange="Filter",
        orderbook=symbolfilter,
        lock=lock,
        main=test
    )
    chain = Chain(
        # url="wss://stream.binance.com:9443/ws/!bookTicker",
        url="wss://testnet.binance.vision",
        orderbook=orderbooks,
        lock=lock
    )
    orders = Order(
        # url="wss://stream.binance.com:9443",
        url="wss://testnet.binance.vision",
        orderbook=orderexec,
        lock=lock
    )
    # start threads
    chain.start()
    sleep(10)
    orders.start()
    sleep(10)
    # y = threading.Thread(target=orders)
    # y.start()
    x = threading.Thread(target=profit_combinations)
    x.start()
