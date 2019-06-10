from research import *

BOOK_DEPTH = 5
PROFIT_PERCENT = 0.325


def is_opportunity(low_book, high_book, req):
    if low_book["asks"][0][0] * (100 + req) / 100 < high_book["bids"][0][0]:
        return True
    return False


def find_quantity(book1, book2, floor):
    qty = 0

    if book1["bids"][0][0] > book2["asks"][0][0]:
        low_book = book2
        high_book = book1
    elif book2["bids"][0][0] > book1["asks"][0][0]:
        low_book = book1
        high_book = book2
    else:
        return -1

    while True:
        if is_opportunity(low_book, high_book, floor):
            if low_book["asks"][0][1] > high_book["bids"][0][1]:
                q = high_book["bids"][0][1]
                del high_book["bids"][0]
                low_book["asks"][0][1] -= q
            else:
                q = low_book["asks"][0][1]
                del low_book["asks"][0]
                high_book["bids"][0][1] -= q
            qty += q
        else:
            break

    return qty


simulate_pairs = ['ETH/BTC', 'RVN/BTC']

logging.basicConfig(filename='SimulateLogging.log', level=logging.INFO)

log("Started running simulate.py")

binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

database = mysql_connect(config.mysql_host, config.mysql_username, config.mysql_password, config.mysql_db)
mycursor = database.cursor()

exchanges = [binance, bittrex]

binance_book = {
    "bids": [[0.04, 5.65], [0.0395, 1.05], [0.0393, 0.05], [0.039, 3.85], [0.038, 12.5]],
    "asks": [[0.0415, 3.25], [0.0415, 1.12], [0.043, 2.05], [0.0442, 8.5], [0.0447, 0.01]]
}

bittrex_book = {
    "bids": [[0.0376, 14.5], [0.0375, 0.02], [0.037, 1.15], [0.037, 2.05], [0.0365, 2.05]],
    "asks": [[0.0385, 1.2], [0.0394, 2.0], [0.0399, 0.05], [0.0425, 4.57], [0.0440, 1.12]]
}

quantity = find_quantity(binance_book, bittrex_book, PROFIT_PERCENT)

binance_book = {
    "bids": [[0.04, 5.65], [0.0395, 1.05], [0.0393, 0.05], [0.039, 3.85], [0.038, 12.5]],
    "asks": [[0.0415, 3.25], [0.0415, 1.12], [0.043, 2.05], [0.0442, 8.5], [0.0447, 0.01]]
}

bittrex_book = {
    "bids": [[0.0376, 14.5], [0.0375, 0.02], [0.037, 1.15], [0.037, 2.05], [0.0365, 2.05]],
    "asks": [[0.0385, 1.2], [0.0394, 2.0], [0.0399, 0.05], [0.0425, 4.57], [0.0440, 1.12]]
}

buy = cost("ETH/BTC", bittrex_book, quantity)
sell = cost("ETH/BTC", binance_book, quantity)
profit = round(sell[2] - buy[3], 8)
print(f"Profit: {profit}")
