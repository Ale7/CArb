from research import *
import threading

FREQUENCY = 15.0
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

        x = find_quantity(book1, book2, PROFIT)

        print(x)


logging.basicConfig(filename='BotLogging.log', level=logging.INFO)

log("Started running bot.py")

binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

database = mysql_connect(config.mysql_host, config.mysql_username, config.mysql_password, config.mysql_db)

mycursor = database.cursor()
exchanges = [binance, bittrex]

arbitrage()
