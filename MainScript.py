#  %%
#  This file is to use the other objects and thread them to allow simutanious collection
import pymongo
import json
from CryptoData import CryptoData
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection._split import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV

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
    
    # lasthour = None
    # print(cryptoDB['Bitcoin'].count_documents({'created_at' : { '$gte' : 1620155677, '$lt' : 1620172771}}))
    # for hour in cryptoDB['BTC_History'].find().sort('time', -1):
    #     if lasthour != None:
    #         print(hour['time'])
    #         if (lasthour - hour['time'] == 0):
    #             print("Break")
    #         # print("From:" + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(hour['time']))) + 
    #         #       " To:" + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lasthour))) + "    Tweets: " 
    #         #         ))    
    #         print(cryptoDB['Bitcoin'].count_documents( {'created_at' : { 'gt' : hour['time'], '$lt' :  hour['time'] + 1440 }}))
    #     lasthour = hour['time']
        
    data = {'tweet' : [], 'mvmt' : []}
    last = None
    # %%
    for hour in cryptoDB['BTC_History'].find().sort('time', -1):
        if (last != None):
            upOrdown = hour['close'] - last['close']
            if (upOrdown > 0 ):
                print("up")
                for tweet in cryptoDB['Bitcoin'].find({'created_at' : { '$gt' : hour['time'], '$lt' :  last['time']}}):
                    data['mvmt'].append("up")
                    data['tweet'].append(tweet['text'])
                    print(tweet['text'])
            else:
                print("down")
                for tweet in cryptoDB['Bitcoin'].find({'created_at' : { '$gt' : hour['time'], '$lt' :  last['time']}}):
                    data['mvmt'].append("down")
                    data['tweet'].append(tweet['text'])
                    print(tweet['text'])
        last = hour
        # %%
        print(len(data['tweet']))
        print(len(data['mvmt']))

        
        # %%
            # split the dataset in training and test set:
docs_train, docs_test, y_train, y_test = train_test_split( data['tweet'], data['mvmt'], test_size=0.25, random_state=None )

    # TASK: Build a vectorizer / classifier pipeline that filters out tokens
    # that are too rare or too frequent
pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
        ('clf', LinearSVC(C=1000)),
    ])

    # TASK: Build a grid search to find out whether unigrams or bigrams are
    # more useful.
    # Fit the pipeline on the training set using grid search for the parameters
parameters = {
        'vect__ngram_range': [(1, 1), (1, 2)],
    }
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
grid_search.fit(docs_train, y_train)
# %%
from sklearn import metrics

# TASK: print the mean and std for each candidate along with the parameter
# settings for all the candidates explored by grid search.
n_candidates = len(grid_search.cv_results_['params'])
for i in range(n_candidates):
    print(i, 'params - %s; mean - %0.2f; std - %0.2f'
             % (grid_search.cv_results_['params'][i],
                grid_search.cv_results_['mean_test_score'][i],
                grid_search.cv_results_['std_test_score'][i]))
# TASK: Predict the outcome on the testing set and store it in a variable
# named y_predicted
y_predicted = grid_search.predict(docs_test)
# Print the classification report
print(metrics.classification_report(y_test, y_predicted))
# Print and plot the confusion matrix
cm = metrics.confusion_matrix(y_test, y_predicted)
print(cm)

import matplotlib.pyplot as plt
plt.matshow(cm)
plt.show()
        
            


        




 
        

# %%
