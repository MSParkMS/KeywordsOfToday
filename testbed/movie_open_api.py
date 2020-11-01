import requests
import json

from datetime import date, timedelta
from urllib import parse

class MovieOpenAPI:
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)

        self.kobis_api_key = config['KOBIS_API_KEY']
        self.tmdb_api_key = config['TMDB_API_KEY']
        self.boxOfficeInfos = {}
        self.movieInfos = {}
        self.peopleInfos = {}

    def gatherBoxOfficeInfos(self):
        today = date.today()
        yesterday = today - timedelta(days = 1)
        targetDt = yesterday.strftime("%Y%m%d")
        query = {
                    'key' : self.kobis_api_key,
                    'targetDt' : targetDt
                }

        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?"
        url += parse.urlencode(query, encoding='UTF-8', doseq=True)

        responseData = requests.get(url).text
        result = json.loads(responseData)
       
        # print("\n박스오피스 순위")
        for dailyBoxOffice in result["boxOfficeResult"]["dailyBoxOfficeList"]:
            movieName = dailyBoxOffice["movieNm"]            
            self.boxOfficeInfos[movieName] = dailyBoxOffice
            self.getMovieInfo(movieName)

            # print("\n랭킹")
            # print(dailyBoxOffice["rank"])
            # print("\n랭킹 증감분")
            # print(dailyBoxOffice["rankInten"])
            # print("\n신규여부")
            # print(dailyBoxOffice["rankOldAndNew"])
            # print("\n영화제목")
            # print(dailyBoxOffice["movieNm"])
            # print("\개봉일")
            # print(dailyBoxOffice["openDt"])
            # print("\n매출액")
            # print(dailyBoxOffice["salesAmt"])
            # print("\n누적매출액")
            # print(dailyBoxOffice["salesAcc"])
            # print("\n관객수")
            # print(dailyBoxOffice["audiCnt"])
            # print("\n누적관객수")
            # print(dailyBoxOffice["audiAcc"])
            # print("\n스크린수")
            # print(dailyBoxOffice["scrnCnt"])
            # print("\n상영횟수")
            # print(dailyBoxOffice["showCnt"])

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
            actorInfo = {'name': actor["peopleNm"], 'profile': self.getProfilePath(actor["peopleNm"])}
            if withCastName and len(actor["cast"]) > 0:
                actorInfo["name"] += "-" + actor["cast"]
            actors.append(actorInfo)
        return actors

    def getMovieInfo(self, movieName):
        if movieName in self.movieInfos:
            return self.movieInfos[movieName]

        query = {
                    'key' : self.kobis_api_key,
                    'movieNm' : movieName
                }

        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?"
        url += parse.urlencode(query, encoding='UTF-8', doseq=True)

        responseData = requests.get(url).text
        result = json.loads(responseData)

        movieCode = result["movieListResult"]["movieList"][0]["movieCd"]   

        query = {
                    'key' : self.kobis_api_key,
                    'movieCd' : movieCode
                }

        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?"
        url += parse.urlencode(query, encoding='UTF-8', doseq=True)

        findResponseData = requests.get(url).text
        findResult = json.loads(findResponseData)

        movieInfo = findResult["movieInfoResult"]["movieInfo"]
        self.movieInfos[movieName] = movieInfo   # caching movie info by movie name

        query = {
                    'api_key' : self.tmdb_api_key,
                    'language' : 'ko-KR',
                    'query' : movieName,
                    'page' : 1
                }

        url = "https://api.themoviedb.org/3/search/movie?"
        url += parse.urlencode(query, encoding='UTF-8', doseq=True)

        responseData = requests.get(url).text
        result = json.loads(responseData)

        if len(result["results"]) > 0:
            self.movieInfos[movieName]["overview"] = result["results"][0]["overview"]
            self.movieInfos[movieName]["poster_path"] = result["results"][0]["poster_path"]
            self.movieInfos[movieName]["poster300"] = self.getMoviePosterPath(movieName)
        else:
            # try english name
            queryEng = {
                    'api_key' : self.tmdb_api_key,
                    'language' : 'ko-KR',
                    'query' : self.movieInfos[movieName]["movieNmEn"],
                    'page' : 1
            }

            url = "https://api.themoviedb.org/3/search/movie?"
            url += parse.urlencode(queryEng, encoding='UTF-8', doseq=True)

            responseData = requests.get(url).text
            result = json.loads(responseData)

            if len(result["results"]) > 0:
                self.movieInfos[movieName]["overview"] = result["results"][0]["overview"]
                self.movieInfos[movieName]["poster_path"] = result["results"][0]["poster_path"]
                self.movieInfos[movieName]["poster300"] = self.getMoviePosterPath(movieName)
            else:
                # trim the words
                movieNameWithoutWords = movieName
                removeWords = ['파이널컷']
                for removeWord in removeWords:
                    movieNameWithoutWords = movieNameWithoutWords.replace(removeWord, '')
                
                queryWithoutWords = {
                    'api_key' : self.tmdb_api_key,
                    'language' : 'ko-KR',
                    'query' : movieNameWithoutWords,
                    'page' : 1
                }

                url = "https://api.themoviedb.org/3/search/movie?"
                url += parse.urlencode(queryWithoutWords, encoding='UTF-8', doseq=True)

                responseData = requests.get(url).text
                result = json.loads(responseData)

                if len(result["results"]) > 0:
                    self.movieInfos[movieName]["overview"] = result["results"][0]["overview"]
                    self.movieInfos[movieName]["poster_path"] = result["results"][0]["poster_path"]
                    self.movieInfos[movieName]["poster300"] = self.getMoviePosterPath(movieName)

        # print("\n영화제목")
        # print(movieInfo["movieNm"])

        # print("\n장르")
        # for genres in movieInfo["genres"]:
            # print(genres["genreNm"])

        # print("\n감독")
        # for directors in movieInfo["directors"]:
            # print(directors["peopleNm"])

        # print("\n배우")
        # for actors in movieInfo["actors"]:
            # print(actors["peopleNm"])

        # print("\n줄거리")
        # print(self.movieInfos[movieName]["overview"])

        # print("\n포스터주소")
        # print(self.getMoviePosterPath(movieName))

        print("\n영화 정보가 캐슁되었습니다.")
        return self.movieInfos[movieName]

    def getMoviePosterPath(self, movieName, width=300):
        return "https://image.tmdb.org/t/p/w" + str(width) + self.getMovieInfo(movieName)["poster_path"]

    def getPeopleFilmos(self, peopleName, isActor, withPartName=False):
        peopleInfo = self.getPeopleInfo(peopleName)
        filmos = []
        for filmo in peopleInfo["filmos"]:
            filmoInfo = filmo["movieNm"]
            if withPartName and len(filmo["moviePartNm"]) > 0:
                filmoInfo += "-" + filmo["moviePartNm"]
            filmos.append(filmoInfo)
        return filmos

    def getPeopleInfo(self, peopleName, isActor=True):
        if peopleName in self.peopleInfos:
            return self.peopleInfos[peopleName]

        query = {
                    'key' : self.kobis_api_key,
                    'peopleNm' : peopleName
                }
        
        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?"
        url += parse.urlencode(query, encoding='UTF-8', doseq=True)

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

        query = {
                    'key' : self.kobis_api_key,
                    'peopleCd' : peopleCode
                }

        url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json?"
        url += parse.urlencode(query, encoding='UTF-8', doseq=True)

        findResponseData = requests.get(url).text
        findResult = json.loads(findResponseData)

        peopleInfo = findResult["peopleInfoResult"]["peopleInfo"]
        self.peopleInfos[peopleName] = peopleInfo   # caching movie info by people name

        # print("\n이름")
        # print(peopleInfo["peopleNm"])

        # print("\n담당업무")
        # print(peopleInfo["repRoleNm"])

        query = {
                    'api_key' : self.tmdb_api_key,
                    'language' : 'ko-KR',
                    'query' : peopleInfo["peopleNm"],
                    'page' : 1
                }

        url = "https://api.themoviedb.org/3/search/person?"
        url += parse.urlencode(query, encoding='UTF-8', doseq=True)

        responseData = requests.get(url).text
        result = json.loads(responseData)

        if len(result["results"]) > 0:
            self.peopleInfos[peopleName]["profile_path"] = result["results"][0]["profile_path"]

            query = {
                    'api_key' : self.tmdb_api_key,
                    'language' : 'ko-KR'
            }

            url = "https://api.themoviedb.org/3/person/" +  str(result["results"][0]["id"]) + "?"
            url += parse.urlencode(query, encoding='UTF-8', doseq=True)

            responseData = requests.get(url).text
            result = json.loads(responseData)

            self.peopleInfos[peopleName]["birthday"] = result["birthday"]
            self.peopleInfos[peopleName]["deathday"] = result["deathday"]
            self.peopleInfos[peopleName]["biography"] = result["biography"]

        print("\n영화인 정보가 캐슁되었습니다.")
        return self.peopleInfos[peopleName]

    def getProfilePath(self, peopleName, width=300):
        if "profile_path" in self.getPeopleInfo(peopleName):
            if self.getPeopleInfo(peopleName)["profile_path"] is None:
                return "/static/image/default_profile.png"
            else:
                return "https://image.tmdb.org/t/p/w" + str(width) + self.getPeopleInfo(peopleName)["profile_path"]
        else:
            return "/static/image/default_profile.png"