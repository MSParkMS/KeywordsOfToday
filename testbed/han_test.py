import requests
from bs4 import BeautifulSoup

source = requests.get("http://www.hani.co.kr/").text
soup = BeautifulSoup(source, "html.parser")

titles = soup.select(".article-title")

for title in titles:
    print(title.get_text())