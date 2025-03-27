import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 웹 브라우져 오픈
driver = webdriver.Chrome()

driver.get("https://kr.investing.com/economic-calendar")
# 로그인 팝업 제거
try:
    driver.find_element(By.CLASS_NAME, 'popupCloseIcon').click()
except:
    print('로그인 팝업 에러')

# 해당 페이지의 html을 파싱
soup = bs(driver.page_source, 'html.parser')

# table 태그중 id가 economicCalendarData 인 태그를 추출
table_data = soup.find(
    'table',
    attrs = {
        'id' : 'economicCalendarData'
    }
)

td_list = table_data.find_all(
    'td',
    attrs= {'class' : 'left event'}
)
link_list = []

for td_data in td_list:
    data = td_data.find('a')['href']
    link_list.append(data)

base_url = "https://kr.investing.com/"

for link in link_list:
    try:
        driver.get(base_url+link)
        time.sleep(10)
        # driver의 html 파싱
        soup2 = bs(driver.page_source, 'html.parser')
        section_data = soup2.find(
            'section',
            attrs={
                'id' : 'leftColumn'
            }
        )
        file_name = section_data.h1.get_text().strip()
        # div 태그중 id가 'eventTabDiv_history_0' 인 태그를 추출
        div_data = soup2.find(
            'div',
            attrs={
                'id' : 'eventTabDiv_history_0'
            }
        )
        # div_data를 문자열로 변경 -> pandas에 내장된 read_html함수를 호출
        df = pd.read_html(
            str(div_data)
        )[0]
        # 데이터프레임을 파일로 저장
        df.to_csv(f"{file_name[:10]}.csv", index=False)
        print(f"{file_name}파일 생성")
    except:
        continue

driver.close()