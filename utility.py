import ccxt
import mysql.connector
import datetime
import logging


def timestamp():
    return str(datetime.datetime.now())


def log(msg):
    logging.info(timestamp() + f" - {msg}")


def mysql_connect(host, username, passwd, db):
    database = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        db=db
    )
    log(f"Connected to MySQL database '{db}'")

    return database


def btc_price(exchange):
    btc = exchange.fetch_ticker("BTC/USDT").get("last")
    log(f"Found current Bitcoin price: {btc}")

    return btc


def eth_price(exchange):
    eth = exchange.fetch_ticker("ETH/USDT").get("last")
    log(f"Found current Ethereum price: {eth}")

    return eth


def get_binance_connection(key, secret):
    binance = ccxt.binance({
        'apiKey': key,
        'secret': secret
    })
    log("Binance API connection established")

    return binance


def get_bittrex_connection(key, secret):
    bittrex = ccxt.bittrex({
        'apiKey': key,
        'secret': secret
    })
    log("Bittrex API connection established")

    return bittrex
