
from datetime import date
import time

from getPrice import getCryptoPrice1

# zabezpieczenie przed leceniem na leb na szyje
# NIE MA XD

usdBalance = 100.0
cryptoBalance = 0.0

TRADE_FEE = 0.25
MIN_PROFIT = TRADE_FEE * 3
MIN_PROFIT += 1

# open config file
configFile = open("config.txt", "r")
configFileContent = configFile.readlines()

# get crypto name
CHOSEN_CRYPTO = configFileContent[0]
CHOSEN_CRYPTO = CHOSEN_CRYPTO[:-1]

# get kraken api key
KRAKEN_API_KEY = configFileContent[1]
KRAKEN_API_KEY = KRAKEN_API_KEY[:-1]

# close config file
configFile.close()

# last 48h prices
HOUR_AMOUNT = 24
LAST_PRICES = []

# loop bool
quit = False

# start trading bool
startTrading = False

# main loop
while not quit:

    # logfile open
    logFile = open("log.txt", "a")

    # get current price and output it
    currentPrice = getCryptoPrice1(CHOSEN_CRYPTO)
    todayDate = date.today()
    currentDate = todayDate.strftime("%d/%m/%Y %H:%M:%S")
    logFile.write("[ PRICE ALERT ] " + CHOSEN_CRYPTO.upper() + " : " + str(currentPrice) + " USD" + "   " + currentDate + "\n")

    # doing stuff with last prices data
    if len(LAST_PRICES) < HOUR_AMOUNT:
        logFile.write("[ ACTION ALERT ] waiting for more data" + "\n")
    else:
        logFile.write("[ ACTION ALERT ] data collected" + "\n")
        LAST_PRICES.append(currentPrice)
        LAST_PRICES.pop(0)
        startTrading = True

    if startTrading:

        # calculate the average price
        averagePrice = sum(LAST_PRICES) / HOUR_AMOUNT

        if currentPrice < averagePrice * MIN_PROFIT:
            logFile.write("[ ACTION ALERT ] buying crypto" + "\n")
            # TEMP KUPOWANIE DLA TESTU
            buyAmount = usdBalance * 0.2
            usdBalance -= buyAmount
            cryptoBalance += (buyAmount / currentPrice)  * (1 - TRADE_FEE)
        elif currentPrice > averagePrice * MIN_PROFIT:
            logFile.write("[ ACTION ALERT ] selling crypto" + "\n")
            # TEMP SPRZEDAZ DLA TESTU
            sellAmount = cryptoBalance * 0.5
            cryptoBalance -= sellAmount
            usdBalance += (sellAmount * currentPrice) * (1 - TRADE_FEE)

    logFile.write(CHOSEN_CRYPTO + " balance : " + str(cryptoBalance) + "\n")
    logFile.write("usd balance : " + str(usdBalance) + "\n")
    logFile.write("combined usd balance : " + str(cryptoBalance*currentPrice+usdBalance) + "\n")
    logFile.write("\n")

    # log file close
    logFile.close()

    # wait for 1 hour
    time.sleep(3600) 

