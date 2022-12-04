import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os
import csv

import warnings
warnings.filterwarnings("ignore")

#read key
load_dotenv()

api_key = os.getenv("api_key")
api_key_secret = os.getenv("api_key_secret")

access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

columns = ['tweet_text']
df = pd.DataFrame(columns=columns)

korea_geo = "%s,%s,%s"%("35.95","128.25","1000km")
keyword = input("키워드를 입력하세요:")

for i in range(1,100):
  print("Get data", str(i),"%complete..")
  tweets = api.search_tweets(q=keyword, lang="ko", count='100', geocode=korea_geo) #한국에서 만들어진 트윗 100개
  for tweet in tweets:
    tweet_text = tweet.text
    row = [tweet_text]
    series = pd.Series(row, index=df.columns)
    df = df.append(series, ignore_index=True)
print("Get data 100% complete..")

df.drop_duplicates(keep='first',inplace=True) #중복행 제거
df.to_csv("test.csv")