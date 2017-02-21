import os
from selenium import webdriver

# 브라우저 세팅
chrome_path = "../chromedriver.exe"
browser = webdriver.Chrome(chrome_path)

# 클래스넷 접속
browser.get("http://classnet.hongik.ac.kr")
browser.implicitly_wait(1)

# 로그인 페이지로 이동
move_to_login = browser.find_element_by_link_text("통합 로그인 페이지 바로가기")
move_to_login.click()

# 로그인
username = browser.find_element_by_name("USER_ID")
password = browser.find_element_by_name("PASSWD")

username.send_keys(input("ID > "))
password.send_keys(input("PW > "))
password.submit()
browser.implicitly_wait(1)

# 우수 강사 조회 페이지로 이동
browser.get("http://classnet.hongik.ac.kr/class/cnet-php/cn1680/cn1680.php")
browser.implicitly_wait(1)

# 2016년 2학기 우수 강사 조회
browser.find_element_by_xpath("//select[@name='p_yy']/option[text()='2016']").click()
browser.find_element_by_xpath("//select[@name='p_hakgi']/option[@value='2']").click()
browser.find_element_by_xpath("//input[@type='submit' and @value='검색']").click()
browser.implicitly_wait(1)

# HTML로 추출
html = browser.page_source
html = html.replace("euc-kr", "utf-8")
path = "./output"
if not os.path.exists(path):
    os.makedirs(path)
with open(path + "/best_professor.html", mode="w", encoding="utf-8") as fp:
    fp.write(html)
