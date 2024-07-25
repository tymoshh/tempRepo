import requests
from discord import SyncWebhook

WEBHOOK_URL = ""

def sendMsg(stringMessage, WEBHOOK_URL):
    MY_WEBHOOK = SyncWebhook.from_url(WEBHOOK_URL)
    MY_WEBHOOK.send(content=stringMessage)
