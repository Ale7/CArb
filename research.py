from exchange import *
import config
import time
import threading

FREQUENCY = 15
ITERATIONS = 480
PROFIT_FLOOR = 0.35
PROFIT_IDEAL = PROFIT_FLOOR + 0.5

RESEARCH_TABLE = "BinanceBittrex"

research_pairs = ['XLM/BTC', 'ETH/BTC', 'LOOM/BTC', 'DASH/BTC', 'TRX/BTC', 'XVG/BTC',
                  'GNT/BTC', 'SC/BTC', 'ARDR/BTC', 'XEM/BTC', 'BAT/BTC', 'ZEC/BTC',
                  'XZC/BTC', 'MANA/BTC', 'ENJ/BTC', 'NEO/BTC', 'SNT/BTC', 'STRAT/BTC',
                  'MFT/BTC', 'ADX/BTC', 'STEEM/BTC', 'ADA/BTC', 'POLY/BTC', 'ENG/BTC',
                  'SYS/BTC', 'GO/BTC', 'CVC/BTC', 'POWR/BTC', 'RVN/BTC', 'XMR/BTC']

database = mycursor = exchanges = None


def harvest_spreads():
    timer = threading.Timer(FREQUENCY, harvest_spreads)
    timer.start()

    sql_binance_bittrex = f"INSERT INTO {RESEARCH_TABLE} (pair, spread, quantity, base, time) " \
                          f"VALUES (%s, %s, %s, %s, %s)"

    for pair in research_pairs:
        base = quantity = 0
        spread = find_spread(exchanges, pair)

        if spread >= PROFIT_FLOOR:
            book1 = exchanges[0].fetch_order_book(pair)
            book2 = exchanges[1].fetch_order_book(pair)

            books = low_high_book(book1, book2)

            if books is None:
                continue

            order_info = find_order_info(books[0], books[1], PROFIT_FLOOR)

            if order_info is [0, 0, 0]:
                continue

            quantity = float(order_info[0])
            if quantity > 0:
                price = float((order_info[1] + order_info[2]) / 2)
                base = price * quantity

        row = (pair, spread, quantity, base, int(time.time()))
        mycursor.execute(sql_binance_bittrex, row)

    database.commit()
    log("INFO", "Committed all SQL statements inserting pair spreads")

    global ITERATIONS
    ITERATIONS -= 1

    if ITERATIONS <= 0:
        timer.cancel()
        return


def main():
    logging.basicConfig(filename='ResearchLogging.log', level=logging.INFO)

    log("INFO", "Started running research.py")

    binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
    bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

    global exchanges, database, mycursor
    exchanges = [binance, bittrex]
    database = mysql_connect(config.mysql_host, config.mysql_username,
                             config.mysql_password, config.mysql_db)
    mycursor = database.cursor()

    harvest_spreads()


if __name__ == '__main__':
    main()
