# This class is an object to collect data on the keyword on a timer timer based on the passed in parameter
#  %%
import twitter
import json
class TwitterData:
    def __init__(self):
        self.auth = None
        self.twitter_api = None
    
    def authenticate(self):
        with open('TwitterAuth.json') as f:
            tokenFile = json.load(f)
        if tokenFile['OAUTH_TOKEN'] != None:
            self.auth = twitter.oauth.OAuth(tokenFile['CONSUMER_KEY'], 
                                            tokenFile['CONSUMER_SECRET'],
                                            tokenFile['OAUTH_TOKEN'], 
                                            tokenFile['OAUTH_TOKEN_SECRET'])

            self.twitter_api = twitter.Twitter(auth=self.auth)
        else:
            print("Please fill out the TwitterAuth.json file to authenticate!")
    
    def getVolume(self, word):
        done = False
        if self.twitter_api == None:
            self.authenticate()
        dateFrom = '2021-05-04'; #Inclusive (YYYY-MM-DD)
        dateTo = '2021-05-05'; #Exclusive (YYYY-MM-DD)
        response = self.twitter_api.search.tweets(q=word, count=100, since = dateFrom, until = dateTo, result_type = 'mixed') 

        countTweets = len(response['statuses']);

        #If all the tweets have been fetched, then we are done
        if not ('next_results' in response['search_metadata']): 
            done = True;

        #If not all the tweets have been fetched, then...
        while (done == False):
        
            #Parsing information for maxID
            parse1 = response['search_metadata']['next_results'].split("&");
            parse2 = parse1[0].split("?max_id=");
            parse3 = parse2[1];
            maxID = parse3;
            
            print(countTweets)
            response = self.twitter_api.search.tweets(q=word, count=100, since = dateFrom, until = dateTo, result_type = 'mixed', max_id = maxID, include_entities = 1) 
            #Updating the total amount of tweets fetched
            countTweets = countTweets + len(response['statuses']);       

            #If all the tweets have been fetched, then we are done
            if not ('next_results' in response['search_metadata']): 
                done = True;
        return  countTweets

# %%

TD = TwitterData()
print(TD.getVolume("North Dakota"))


# %%

  

# %%
