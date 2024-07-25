import requests

# coingecko version
def getCryptoPrice1(TARGET_CRYPTO_ID) :
    coingeckoResponse = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={TARGET_CRYPTO_ID}&vs_currencies=usd")
    cryptoPriceJson = coingeckoResponse.json()
    return cryptoPriceJson[TARGET_CRYPTO_ID]["usd"]

# kraken version
def getCryptoPrice2(TARGET_CRYPTO_ID):
    print("getCryptoPrice2")