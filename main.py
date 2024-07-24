
from datetime import date
import time

from getPrice import getCryptoPrice1

# zabezpieczenie przed leceniem na leb na szyje

usdBalance = 100.0
cryptoBalance = 0.0

TRADE_FEE = 0.25
MIN_PROFIT = TRADE_FEE * 3
MIN_PROFIT += 1

# enter name of the crypto
CHOSEN_CRYPTO = ""
print("enter the name of the crypto you want to trade : ", end="")
CHOSEN_CRYPTO = input()

# enter kraken api key
'''
KRAKEN_API_KEY = ""
print("enter your kraken api key : ", end="")
KRAKEN_API_KEY = input()
'''

# last 48h prices
HOUR_AMOUNT = 72
LAST_PRICES = []

# press enter to start
print()
print("press enter to start ...", end=" ")
input()
print()

# loop bool
quit = False

# start trading bool
startTrading = False

# main loop
while not quit:

    # get current price and output it
    print()
    currentPrice = getCryptoPrice1(CHOSEN_CRYPTO)
    todayDate = date.today()
    currentDate = todayDate.strftime("%d/%m/%Y %H:%M:%S")
    print("[ PRICE ALERT ] " + CHOSEN_CRYPTO.upper() + " : " + str(currentPrice) + " USD" + "   " + currentDate)

    # doing stuff with last prices data
    if len(LAST_PRICES) < HOUR_AMOUNT:
        print("[ ACTION ALERT ] waiting for more data")
    else:
        print("[ ACTION ALERT ] data collected")
        LAST_PRICES.append(currentPrice)
        LAST_PRICES.pop(0)
        startTrading = True

    if startTrading:

        # calculate the average price
        averagePrice = sum(LAST_PRICES) / HOUR_AMOUNT

        if currentPrice < averagePrice * MIN_PROFIT:
            print("[ ACTION ALERT ] buying crypto")
            # TEMP KUPOWANIE DLA TESTU
            buyAmount = usdBalance * 0.2
            usdBalance -= buyAmount
            cryptoBalance += (buyAmount / currentPrice)  * (1 - TRADE_FEE)
        elif currentPrice > averagePrice * MIN_PROFIT:
            print("[ ACTION ALERT ] selling crypto")
            # TEMP SPRZEDAZ DLA TESTU
            sellAmount = cryptoBalance * 0.5
            cryptoBalance -= sellAmount
            usdBalance += (sellAmount * currentPrice) * (1 - TRADE_FEE)

    print(CHOSEN_CRYPTO + " balance : " + str(cryptoBalance))
    print("usd balance : " + str(usdBalance))
    print("combined usd balance : " + str(cryptoBalance*currentPrice+usdBalance))

    # wait for 1 hour
    time.sleep(3600) 

