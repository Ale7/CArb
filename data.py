import mysql.connector

# SELECT *
# FROM binance bina
# JOIN bittrex trex ON
# 	(bina.pair = trex.pair AND bina.time = trex.time)
# WHERE (bina.buy > trex.buy AND bina.price < trex.price) OR
#       (bina.buy < trex.buy AND bina.price > trex.price)

mydb = mysql.connector.connect(
    host='67.225.225.24',
    user='alecwood_user198',
    passwd='pass198',
    db="alecwood_crypto"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM binance")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)