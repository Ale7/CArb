from research import *
import logging
import matplotlib.pyplot as plt

logging.basicConfig(filename='DataLogging.log', level=logging.INFO)

logging.info(timestamp() + f" - Started running data.py")

mydb = mysql_connect('67.225.225.24', 'alecwood_user198', 'pass198', 'alecwood_crypto')
logging.info(timestamp() + " - Connected to MySQL database 'alecwood_crypto'")

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM binance_bittrex_spreads")
result = mycursor.fetchall()
logging.info(timestamp() + " - Fetched all rows from 'binance_bittrex_spreads' table")

charts = {}

for pair in arb_pairs:
    charts[pair] = {"x": [], "y": []}

for r in result:
    pair = r[1]
    spread = r[2]
    time = r[3]

    charts[pair].get("x").append(time)
    charts[pair].get("y").append(spread)

print(charts)

fig, ax = plt.subplots(10, 3)

pair_index = 0

i = 0
while i < 10:
    j = 0
    while j < 3:
        pair = arb_pairs[pair_index]
        chart = ax[i][j]
        chart.set_title(pair, fontsize=8)
        chart.plot(charts[pair].get("x"), charts[pair].get("y"))
        pair_index += 1
        j += 1
    i += 1

plt.grid(True)
plt.show()

logging.info(timestamp() + f" - Finished running data.py")
