import requests
import tweepy as tw
import ssl
from twurl import augment
import pandas as pd

#Twitter API Key and API Secret Key.
my_api_key='Oz8kTPAiPd67MsmJYgzuokRe2'
my_api_secret='qjypQlNsp9m3sBLJunlzzxi3lbVKsDpezhIOng65nlHzkolO4b'

#Authenticate.
auth=tw.OAuthHandler(my_api_key, my_api_secret)
api=tw.API(auth, wait_on_rate_limit=True)

search_query='#SpaceX -filter:retweets'

#Get tweets from the API.
tweets = tw.Cursor(api.search_tweets, q=search_query, lang="en", since="2020-09-16").items(50)

#Store the API responses in a list.
tweets_copy=[]
for tweet in tweets:
    tweets_copy.append(tweet)

print('Total tweets fetched: ', len(tweets_copy))

#Initialize the DataFrame.
tweets_df=pd.DataFrame()

#Populate the DataFrame.
for tweet in tweets_copy:
    hashtags=[]
    try:
        for hashtag in tweet.entities['hashtags']:
            hashtags.append(hashtag['text'])
        text=api.get_status(id=tweet.id, tweet_mode='extended').full_text
    except:
        pass
    tweets_df=tweets_df.append(pd.DataFrame({'user_name':tweet.user.name, 'user_location':tweet.user.location, 'user_description':tweet.user.description, 'user_verified': tweet.user.verified, 'date':tweet.created_at, 'text':text, 'hashtags':[hastags if hashtags else None], 'source':tweet.source}))
    tweets_df=tweets_df.reset_index(drop=True)

print(tweets_df.head())