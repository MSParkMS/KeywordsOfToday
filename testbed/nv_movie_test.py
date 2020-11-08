import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

'''
source = requests.get("https://movie.naver.com/movie/sdb/rank/rmovie.nhn").text
soup = BeautifulSoup(source, "html.parser")

movies = soup.select(".tit3")

for movie in movies:
    tag = movie.select_one("td.title > div > a")
    if tag is None:
        continue
    if tag["href"] is None:
        continue

    movieCode = tag["href"].split("=")[1]

    print("\n영화이름\n")
    print(tag.get_text())
    print(tag["href"])
    print(movieCode)

    movieURL = "https://movie.naver.com/movie/bi/mi/detail.nhn?code=" + movieCode
    movieSource = requests.get(movieURL).text
    movieSoup = BeautifulSoup(movieSource, "html.parser")\

    director = movieSoup.select_one(".director > .dir_obj > .dir_product > a")
    if director is None:
        continue

    print("\n감독\n")
    print(director.get_text())
    print(director["href"])

    actors = movieSoup.select(".lst_people > li > .p_info > a")
    if actors is None:
        continue

    print("\n배우\n")
    for actor in actors:
        print(actor.get_text())
        print(actor["href"])
'''

driver = webdriver.Chrome('chromedriver')
driver.get("https://movie.naver.com")
time.sleep(3)

element = driver.find_element_by_id("ipt_tx_srch")
element.send_keys('도굴')

driver.find_element_by_class_name("btn_srch").click()
driver.find_element_by_xpath('//*[@id="old_content"]/ul[2]/li[1]/dl/dt/a').click()
driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[5]/a').click()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

result = soup.find("div", class_ = "grade_audience").find("span", class_ = "st_on")
print(float(result["style"].split(':')[1][:-1]))

driver.switch_to_default_content()
driver.switch_to_frame('pointAfterListIframe')

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

content_list = soup.find("div", class_ = "score_result").find_all('li')
for li in content_list :
    temp_review = li.find("div", class_ = "score_reple").find("p").get_text()
    temp_review = temp_review.strip()
    temp_review = temp_review.replace("\n\t", "")
    temp_review = temp_review.replace("\t", "")
    temp_review = temp_review.replace("관람객\n\n", "")
    print(temp_review)

driver.close()