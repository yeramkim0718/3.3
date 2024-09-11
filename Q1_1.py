from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv

#삼쩜삼으로 검색한 최신 일주일 기사 URL
URL = "https://www.google.com/search?q=%EC%82%BC%EC%A9%9C%EC%82%BC&sca_esv=1bc5ef0ecf8e9d09&sca_upv=1&tbs=sbd:1,qdr:w&tbm=nws&sxsrf=ADLYWIIjNkY23H162Wb2fF0kAxWGWykSCg:1725431866823&source=lnt&sa=X&ved=2ahUKEwi9_4XM1qiIAxXFzTQHHWnrGCIQpwV6BAgBEAk&biw=1264&bih=945&dpr=1"

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 브라우저를 열지 않고 실행
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(3)

driver.get(URL)
titles = driver.find_elements(By.CLASS_NAME, "n0jPhd")
urls = driver.find_elements(By.CLASS_NAME, "WlydOe")

data = [
    ["title","url"]
     ]

for i in range (0,len(titles)) :
    title = titles[i]
    url = urls[i]
    data.append([title.text, url.get_attribute("href")])

driver.quit()

# csv 파일로 저장
with open("recentweek.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(data)
