# This class is an object to collect data on the keyword on a timer timer based on the passed in parameter
#  %%
import twitter
import json
import pymongo
import arrow 
import time

class TwitterData:
    def __init__(self):
        self.auth = None
        self.twitter_api = None
        self.mongo = None
        self.db = None
    
    def authenticate(self):
        with open('TwitterAuth.json') as f:
            tokenFile = json.load(f)
        if tokenFile['OAUTH_TOKEN'] != None:
            self.auth = twitter.oauth.OAuth(tokenFile['CONSUMER_KEY'], 
                                            tokenFile['CONSUMER_SECRET'],
                                            tokenFile['OAUTH_TOKEN'], 
                                            tokenFile['OAUTH_TOKEN_SECRET'])

            self.twitter_api = twitter.Twitter(auth=self.auth)
            
            self.mongo = pymongo.MongoClient(tokenFile['MongoURL'])
            self.db = self.mongo['Crypto']
        else:
            print("Please fill out the TwitterAuth.json file to authenticate!")
    
    def getVolume(self, word):
        done = False
        if self.twitter_api == None:
            self.authenticate()
        dateFrom = '2021-05-07'; #Inclusive (YYYY-MM-DD)
        dateTo = '2021-05-10'; #Exclusive (YYYY-MM-DD)
        response = self.twitter_api.search.tweets(q=word, count=100, result_type = 'mixed', since = dateFrom, until = dateTo) 
        
        coll = self.db[word]
   
        countTweets = len(response['statuses']);

        #If all the tweets have been fetched, then we are done
        if not ('next_results' in response['search_metadata']): 
            done = True;

        #If not all the tweets have been fetched, then...
        while (done == False):
            time.sleep(3)
            #Parsing information for maxID
            parse1 = response['search_metadata']['next_results'].split("&");
            parse2 = parse1[0].split("?max_id=");
            parse3 = parse2[1];
            maxID = parse3;
            
            statuses = response['statuses'] #Narows down the jsons feilds

            for status in statuses:
                status['created_at'] = arrow.Arrow.strptime(status['created_at'],"%a %b %d %H:%M:%S %z %Y").timestamp()
            
            print(countTweets)
            response = self.twitter_api.search.tweets(q=word, count=100, result_type = 'mixed', max_id = maxID, include_entities = 1, since = dateFrom, until= dateTo) 
            if response != None:
                _ = coll.insert_many(statuses)
            # Updating the total amount of tweets fetched
            countTweets = countTweets + len(response['statuses']);       

            #If all the tweets have been fetched, then we are done
            if not ('next_results' in response['search_metadata']): 
                done = True;
        return  countTweets

# %%

TD = TwitterData()
print(TD.getVolume("Bitcoin"))


# %%

  

# %%
