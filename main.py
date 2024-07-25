
from datetime import datetime, timezone
import time

import socket

from getPrice import getCryptoPrice1

from webhookSender import sendMsg

# zabezpieczenie przed leceniem na leb na szyje
# NIE MA XD

PLATFORM_NAME = socket.gethostname()

usdBalance = 100.0
cryptoBalance = 0.0

TRADE_FEE = 0.25
MIN_PROFIT = TRADE_FEE * 2
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

# initialize webhook
WEBHOOK_URL = configFileContent[2]
WEBHOOK_URL = WEBHOOK_URL[:-1]

# close config file
configFile.close()

# last prices
HOUR_AMOUNT = 12
LAST_PRICES = []

# loop bool
quit = False

# start trading bool
startTrading = False

# main loop
while not quit:

    # message to send
    messageToSend = ""
    
    # add platform name
    messageToSend += "**" + "hostname : " + PLATFORM_NAME + "\n" + "**"

    # add embedding stuff
    messageToSend += "```" + "\n"


    # logfile open
    logFile = open("log.txt", "a")

    # get current price and output it
    
    todayDate = datetime.now(tz=timezone.utc)
    currentDate = todayDate.strftime("%D/%M/%Y %H:%M:%S")
    messageToSend += "date : " + currentDate + " UTC" + "\n"

    # crypto price
    currentPrice = getCryptoPrice1(CHOSEN_CRYPTO)
    messageToSend += CHOSEN_CRYPTO.upper() + " : " + str(currentPrice) + " USD" + "\n"

    # pause
    messageToSend += "\n"

    # doing stuff with last prices data
    if len(LAST_PRICES) < HOUR_AMOUNT:
        messageToSend += "data info : waiting for more data" + "\n"
    else:
        messageToSend += "data info : data updated" + "\n"
        LAST_PRICES.append(currentPrice)
        LAST_PRICES.pop(0)
        startTrading = True

    if startTrading:

        # calculate the average price
        averagePrice = sum(LAST_PRICES) / HOUR_AMOUNT

        if currentPrice < averagePrice * MIN_PROFIT:
            # TEMP KUPOWANIE DLA TESTU
            usdOperationAmount = usdBalance * 0.2
            cryptoOperationAmount = usdOperationAmount / currentPrice
            usdBalance -= usdOperationAmount
            cryptoBalance += cryptoOperationAmount * (1 - TRADE_FEE)
            # add to message
            messageToSend += "trade info : buying " + str(cryptoOperationAmount) + " " + CHOSEN_CRYPTO.upper() + " for " + str(usdOperationAmount) + " USD" + "\n"
        elif currentPrice > averagePrice * MIN_PROFIT:
            # TEMP SPRZEDAZ DLA TESTU
            cryptoOperationAmount = cryptoBalance * 0.5
            usdOperationAmount = (cryptoOperationAmount * currentPrice) * (1 - TRADE_FEE)
            cryptoBalance -= cryptoOperationAmount
            usdBalance += usdOperationAmount
            # add to message
            messageToSend += "trade info : selling " + str(cryptoOperationAmount) + " " + CHOSEN_CRYPTO.upper() + " for " + str(usdOperationAmount) + "\n"

    messageToSend += CHOSEN_CRYPTO + " balance : " + str(cryptoBalance) + "\n"
    messageToSend += "USD balance : " + str(usdBalance) + "\n"
    messageToSend += "combined USD balance : " + str(cryptoBalance*currentPrice+usdBalance) + "\n"
    messageToSend += "\n"

    # add embedding stuff
    messageToSend += "```" + "\n"

    # send message and write to file
    sendMsg(messageToSend, WEBHOOK_URL)
    logFile.write(messageToSend)

    # log file close
    logFile.close()

    # wait for 1 hour
    time.sleep(3600) 

