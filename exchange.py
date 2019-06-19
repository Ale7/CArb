from utility import *
import math


def get_nonzero_balances(exchange_balances):
    balances = {}
    for current, amount in exchange_balances["free"].items():
        if amount > 0:
            balances[f"{current}"] = format(amount, '.8f')
    log("INFO", f"Determined non-zero balances: {balances}")

    return balances


def find_viable_volume(exs, pairs, min_usd):
    low_vol = set()

    min_btc = min_usd / btc_price(exs[0])
    min_eth = min_usd / eth_price(exs[0])

    for ex in exs:
        for pair in pairs:
            ticker_info = ex.fetch_ticker(pair)
            vol = float(ticker_info.get("quoteVolume"))
            sym = ticker_info.get("symbol")

            if "/BTC" not in sym:
                if "/ETH" in sym:
                    if vol < min_eth:
                        low_vol.add(pair)
                else:
                    if vol < min_usd:
                        low_vol.add(pair)
            else:
                if vol < min_btc:
                    low_vol.add(pair)

    pairs = set(pairs)
    plist = pairs - low_vol
    log("INFO", f"Found viable volume pairs: {plist}")

    return plist


def find_common_pairs(exs):
    ex1_tickers = []
    ex2_tickers = []

    i = 0
    while i < 2:
        data = exs[i].fetch_tickers()
        for ticker in data:
            if i == 0:
                ex1_tickers.append(ticker)
            else:
                ex2_tickers.append(ticker)
        i += 1

    common_pairs = list(set(ex1_tickers).intersection(ex2_tickers))
    log("INFO", f"Determined common pairs between exchanges {exs[0].id} and {exs[1].id}: {common_pairs}")

    return common_pairs


def low_high_book(book1, book2):
    low_ask = [math.inf, ""]
    high_bid = [0, ""]

    books = [book1, book2]

    for book in books:
        best_bid = book["bids"][0][0]
        best_ask = book["asks"][0][0]

        if best_bid > high_bid[0]:
            high_bid = [best_bid, book]

        if best_ask < low_ask[0]:
            low_ask = [best_ask, book]

    if high_bid[0] > low_ask[0]:
        return [low_ask[1], high_bid[1]]

    return


def find_spread(exs, pair):
    lowest_ask = math.inf
    highest_bid = 0

    for ex in exs:
        ticker = ex.fetch_ticker(pair)

        bid = ticker.get("bid")
        ask = ticker.get("ask")

        if bid > highest_bid:
            highest_bid = bid

        if ask < lowest_ask:
            lowest_ask = ask

    spread = round((highest_bid - lowest_ask) / lowest_ask * 100, 4)
    log("INFO", f"Found spread of {pair} between exchanges {exs[0].id} and {exs[1].id}: {spread}")

    return spread


def available_liquidity(book, price, buy):
    units = i = 0

    if buy is True:
        b = book["asks"]
        while b[i][0] <= price:
            units += b[i][1]
            i += 1
    else:
        b = book["bids"]
        while b[i][0] >= price:
            units += b[i][1]
            i += 1



    return units


def find_order_info(low_book, high_book, floor):
    low_price = high_price = qty = 0

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

            low_price = low_book["asks"][0][0]
            high_price = high_book["bids"][0][0]
            qty += q
        else:
            break

    log("INFO", f"Found order info - quantity: {qty}, low_price: {low_price}, high_price: {high_price}")
    return [qty, low_price, high_price]


def is_opportunity(low_book, high_book, req):
    if low_book["asks"][0][0] * (100 + req) / 100 < high_book["bids"][0][0]:
        log("INFO", "Arbitrage opportunity found")
        return True
    log("INFO", "Arbitrage opportunity not found")
    return False
