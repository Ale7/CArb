import ccxt
import mysql.connector
import datetime
import logging


def timestamp():
    return str(datetime.datetime.now())


def log(level, message):
    if level == "DEBUG":
        logging.debug(timestamp() + f" - {message}")
    elif level == "INFO":
        logging.info(timestamp() + f" - {message}")
    elif level == "WARNING":
        logging.warning(timestamp() + f" - {message}")
    elif level == "ERROR":
        logging.error(timestamp() + f" - {message}")
    else:
        logging.critical(timestamp() + f" - {message}")


def mysql_connect(host, username, passwd, db):
    database = mysql.connector.connect(
        host=host,
        user=username,
        passwd=passwd,
        db=db
    )
    log("INFO", f"Connected to MySQL database '{db}'")

    return database


def btc_price(exchange):
    btc = exchange.fetch_ticker("BTC/USDT").get("last")
    log("INFO", f"Found current Bitcoin price: {btc}")

    return btc


def eth_price(exchange):
    eth = exchange.fetch_ticker("ETH/USDT").get("last")
    log("INFO", f"Found current Ethereum price: {eth}")

    return eth


def get_binance_connection(key, secret):
    binance = ccxt.binance({
        'apiKey': key,
        'secret': secret
    })
    log("INFO", "Binance API connection established")

    return binance


def get_bittrex_connection(key, secret):
    bittrex = ccxt.bittrex({
        'apiKey': key,
        'secret': secret
    })
    log("INFO", "Bittrex API connection established")

    return bittrex
