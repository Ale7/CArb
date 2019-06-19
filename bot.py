from research import *
import threading

FREQUENCY = 5
PROFIT_FLOOR = 0.325
PROFIT_IDEAL = PROFIT_FLOOR + 0.5


def arbitrage():
    timer = threading.Timer(FREQUENCY, arbitrage)
    timer.start()
    log("INFO", "Checking for arbitrage opportunities")

    ex1_balances = get_nonzero_balances(exchanges[0].fetch_balance())
    ex2_balances = get_nonzero_balances(exchanges[1].fetch_balance())

    common = list(set(ex1_balances).intersection(ex2_balances))

    for currency in common:
        if currency == "BTC":
            continue
        pair = currency + "/BTC"

        book1 = exchanges[0].fetch_order_book(pair)
        book2 = exchanges[1].fetch_order_book(pair)

        books = low_high_book(book1, book2)

        if books is None:
            continue

        if book1 is books[0]:
            low_exchange = exchanges[0]
            high_exchange = exchanges[1]
        else:
            low_exchange = exchanges[1]
            high_exchange = exchanges[0]

        order_info = find_order_info(books[0], books[1], PROFIT_IDEAL)

        if order_info is [0, 0, 0]:
            continue

        params = params_h = ""

        if low_exchange.id == "bittrex":
            params = {
                "TimeInEffect": "IMMEDIATE_OR_CANCEL"
            }
            params_h = {
                "timeInForce": "IOC"
            }
        elif low_exchange.id == "binance":
            params = {
                "timeInForce": "IOC"
            }
            params_h = {
                "TimeInEffect": "IMMEDIATE_OR_CANCEL"
            }

        symbol = pair
        t = "limit"
        side = "buy"

        lowest_balance = float(min(ex1_balances[currency], ex2_balances[currency]))
        amount = min(float(order_info[0]), lowest_balance)

        price = order_info[1]

        side_h = "sell"
        price_h = order_info[2]

        log("INFO", f"Attempting to place order: {symbol}, {t}, {side}, {amount}, {price}, {params}")
        low_exchange.create_order(symbol, t, side, amount, price, params)
        log("INFO", f"Attempting to place order: {symbol}, {t}, {side_h}, {amount}, {price_h}, {params_h}")
        high_exchange.create_order(symbol, t, side_h, amount, price_h, params_h)

        if len(common) < 2:
            timer.cancel()
            return


logging.basicConfig(filename='BotLogging.log', level=logging.INFO)

log("INFO", "Started running bot.py")

binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

database = mysql_connect(config.mysql_host, config.mysql_username, config.mysql_password, config.mysql_db)

mycursor = database.cursor()
exchanges = [binance, bittrex]

arbitrage()

log("INFO", "Finished running bot.py")
