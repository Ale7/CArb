from app import timestamp, mysql_connect
import logging

logging.basicConfig(filename='DataLogging.log', level=logging.INFO)

logging.info(timestamp() + f" - Started running data.py")

mydb = mysql_connect('67.225.225.24', 'alecwood_user198', 'pass198', 'alecwood_crypto')
logging.info(timestamp() + " - Connected to MySQL database 'alecwood_crypto'")

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM binance")
result = mycursor.fetchall()
logging.info(timestamp() + " - Fetched all rows from 'binance' table")

for x in result:
    print(x)
logging.info(timestamp() + " - Printed all rows from 'binance' table")

logging.info(timestamp() + f" - Finished running data.py")
