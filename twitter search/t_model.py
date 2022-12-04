import pandas as pd 
import numpy as np
import csv

train_data = pd.read_csv("?/comm/train_dataset_1007.csv") #train_dataset_1007.csv 위치, 학습데이터
test_data = pd.read_csv("?/comm/test_dataset_1007.csv") #test_dataset_1007.csv 위치, 학습확인 데이터
stopwords = ("?/comm/korean_stopwords.txt") #korean_stopwords.txt 위치


import konlpy
from konlpy.tag import Okt #한글 형태소 분석기
okt = Okt()


X_train = []
for sentence in train_data['title']:
  temp_X = []
  temp_X = okt.morphs(sentence, stem=True) # 토큰화
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
  X_train.append(temp_X)
  
X_test = []
for sentence in test_data['title']:
  temp_X = []
  temp_X = okt.morphs(sentence, stem=True) # 토큰화
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
  X_test.append(temp_X)

from keras.preprocessing.text import Tokenizer
max_words = 35000 #이미지에 넣을 최대 word 수 
tokenizer = Tokenizer(num_words = max_words) 
tokenizer.fit_on_texts(X_train) #문자 데이터를 입력받아서 리스트 형태로 변환

X_train = tokenizer.texts_to_sequences(X_train) #텍스트 단어를 시퀸스 형태로 변환
X_test = tokenizer.texts_to_sequences(X_test)

y_train = []
y_test = []


for i in range(len(train_data['label'])): #라벨값 비교 1긍정 0중립 -1부정
  if train_data['label'].iloc[i] == 1:
    y_train.append([0, 0, 1])
  elif train_data['label'].iloc[i] == 0:
    y_train.append([0, 1, 0])
  elif train_data['label'].iloc[i] == -1:
    y_train.append([1, 0, 0])

for i in range(len(test_data['label'])):
  if test_data['label'].iloc[i] == 1:
    y_test.append([0, 0, 1])
  elif test_data['label'].iloc[i] == 0:
    y_test.append([0, 1, 0])
  elif test_data['label'].iloc[i] == -1:
    y_test.append([1, 0, 0])

y_train = np.array(y_train)
y_test = np.array(y_test)

from keras.layers import Embedding, Dense, LSTM
from keras.models import Sequential
from keras_preprocessing.sequence import pad_sequences
max_len = 20 # 전체 데이터의 길이를 20로 맞춘다

X_train = pad_sequences(X_train, maxlen=max_len)  
X_test = pad_sequences(X_test, maxlen=max_len)



model = Sequential() #모델생성
model.add(Embedding(max_words, 100))
model.add(LSTM(128))
model.add(Dense(3, activation='softmax'))

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=20, batch_size=20, validation_split=0.1) 
#model.fit(학습 데이터, 레이블 데이터, 전체 데이터셋 20번 반복학습 ,20개의 샘플로 가중치 갱신, 10%의 검증 데이터)

print("{:.2f}".format(model.evaluate(X_test,y_test)[1]*100)) #학습비교 일치확률 95.27%

from keras.models import load_model 
model.save('?/comm/model.h5') #모델저장