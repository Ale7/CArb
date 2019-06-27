from research import *
from config import *
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

PROFIT_FLOOR = 0.325
PROFIT_IDEAL = PROFIT_FLOOR + 0.5

NORMALIZE_LIQUIDITY = 60 / FREQUENCY

logging.basicConfig(filename='DataLogging.log', level=logging.INFO)

log("INFO", "Started running data.py")

mydb = mysql_connect(mysql_host_local, mysql_username_local, mysql_password_local, mysql_db_local)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM binance_bittrex_spreads")
result = mycursor.fetchall()
log("INFO", "Fetched all rows from 'binance_bittrex_spreads' table")

charts = {}

for pair in research_pairs:
    charts[pair] = {"x": [], "y": [], "min": [], "ideal": [], "liquidity": [], "rating": []}

header = "%20s  %20s  %20s  %20s %20s" % ("Pair", f"Spread >= {PROFIT_FLOOR}%",
                                          f"Spread >= {PROFIT_IDEAL}%", "Liquidity", "Rating")
print(header)

for r in result:
    pair = r[1]
    spread = r[2]
    quantity = r[3]
    base = r[4]
    time = r[5]

    charts[pair].get("x").append(time)
    charts[pair].get("y").append(spread)

    if spread >= PROFIT_FLOOR:
        charts[pair].get("min").append(spread)
    if spread >= PROFIT_IDEAL:
        charts[pair].get("ideal").append(spread)

    charts[pair].get("liquidity").append(base)

log("INFO", "Prepared all data for chart subplots")

for pair in research_pairs:
    time_count = len(charts[pair].get("x"))
    floor_count = len(charts[pair].get("min"))
    floor_percent = 100 * floor_count / time_count
    floor_str = f"{floor_count} ({round(floor_percent, 4)}%)"

    ideal_count = len(charts[pair].get("ideal"))
    ideal_percent = 100 * ideal_count / time_count
    ideal_str = f"{ideal_count} ({round(ideal_percent, 4)}%)"

    liquidity = sum(charts[pair].get("liquidity"))
    if liquidity > 0:
        liquidity = liquidity / NORMALIZE_LIQUIDITY
    liquidity_str = round(liquidity, 4)

    rating = math.sqrt(liquidity + 1) * math.sqrt(50 * ideal_count / time_count + 1) - 1
    rating_str = round(rating, 4)

    line = "%20s  %20s  %20s  %20s  %20s" % (pair, floor_str, ideal_str, liquidity_str, rating_str)
    print(line)

log("INFO", "Printed summary data to console")

plt.style.use('dark_background')
fig = plt.figure(num='CArb Charts')
date_fmt = '%H:%M'
date_formatter = mdate.DateFormatter(date_fmt)
mng = plt.get_current_fig_manager()
mng.window.state('zoomed')

for i in range(1, 31):
    ax = fig.add_subplot(5, 6, i)
    pair = research_pairs[i - 1]
    secs = mdate.epoch2num(charts[pair].get("x"))
    ax.plot(secs, charts[pair].get("y"), color="#C0C0C0", linewidth=1)

    ax.axhline(y=PROFIT_IDEAL, color='g', linestyle="dashed", linewidth=1)
    ax.axhline(y=PROFIT_FLOOR, color='y', linestyle="dashed", linewidth=1)
    ax.axhline(y=0, color='r', linewidth=1)

    ax.set_title(pair, size=10)
    ax.grid(color="#2F2F2F", linewidth=1)
    ax.set_facecolor("#191919")
    ax.xaxis.set_major_formatter(date_formatter)

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)

plt.subplots_adjust(left=0.02, right=0.98, bottom=0.05, top=0.95, wspace=0.2, hspace=0.4)
log("INFO", "Displaying data subplots")

mng = plt.get_current_fig_manager()
mng.window.state('zoomed')
plt.show()

log("INFO", "Finished running data.py")
