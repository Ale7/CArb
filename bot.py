from research import *
import threading

FREQUENCY = 5
PROFIT = 1
BOOK_DEPTH = 20


def arbitrage():
    timer = threading.Timer(FREQUENCY, arbitrage)
    timer.start()
    log("Checking for arbitrage opportunities")

    ex1_balances = get_nonzero_balances(exchanges[0].fetch_balance())
    ex2_balances = get_nonzero_balances(exchanges[1].fetch_balance())

    common = list(set(ex1_balances).intersection(ex2_balances))

    for currency in common:
        if currency == "BTC":
            continue
        pair = currency + "/BTC"

        book1 = exchanges[0].fetch_order_book(pair, BOOK_DEPTH)
        book2 = exchanges[1].fetch_order_book(pair, BOOK_DEPTH)
        book_data = find_order_info(book1, book2, PROFIT)

        if int(book_data[1]) == -1 or int(book_data[2]) == -1:
            find_spread(exchanges, pair)
            continue

        spread_info = find_spread(exchanges, pair)
        low_exchange = spread_info[0]
        high_exchange = spread_info[1]
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

        lowest_bal = float(min(ex1_balances[currency], ex2_balances[currency]))
        amount = min(float(book_data[0]), lowest_bal)

        price = book_data[1]

        side_h = "sell"
        price_h = book_data[2]

        log(f"Attempting to place order: {symbol}, {t}, {side}, {amount}, {price}, {params}")
        low_exchange.create_order(symbol, t, side, amount, price, params)
        log(f"Attempting to place order: {symbol}, {t}, {side_h}, {amount}, {price_h}, {params_h}")
        high_exchange.create_order(symbol, t, side_h, amount, price_h, params_h)

        if len(common) < 2:
            timer.cancel()
            return


logging.basicConfig(filename='BotLogging.log', level=logging.INFO)

log("Started running bot.py")

binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

database = mysql_connect(config.mysql_host, config.mysql_username, config.mysql_password, config.mysql_db)

mycursor = database.cursor()
exchanges = [binance, bittrex]

arbitrage()
log("Finished running bot.py")
