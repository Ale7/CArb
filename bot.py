from research import *
import threading

FREQUENCY = 15
PROFIT = 0.5
BOOK_DEPTH = 20


def arbitrage():
    threading.Timer(FREQUENCY, arbitrage).start()
    log("Check for arbitrage opportunities")

    ex1_balances = get_nonzero_balances(exchanges[0].fetch_balance())
    log(f"ex1_balances: {ex1_balances}")
    ex2_balances = get_nonzero_balances(exchanges[1].fetch_balance())
    log(f"ex2_balances: {ex2_balances}")

    common = list(set(ex1_balances).intersection(ex2_balances))
    log(f"common: {common}")

    for currency in common:
        log(f"currency: {currency}")
        if currency == "BTC":
            continue
        currency += "/BTC"

        book1 = exchanges[0].fetch_order_book(currency, BOOK_DEPTH)
        log(f"book1: {book1}")
        book2 = exchanges[1].fetch_order_book(currency, BOOK_DEPTH)
        log(f"book2: {book2}")
        book_data = find_order_info(book1, book2, PROFIT)
        log(f"book_data: {book_data}")

        if int(book_data[1]) == -1 or int(book_data[2]) == -1:
            continue

        spread_info = find_spread(exchanges, currency)
        log(f"spread_info: {spread_info}")
        low_exchange = spread_info[0]
        log(f"low_exchange: {low_exchange}")
        high_exchange = spread_info[1]
        log(f"high_exchange: {high_exchange}")

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

        symbol = currency
        t = "limit"
        side = "buy"
        amount = book_data[0]
        price = book_data[1]

        side_h = "sell"
        price_h = book_data[2]

        log(f"Attempting to place order: {symbol}, {t}, {side}, {amount}, {price}, {params}")
        low_exchange.create_order(symbol, t, side, amount, price, params)
        log(f"Attempting to place order: {symbol}, {t}, {side_h}, {amount}, {price_h}, {params_h}")
        high_exchange.create_order(symbol, t, side_h, amount, price_h, params_h)


logging.basicConfig(filename='BotLogging.log', level=logging.INFO)

log("Started running bot.py")

binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

database = mysql_connect(config.mysql_host, config.mysql_username, config.mysql_password, config.mysql_db)

mycursor = database.cursor()
exchanges = [binance, bittrex]

arbitrage()
