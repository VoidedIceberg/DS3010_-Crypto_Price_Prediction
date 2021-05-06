# This class is an object to collect data on a periodic timer based on the passed in parameter
#  %%
import cryptocompare
import datetime
import json

class CryptoData:
    def __init__(self):
        # self.api_key = None
        self.client = None
        
    def authenticate(self):
        with open('TwitterAuth.json') as f:
            tokenFile = json.load(f)
        api = cryptocompare.cryptocompare._set_api_key_parameter(tokenFile['CryptoDataKey'])
        coinList = cryptocompare.get_coin_list(format=False)
        print(coinList)
    def getCurrentPrice(self, ticker):
        return cryptocompare.get_price(ticker, currency='USD', full=False)
    def getPastPrice(self, ticker):
            return cryptocompare.get_historical_price(ticker, 'USD', datetime.datetime(2017,6,6))
    def getPastPriceHour(self, ticker):
        return cryptocompare.get_historical_price_hour(ticker, currency='USD')

    
# %%

CD = CryptoData()

CD.authenticate()
print(CD.getCurrentPrice('BTC'))
print(CD.getPastPrice('BTC'))
time = CD.getPastPriceHour("BTC")
# %%
