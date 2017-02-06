import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
'''日経'''
BP = "http://www.wul.waseda.ac.jp.ez.wul.waseda.ac.jp/DOMEST/db_about/nikkei/nikkeibp.html"
'''テレコン'''
TELECON = "http://www.wul.waseda.ac.jp.ez.wul.waseda.ac.jp/DOMEST/db_about/nikkei21/nikkei21.html"
'''早稲田図書館'''
WASEDA = 'https://login.ez.wul.waseda.ac.jp/login?url=http://www.wul.waseda.ac.jp/imas/index.html'

WASEDA_USERID = os.environ.get('WASEDA_USERID')
WASEDA_PASSWORD = os.environ.get('WASEDA_PASSWORD')

driver = webdriver.Chrome()
driver.implicitly_wait(2)  # seconds
driver.get("https://login.ez.wul.waseda.ac.jp/login?url=http://www.wul.waseda.ac.jp/imas/index.html")

'''ログインページ'''
time.sleep(2)
userid = driver.find_element_by_name("user")
userid.clear()
userid.send_keys(WASEDA_USERID)

password = driver.find_element_by_name("pass")
password.clear()
password.send_keys(WASEDA_PASSWORD)
password.send_keys(Keys.RETURN)

'''日経検索'''
time.sleep(2)
search = driver.find_element_by_name("all")
search.send_keys("NIKKEI")
search.send_keys(Keys.RETURN)


links = driver.find_elements_by_partial_link_text("日経")
for link in links:
    if link.get_attribute("href") and link.get_attribute("href").find(BP) >= 0:
        driver.execute_script("s = document.querySelectorAll('a');for(i=0;i<s.length;i++){s[i].target='_self'}")
        link.click()
        break

'''日経BPログイン'''
time.sleep(3)
driver.execute_script("s = document.querySelectorAll('a');for(i=0;i<s.length;i++){s[i].target='_self'}")
login = driver.find_elements_by_class_name("A_button")[0]
login.click()


'''BP一覧'''
time.sleep(2)
driver.find_element_by_xpath("//*[contains(text(), '日経マネー')]").click()
'''modal'''
time.sleep(2)
driver.find_element_by_xpath('//*[@id="top_left"]/ul/li[9]/ul/li[6]/div/div[2]/span[2]/a').click()

while True:
    try:
        driver.execute_script("s = document.querySelectorAll('ul.kiji a');for(i=0;i<s.length;i++){s[i].setAttribute('download', '')}")
        links = driver.find_elements_by_css_selector("ul.kiji")
        for link in links:
            link.find_element_by_tag_name("a").click()

        pager = driver.find_element_by_css_selector("div.pager")
        pagenation = pager.find_element_by_partial_link_text("次へ")
        driver.execute_script("arguments[0].click();", pagenation)
        time.sleep(1)
    except:
        break

driver.close()
