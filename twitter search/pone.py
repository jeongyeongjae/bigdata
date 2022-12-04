import codecs
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm
from keras.preprocessing.text import Tokenizer
from keras.layers import Embedding, Dense, LSTM
from keras.models import Sequential
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from konlpy.tag import Okt
import numpy as np

positive = []
negative = []
posneg = []
    
pos = codecs.open("positive_words_self.txt.crdownload", 'rb', encoding='UTF-8')
with open("negative_words_self.txt.crdownload", encoding='utf-8') as neg:
  negative = neg.readlines()

negative = [neg.replace("\n", "") for neg in negative]

with open("positive_words_self.txt.crdownload", encoding='utf-8') as pos:
  positive = pos.readlines()

negative = [neg.replace("\n", "") for neg in negative]
positive = [pos.replace("\n", "") for pos in positive]

labels = []
titles = []

j = 0


for k in tqdm(range(400)):
    num = k * 10 + 1
    csv='tweet_temp.csv'
    soup = BeautifulSoup(csv, 'lxml')
    
    titles = soup.select("a._sp_each_title")
    
    for title in titles:
        title_data = title.text
        clean_title = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…\"\“》]', '', title_data) 
        negative_flag = False

        label = 0
        for i in range(len(negative)):
          if negative[i] in clean_title:
            label = -1
            negative_flag = True
            print("negative 비교단어 : ", negative[i], "clean_title : ", clean_title) 
            break
        if negative_flag == False:
          for i in range(len(positive)):
            if positive[i] in clean_title:
              label = 1
              print("positive 비교단어 : ", positive[i], "clean_title : ", clean_title)
              break
        titles.append(clean_title)
        labels.append(label)

my_title_df = pd.DataFrame({"title":titles, "label":labels})

train_data = pd.read_csv("tweet_temp.csv")
test_data = pd.read_csv("tweet_temp1.csv")

stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

okt = Okt()
X_train = []
for sentence in train_data['tweet_text']:
  temp_X = []
  temp_X = okt.morphs(sentence, stem=True) # 토큰화
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
  X_train.append(temp_X)
  
X_test = []
for sentence in test_data['tweet_text']:
  temp_X = []
  temp_X = okt.morphs(sentence, stem=True) # 토큰화
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
  X_test.append(temp_X)

max_words = 35000
tokenizer = Tokenizer(num_words = max_words)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)


max_len = 20 # 전체 데이터의 길이를 20로 맞춘다
X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

model01=load_model("model.h5")
use=model01.predict(X_test)
labal=np.argmax(use,axis=1)

for i in range(100):
  print("제목 : ", test_data['tweet_text'].iloc[i], "/\t예측한 라벨 : ", labal[i]-1)