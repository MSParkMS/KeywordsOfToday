import requests
import json

testKey = ""

keyArg = "key="
targetDtArg = "targetDt="
movieCodeArg = "movieCd="
movieNameArg = "movieNm="

# 일별 박스 오피스
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?"
url += keyArg + testKey
url += "&" + targetDtArg + "20200605"    # 2020-06-05

responseData = requests.get(url).text
result = json.loads(responseData)

for boxOffice in result["boxOfficeResult"]["dailyBoxOfficeList"]:
    print(boxOffice["movieNm"] + " : " + boxOffice["movieCd"])

    url2 = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?"
    url2 += keyArg + testKey
    url2 += "&" + movieCodeArg + boxOffice["movieCd"]

    movieResponseData = requests.get(url2).text
    movieResult = json.loads(movieResponseData)

    movieInfo = movieResult["movieInfoResult"]["movieInfo"]

    print("\n영화제목")
    print(movieInfo["movieNm"])

    print("\n장르")
    for genres in movieInfo["genres"]:
        print(genres["genreNm"])

    print("\n감독")
    for directors in movieInfo["directors"]:
        print(directors["peopleNm"])

    print("\n배우")
    for actors in movieInfo["actors"]:
        print(actors["peopleNm"])

    break

url3 = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?"
url3 += keyArg + testKey
url3 += "&" + movieNameArg + "설국열차"

movieListResponseData = requests.get(url3).text
movieListResult = json.loads(movieListResponseData)

movieListInfos = movieListResult["movieListResult"]["movieList"]

for movieListInfo in movieListInfos:
    url4 = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?"
    url4 += keyArg + testKey
    url4 += "&" + movieCodeArg + movieListInfo["movieCd"]

    findResponseData = requests.get(url4).text
    findResult = json.loads(findResponseData)

    movieInfo = findResult["movieInfoResult"]["movieInfo"]

    print("\n영화제목")
    print(movieInfo["movieNm"])

    print("\n장르")
    for genres in movieInfo["genres"]:
        print(genres["genreNm"])

    print("\n감독")
    for directors in movieInfo["directors"]:
        print(directors["peopleNm"])

    print("\n배우")
    for actors in movieInfo["actors"]:
        print(actors["peopleNm"])

    break
