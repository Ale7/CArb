from research import *

BOOK_DEPTH = 20

simulate_pairs = ['ETH/BTC', 'RVN/BTC']

logging.basicConfig(filename='SimulateLogging.log', level=logging.INFO)

log("Started running simulate.py")

binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

database = mysql_connect(config.mysql_host, config.mysql_username, config.mysql_password, config.mysql_db)

mycursor = database.cursor()
exchanges = [binance, bittrex]

sql_binance_bittrex_spreads = "INSERT INTO binance_bittrex_spreads (pair, percent_spread, time) VALUES (%s, %s, %s)"

transact_costs = []

while True:

    transact_costs.clear()
    for pair in simulate_pairs:
        spread = find_spread(exchanges, pair)

        if spread > -1:
            for ex in exchanges:
                book = ex.fetch_order_book(pair, BOOK_DEPTH)
                book = prepare_book(book)
                transact_costs.append(cost(pair, book, 1))

    sell_0 = transact_costs[0][2]
    buy_0 = transact_costs[0][3]
    profit_0 = sell_0 - buy_0
    print(profit_0)

    sell_1 = transact_costs[0][2]
    buy_1 = transact_costs[1][3]
    profit_1 = sell_1 - buy_1
    print(profit_1)

    time.sleep(3)
