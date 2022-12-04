from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

options = Options()
# options.add_argument('--kiosk') # 전체화면으로
# options.add_argument('--headless') # 브라우저 안 뜨게

# 크롤링 페이지 url
url = "https://www.koreabaseball.com/Record/Player/HitterBasic/Basic1.aspx" # 사이트 url

driverPath = "C:/Users/user/Desktop/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(driverPath, options=options) # 크롬 열기
driver.get(url) # url 접속

rows = []
name = ''

# 30명 경력 추출(year에 연도 입력)
def crawling(year):
    global name
    for i in range(30):
        try:
            if year != 2022: 
                driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_ddlSeason_ddlSeason"]').click()
                driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_ddlSeason_ddlSeason"]/option[%d]' % (year - 1981)).click()
            time.sleep(3)  
            player = driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_udpContent"]/div[3]/table/tbody/tr[%d]/td[2]/a' % (i+1)).click()
            name = driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_playerProfile_lblName"]').text
            carrer = driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_playerProfile_lblCareer"]').text
            temp = [name, carrer, '-']
            rows.append(temp)
            driver.back()
        except Exception as e:
            print("경력 카테고리 없습니다. 출신교로 찾겠음")
            name = driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_ucRetireInfo_lblName"]').text
            carrer = driver.find_element("xpath",'//*[@id="cphContents_cphContents_cphContents_ucRetireInfo_lblCareer"]').text
            temp = [name, carrer, str(e)]
            rows.append(temp)
            driver.back()

# 2021, 2022년 30명 경력 추출
crawling(2022)
crawling(2021)
crawling(2020)
crawling(2019)

# csv 변환
index = ['선수 이름', '경력', '에러내용']
df = pd.DataFrame(rows, columns = index)
df.to_csv('KBO 선수 경력.csv', encoding = 'UTF-8-sig')