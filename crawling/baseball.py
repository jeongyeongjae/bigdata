from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
import time
import csv
import selenium
from selenium import webdriver

url = "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx"

driver = webdriver.Chrome(executable_path='chromedriver') #크롬드라이버 위치. 같은 폴더에 위치 할 경우 chromedriver만 사용해도 됨
driver.get(url)
time.sleep(1) #지연시간

#12월 1일 확인 메인페이지가 정규시즌 -> 한국시리즈로 변경됨 15~17줄 추가
html = driver.page_source #크롬드아이버에 지정된 페이지 주소 html 저장
driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_ddlSeries_ddlSeries"]/option[1]').click()
time.sleep(1)

html = driver.page_source #크롬드아이버에 지정된 페이지 주소 html 저장
soup = BeautifulSoup(html, 'html.parser') #BeautifulSoup 라이브러리를 이용하여 html 문서를 가저온다
temp1 = soup.find_all('table') #html 문서의 모든 table을 찾아 tmpe1에 저장한다.
p1 = parser.make2d(temp1[0]) #make2d를 이용하여 table 안에 있는 텍스트를 불러와 p1에 저장

driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_ucPager_btnNo2"]').click() #xpath를 이용하여 버튼 클릭 후 페이지 이동
time.sleep(1) #지연시간

html = driver.page_source #이동한 페이지의 html에 저장
soup = BeautifulSoup(html, 'html.parser') 
temp2 = soup.find_all('tbody') #페이지가 이동하면서 다른 부분은 tbody. tbody 안에 있는 모든 텍스트를 불러와 temp2에 저장
p2 = parser.make2d(temp2[0]) #make2d를 이용하여 table 안에 있는 텍스트를 불러와 p2에 저장

driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[2]/div[2]/a[2]').click()
time.sleep(1) #지연시간

driver.close() #크롬드라이버 닫음

#csv
f = open("baseball.csv","w", newline="", encoding='UTF-8') #csv파일을 연다. 파일이 없을 경우 생성 
writer = csv.writer(f)
writer.writerows(p1)
writer.writerows(p2)
f.close()