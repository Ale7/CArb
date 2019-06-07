from research import *
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

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

plt.style.use('dark_background')
fig = plt.figure()
date_fmt = '%H:%M'
date_formatter = mdate.DateFormatter(date_fmt)

for i in range(1, 31):
    ax = fig.add_subplot(5, 6, i)
    pair = arb_pairs[i - 1]
    secs = mdate.epoch2num(charts[pair].get("x"))
    ax.plot(secs, charts[pair].get("y"), color="#C0C0C0", linewidth=1)
    ax.axhline(y=0.325, color='g', linestyle="dashed", linewidth=1)
    ax.axhline(y=0, color='r', linewidth=1)
    ax.set_title(pair, size=10)
    ax.grid(color="#2F2F2F", linewidth=1)
    ax.set_facecolor("#191919")
    ax.xaxis.set_major_formatter(date_formatter)
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)

plt.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.95, wspace=0.2, hspace=0.4)
plt.show()

logging.info(timestamp() + f" - Finished running data.py")
