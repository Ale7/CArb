from research import *
import threading

FREQUENCY = 15.0


def arbitrage():
    threading.Timer(FREQUENCY, arbitrage).start()
    for ex in exchanges:
        get_nonzero_balances(ex.fetch_balance())


logging.basicConfig(filename='BotLogging.log', level=logging.INFO)

log("Started running bot.py")

binance = get_binance_connection(config.binance_api_key, config.binance_api_secret)
bittrex = get_bittrex_connection(config.bittrex_api_key, config.bittrex_api_secret)

database = mysql_connect(config.mysql_host, config.mysql_username, config.mysql_password, config.mysql_db)

mycursor = database.cursor()
exchanges = [binance, bittrex]

arbitrage()
