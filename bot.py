from research import *
import threading

FREQUENCY = 60
PROFIT = 0.375
BOOK_DEPTH = 20


def arbitrage():
    threading.Timer(FREQUENCY, arbitrage).start()

    # ex1_balances = get_nonzero_balances(exchanges[0].fetch_balance())
    # ex2_balances = get_nonzero_balances(exchanges[1].fetch_balance())

    # common = list(set(ex1_balances).intersection(ex2_balances))
    common = ["KMD", "BTC"]

    for currency in common:
        if currency == "BTC":
            continue
        currency += "/BTC"

        book1 = exchanges[0].fetch_order_book(currency, BOOK_DEPTH)
        book2 = exchanges[1].fetch_order_book(currency, BOOK_DEPTH)
        book_data = find_order_info(book1, book2, PROFIT)

        spread_info = find_spread(exchanges, currency)
        low_exchange = spread_info[0]
        high_exchange = spread_info[1]
        if low_exchange.id == "bittrex":
            symbol = currency
            t = "limit"
            side = "buy"
            amount = book_data[0]
            price = book_data[1]
            params = {
                "TimeInEffect": "IMMEDIATE_OR_CANCEL"
            }
            side_h = "sell"
            price_h = book_data[2]
            params_h = {
                "timeInForce": "IOC"
            }
            low_exchange.create_order(symbol, t, side, amount, price, params)
            high_exchange.create_order(symbol, t, side_h, amount, price_h, params_h)


logging.basicConfig(filename='BotLogging.log', level=logging.INFO)

log("Started running bot.py")

binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

database = mysql_connect(config.mysql_host, config.mysql_username, config.mysql_password, config.mysql_db)

mycursor = database.cursor()
exchanges = [binance, bittrex]

arbitrage()
