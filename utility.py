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
    try:
        database = mysql.connector.connect(
            host=host,
            user=username,
            passwd=passwd,
            db=db
        )
        log("INFO", f"Successfully connected to MySQL database '{db}'")
        return database
    except Exception as e:
        log("ERROR", f"Failed to connect to MySQL database '{db}': {e}")

    return


def btc_price(exchange):
    try:
        btc = exchange.fetch_ticker("BTC/USDT").get("last")
        log("INFO", f"Found current Bitcoin price on {exchange.id}: {btc}")
        return btc
    except Exception as e:
        log("ERROR", f"Failed to find current Bitcoin price on {exchange.id}: {e}")

    return


def eth_price(exchange):
    try:
        eth = exchange.fetch_ticker("ETH/USDT").get("last")
        log("INFO", f"Found current Ethereum price on {exchange.id}: {eth}")
        return eth
    except Exception as e:
        log("ERROR", f"Failed to find current Ethereum price on {exchange.id}: {e}")

    return


def get_binance_connection(key, secret):
    try:
        binance = ccxt.binance({
            'apiKey': key,
            'secret': secret
        })
        log("INFO", "Successfully established connection to Binance API")
        return binance
    except Exception as e:
        log("ERROR", f"Failed to establish connection to Binance API: {e}")

    return


def get_bittrex_connection(key, secret):
    try:
        bittrex = ccxt.bittrex({
            'apiKey': key,
            'secret': secret
        })
        log("INFO", "Successfully established connection to Bittrex API")
        return bittrex
    except Exception as e:
        log("ERROR", f"Failed to establish connection to bittrex API: {e}")

    return
