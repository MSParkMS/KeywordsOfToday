import requests
from bs4 import BeautifulSoup

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