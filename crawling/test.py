import pandas as pd 
import numpy as np
import csv
from google.colab import drive #크롬드라이버 연결

drive.mount('/content/drive')



import urllib.request
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

stopwords = pd.read_csv("/content/word.txt") #불용어 파일
stopwords = [line.rstrip('\n') for line in stopwords]



from konlpy.tag import Kkma, Komoran, Hannanum, Okt
from konlpy.utils import pprint
import konlpy
from konlpy.tag import Mecab
mecab = Mecab()
X_tweet = []
result=pd.read_csv("/content/result.csv")
result['tweet_text'] = result['tweet_text'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣]","  ") #한글과 공백을 제외하고 모두 제거

result['tweet_text'] = result['tweet_text'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣]"," ") #불용어 제거
tweet_corpus ="".join(result['tweet_text'].tolist())
print(tweet_corpus)



from konlpy.tag import Okt
from collections import Counter
#명사 키워드 추출
nouns_tagger = Okt()
nouns = nouns_tagger.nouns(tweet_corpus)
count = Counter(nouns)
#한글자 키워드 제거
remove_char_counter = Counter({x:count[x] for x in count if len(x)>1})
print(remove_char_counter)
most = dict(remove_char_counter.most_common(20)) #상위 20개 단어로 dict생성
most



from matplotlib import font_manager, rc
font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf" #폰트설정, 안하면 한글 깨짐
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

y_pos = np.arange(len(most)) #상위 20개 단어로 barh그래프 생성
plt.figure(figsize=(12,12))
plt.barh(y_pos, most.values())
plt.title('Word Count')
plt.yticks(y_pos, most.keys())
plt.show()