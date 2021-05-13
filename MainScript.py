#  This file is to use the other objects and thread them to allow simutanious collection
import pymongo
import json
from CryptoData import CryptoData
import time

# Fetches the Month histroy and pushes it into mongoDB
def getBTCHistoricalData():
    histroy = CD.getPastPriceHour("BTC") 
    coll = cryptoDB['BTC_History']
    _ = coll.insert_many(histroy)
    
if __name__ == '__main__':
    with open('TwitterAuth.json') as f:
        tokenFile = json.load(f)
    if tokenFile['OAUTH_TOKEN'] != None:
        mongo = pymongo.MongoClient(tokenFile['MongoURL'])
    cryptoDB = mongo['Crypto']
    
    CD = CryptoData()
    CD.authenticate()
    # getBTCHistoricalData()
    
    lasthour = None
    # print(cryptoDB['Bitcoin'].count_documents({'created_at' : { '$gte' : 1620155677, '$lt' : 1620172771}}))
    for hour in cryptoDB['BTC_History'].find().sort('time', -1):
        if lasthour != None:
            if (lasthour - hour['time'] == 0):
                print("Break")
            print("From:" + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(hour['time']))) + 
                  " To:" + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lasthour))) + "    Tweets: " +
                    str(cryptoDB['Bitcoin'].count_documents( {'created_at' : { 'gte' : hour['time'], '$lt' :  lasthour }})))    
        lasthour = hour['time']

        




 
        
