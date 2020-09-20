import requests
import json

class MovieOpenAPI:
    def __init__(self):
        self.testKey = "5a616755c609136c99d80a46c29b66fc"
        self.boxOfficeInfos = {}
        self.movieInfos = {}
        self.peopleInfos = {}

    def gatherBoxOfficeInfos(self):
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?"
        url += "key=" + self.testKey
        url += "&targetDt=20200918"

        responseData = requests.get(url).text
        result = json.loads(responseData)
       
        print("\n박스오피스 순위")
        for dailyBoxOffice in result["boxOfficeResult"]["dailyBoxOfficeList"]:
            movieName = dailyBoxOffice["movieNm"]            
            self.boxOfficeInfos[movieName] = dailyBoxOffice

            print("\n랭킹")
            print(dailyBoxOffice["rank"])
            print("\n랭킹 증감분")
            print(dailyBoxOffice["rankInten"])
            print("\n신규여부")
            print(dailyBoxOffice["rankOldAndNew"])
            print("\n영화제목")
            print(dailyBoxOffice["movieNm"])
            print("\개봉일")
            print(dailyBoxOffice["openDt"])
            print("\n매출액")
            print(dailyBoxOffice["salesAmt"])
            print("\n누적매출액")
            print(dailyBoxOffice["salesAcc"])
            print("\n관객수")
            print(dailyBoxOffice["audiCnt"])
            print("\n누적관객수")
            print(dailyBoxOffice["audiAcc"])
            print("\n스크린수")
            print(dailyBoxOffice["scrnCnt"])
            print("\n상영횟수")
            print(dailyBoxOffice["showCnt"])

        print("\n박스오피스 순위 정보가 캐슁되었습니다.")

    def getMovieGenres(self, movieName):
        movieInfo = self.getMovieInfo(movieName)
        genres = []
        for genre in movieInfo["genres"]:
            genres.append(genre["genreNm"])
        return genres

    def getMovieDirectors(self, movieName):
        movieInfo = self.getMovieInfo(movieName)
        directors = []
        for director in movieInfo["directors"]:
            directors.append(director["peopleNm"])
        return directors

    def getMovieActors(self, movieName, withCastName=False):
        movieInfo = self.getMovieInfo(movieName)
        actors = []
        for actor in movieInfo["actors"]:
            actorInfo = actor["peopleNm"]
            if withCastName and len(actor["cast"]) > 0:
                actorInfo += "-" + actor["cast"]
            actors.append(actorInfo)
        return actors

    def getMovieInfo(self, movieName):
        if movieName in self.movieInfos:
            return self.movieInfos[movieName]

        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?"
        url += "key=" + self.testKey
        url += "&movieNm=" + movieName

        responseData = requests.get(url).text
        result = json.loads(responseData)

        movieCode = result["movieListResult"]["movieList"][0]["movieCd"]   

        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?"
        url += "key=" + self.testKey
        url += "&movieCd=" + movieCode

        findResponseData = requests.get(url).text
        findResult = json.loads(findResponseData)

        movieInfo = findResult["movieInfoResult"]["movieInfo"]
        self.movieInfos[movieName] = movieInfo   # caching movie info by movie name

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

        print("\n영화 정보가 캐슁되었습니다.")
        return self.movieInfos[movieName]

    def getPeopleFilmos(self, peopleName, isActor, withPartName=False):
        peopleInfo = self.getPeopleInfo(peopleName, isActor)
        filmos = []
        for filmo in peopleInfo["filmos"]:
            filmoInfo = filmo["movieNm"]
            if withPartName and len(filmo["moviePartNm"]) > 0:
                filmoInfo += "-" + filmo["moviePartNm"]
            filmos.append(filmoInfo)
        return filmos

    def getPeopleInfo(self, peopleName, isActor):
        if peopleName in self.peopleInfos:
            return self.peopleInfos[peopleName]
        
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?"
        url += "key=" + self.testKey
        url += "&peopleNm=" + peopleName

        responseData = requests.get(url).text
        result = json.loads(responseData)

        peopleCode = 0
        for people in result["peopleListResult"]["peopleList"]:
            if isActor:
                if people["repRoleNm"] == "배우":
                    peopleCode = people["peopleCd"]
                    break
            else:
                if people["repRoleNm"] != "배우":
                    peopleCode = people["peopleCd"]
                    break

        if peopleCode == 0:
            peopleCode = result["peopleListResult"]["peopleList"][0]["peopleCd"]

        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?"
        url += "key=" + self.testKey
        url += "&peopleCd=" + peopleCode

        findResponseData = requests.get(url).text
        findResult = json.loads(findResponseData)

        peopleInfo = findResult["peopleInfoResult"]["peopleInfo"]
        self.peopleInfos[peopleName] = peopleInfo   # caching movie info by people name

        print("\n이름")
        print(peopleInfo["peopleNm"])

        print("\n담당업무")
        print(peopleInfo["repRoleNm"])

        print("\n영화인 정보가 캐슁되었습니다.")
        return self.peopleInfos[peopleName]

movieOpenAPI = MovieOpenAPI()
movieOpenAPI.gatherBoxOfficeInfos()