from research import *
import logging
import matplotlib.pyplot as plt
import matplotlib.dates as mdate

MIN = 0.325
IDEAL = 0.825

logging.basicConfig(filename='DataLogging.log', level=logging.INFO)

log("INFO", "Started running data.py")

mydb = mysql_connect('67.225.225.24', 'alecwood_user198', 'pass198', 'alecwood_crypto')

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM binance_bittrex_spreads")
result = mycursor.fetchall()
log("INFO", "Fetched all rows from 'binance_bittrex_spreads' table")

charts = {}

for pair in research_pairs:
    charts[pair] = {"x": [], "y": [], "min": [], "ideal": []}

header = "%12s  %12s  %12s" % ("Pair", f">= {MIN}", f">= {IDEAL}")
print(header)

for r in result:
    pair = r[1]
    spread = r[2]
    time = r[3]

    charts[pair].get("x").append(time)
    charts[pair].get("y").append(spread)

    if spread >= MIN:
        charts[pair].get("min").append(spread)
    if spread >= IDEAL:
        charts[pair].get("ideal").append(spread)

log("INFO", "Prepared all data for chart subplots")

for pair in research_pairs:
    m = len(charts[pair].get("min"))
    i = len(charts[pair].get("ideal"))

    line = "%12s  %12s  %12s" % (pair, m, i)
    print(line)

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

    ax.axhline(y=IDEAL, color='g', linestyle="dashed", linewidth=1)
    ax.axhline(y=MIN, color='y', linestyle="dashed", linewidth=1)
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
