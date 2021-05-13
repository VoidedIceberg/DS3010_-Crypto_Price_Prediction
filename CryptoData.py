# This class is an object to collect data on a periodic timer based on the passed in parameter
#  %%
import cryptocompare
import datetime
import json

class CryptoData:
    def __init__(self):
        # self.api_key = None
        self.api = None
        
    def authenticate(self):
        with open('TwitterAuth.json') as f:
            tokenFile = json.load(f)
        self.api = cryptocompare.cryptocompare._set_api_key_parameter(tokenFile['CryptoDataKey'])
    def getCurrentPrice(self, ticker):
        return cryptocompare.get_price(ticker, currency='USD', full=False)
    def getPastPrice(self, ticker):
            return cryptocompare.get_historical_price(ticker, 'USD', datetime.datetime(2017,6,6))
    def getPastPriceHour(self, ticker):
        if (self.api == None):
            authenticate()
        return cryptocompare.get_historical_price_hour(ticker, currency='USD')

    
# %%
# %%
