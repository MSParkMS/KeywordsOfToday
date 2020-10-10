#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import requests
import json
import pymysql
from datetime import datetime
#from openpyxl import Workbook
#from openpyxl import load_workbook
from bs4 import BeautifulSoup
from io import StringIO
from flask import Flask, render_template
from movie_open_api import MovieOpenAPI


# In[169]:


def updateTimetable(theaters,thName) :
    if (theaters == "CGV") :
        updateTimetableCGV(theaters,thName)
    if (theaters == "LOTTE") :
        updateTimetableLOTTE(theaters,thName)
    if (theaters == "MEGABOX") :
        updateTimetableMEGABOX(theaters,thName)



def dbConnection() :
    #conn = pymysql.connect(host='localhost',user='root',password='akdlelql12#$',db='today', charset='utf8')
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    #conn.query("set character_set_connection=utf8;")
    #conn.query("set character_set_server=utf8;")
    #conn.query("set character_set_client=utf8;")
    #conn.query("set character_set_results=utf8;")
    #conn.query("set character_set_database=utf8;")
    return conn


# In[3]:


def get_timetable(moive):
    tuples = []
    timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
    #print(timetables)
    for timetable in timetables:
        time = timetable.select_one('em').get_text()        
        seat = timetable.select_one('span').get_text()
        #print(time,seat)
        tuple = (time,seat)
        tuples.append(tuple)
    return tuples


# In[4]:


def seatsUpdate(PLAY_SEQ, SEATS_LEFT) :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'update movie_play SET SEATS_LEFT = %s where PLAY_SEQ = %s'
            rs = curs.execute(sql,(SEATS_LEFT,PLAY_SEQ))
        conn.commit()
        print("갱신 성공!")
    finally :
        conn.close()


# In[5]:


def findPlaySeq(MOVIE_SEQ, THEATERS_SEQ, START_TIME) : 
    conn = dbConnection()
    seq = 0
    try :
        with conn.cursor() as curs :
            sql = 'select PLAY_SEQ from movie_play where MOVIE_SEQ = %s AND THEATERS_SEQ = %s AND START_TIME = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()'
            curs.execute(sql,(MOVIE_SEQ,THEATERS_SEQ,START_TIME))
            rs = curs.fetchall()
            if len(rs) == 0 :
                seq = 0
            else :
                seq = rs[0][0]
            return seq
    finally :
        conn.close()


# In[6]:


def insert_movie(SEQ, COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE) :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "insert into movie (MOVIE_SEQ, COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE) values ("+SEQ+",%s,%s,%s,%s,%s,%s)"
            curs.execute(sql,(COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE))
        conn.commit()
        print("입력 성공!")
    finally :
        conn.close()


# In[7]:


def select_theaters_seq_all() :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select theaters_seq from theaters"
            curs.execute(sql)
            rs = curs.fetchall()
            #for row in rs :
            #    print(row[0])
        return rs
    finally :
        conn.close()


# In[8]:


def select_theaters_seq(THEATERS) :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select theaters_seq from theaters where THEATERS = %s"
            curs.execute(sql,(THEATERS))
            rs = curs.fetchall()
            #for row in rs :
                #print(row[0])
        return rs
    finally :
        conn.close()


# In[9]:


def insert_moviePlay(MOVIE_SEQ, THEATERS_SEQ, START_TIME, RUNNING_TIME, SEATS, SEATS_LEFT) :
    playSeq = findPlaySeq(MOVIE_SEQ, THEATERS_SEQ, START_TIME)
    if(playSeq == 0) :
        conn = dbConnection()
        try :
            with conn.cursor() as curs :
                sql = "insert into movie_play (MOVIE_SEQ, THEATERS_SEQ, START_TIME, RUNNING_TIME, SEATS, SEATS_LEFT) values (%s,%s,%s,%s,"+SEATS+","+SEATS_LEFT+")"
                curs.execute(sql,(MOVIE_SEQ, THEATERS_SEQ, START_TIME, RUNNING_TIME))
            conn.commit()
            print("입력 성공!")
        finally :
            conn.close()
    else :
        seatsUpdate(playSeq, SEATS_LEFT)


# In[10]:


def findPlaySeq(MOVIE_SEQ, THEATERS_SEQ, START_TIME) : 
    conn = dbConnection()
    seq = 0
    try :
        with conn.cursor() as curs :
            sql = 'select PLAY_SEQ from movie_play where MOVIE_SEQ = %s AND THEATERS_SEQ = %s AND START_TIME = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()'
            curs.execute(sql,(MOVIE_SEQ,THEATERS_SEQ,START_TIME))
            rs = curs.fetchall()
            if len(rs) == 0 :
                seq = 0
            else :
                seq = rs[0][0]
            return seq
    finally :
        conn.close()


# In[11]:


def seatsUpdate(PLAY_SEQ, SEATS_LEFT) :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'update movie_play SET SEATS_LEFT = %s where PLAY_SEQ = %s'
            rs = curs.execute(sql,(SEATS_LEFT,PLAY_SEQ))
        conn.commit()
        print("갱신 성공!")
    finally :
        conn.close()


# In[12]:


def get_movie_seq() :
    SEQ=0
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select MOVIE_SEQ from movie ORDER BY MOVIE_SEQ DESC"
            curs.execute(sql)
            rs = curs.fetchall()
            if rs == 0 :
                SEQ = 0
            else :
                SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


# In[13]:


def select_movie_bySubject(subject) :
    SEQ = 0
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select MOVIE_SEQ from movie WHERE SUBJECT = %s"
            curs.execute(sql,(subject))
            rs = curs.fetchall()
            if rs == 0 :
                SEQ = 0
            else :
                SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


# In[14]:


#극장 번호로 극장이름 가져오기
def get_theaterName_by_seq(th_seq) :
    name = []
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select theaters, th_name from theaters WHERE theaters_seq = %s"
            curs.execute(sql,(th_seq))
            rs = curs.fetchall()
            if rs == 0 :
                name = 0
            else :
                name = rs[0][0],rs[0][1]
    finally :
        conn.close()
        return name


# In[15]:


#영화 번호로 영화이름 가져오기
def get_movieSubject_by_seq(movie_seq) :
    SEQ = 0
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select SUBJECT from movie WHERE MOVIE_SEQ = %s"
            curs.execute(sql,(movie_seq))
            rs = curs.fetchall()
            if rs == 0 :
                SEQ = 0
            else :
                SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


# In[16]:


#극장 이름으로 극장번호 가져오기
def get_seq_by_theaterName(theaters, thName) :
    SEQ = 0
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select theaters_seq from theaters WHERE theaters = %s AND th_name = %s"
            curs.execute(sql,(theaters, thName))
            rs = curs.fetchall()
            if rs == 0 :
                SEQ = 0
            else :
                SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


# In[148]:


#선택한 영화가 상영중인 영화관을 알고싶다
def get_movie_play_s_timetable_by_s(movie_seq) :
    #movieSeq = select_movie_bySubject(subject)
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'select A.START_TIME, A.SEATS_LEFT, subject, theaters, th_name from movie_play A, THEATERS B, MOVIE C WHERE A.THEATERS_SEQ = B.THEATERS_SEQ AND A.MOVIE_SEQ = C.MOVIE_SEQ AND A.movie_seq = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()  AND START_TIME > curtime() ORDER BY SUBJECT, START_TIME'
            curs.execute(sql,(movie_seq))
            rs = curs.fetchall()
            return rs
    finally :
        conn.close()


# In[181]:


def get_movie_play_s_timetable_by_s2(movie_seq) :
    #movieSeq = select_movie_bySubject(subject)
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'select distinct(A.THEATERS_SEQ), theaters, th_name from movie_play A, THEATERS B, MOVIE C WHERE A.THEATERS_SEQ = B.THEATERS_SEQ AND A.MOVIE_SEQ = C.MOVIE_SEQ AND A.movie_seq = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()  AND START_TIME > curtime() ORDER BY SUBJECT, START_TIME'
            curs.execute(sql,(movie_seq))
            rs = curs.fetchall()
            return rs
    finally :
        conn.close()


#선택한 영화관에서 상영중인 영화를 알고싶은데 시간표도 같이 가져와주라
def get_movie_play_s_timetable_by_t(theaters, theaterName) :
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'select A.START_TIME, A.SEATS_LEFT, subject, theaters, th_name from movie_play A, THEATERS B, MOVIE C WHERE A.THEATERS_SEQ = B.THEATERS_SEQ AND A.MOVIE_SEQ = C.MOVIE_SEQ AND A.theaters_seq = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()  AND START_TIME > curtime() ORDER BY SUBJECT, START_TIME'
            curs.execute(sql,(theaterSeq))
            rs = curs.fetchall()
            return rs
    finally :
        conn.close()


#특정 영화관만 좌석수 최신화하기
def updateTimetableCGV(theaters,thName) :
    theatercode = get_seq_by_theaterName(theaters, thName)
    print(theatercode)
    req3 = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode='+theatercode.replace("C-",""))
    print('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode='+theatercode.replace("C-","")+'&date=20200609')
    html3 = req3.text
    soup3 = BeautifulSoup(html3, 'html.parser')
    movies3 = soup3.select('body > div > div.sect-showtimes > ul > li')
    #print(movies3)
    for movie in movies3 :
        title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
        
        tuples = []
        timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
        #print(timetables)
        for timetable in timetables:
            time = timetable.select_one('em').get_text()        
            seat = timetable.select_one('span').get_text()
            #print(time,seat)
            tuple = (time,seat)
            tuples.append(tuple)
        #timetable = get_timetable(movie)
        print(title, tuples, '\n')
        
        movie_seq = select_movie_bySubject(title)
        add_seq = get_movie_seq() + 1
        print(movie_seq)
        if movie_seq == 0 :
            insert_movie(str(add_seq), "대한민국", title, "", "", "", "")
            for time in tuples :
                insert_moviePlay(str(add_seq), theatercode, time[0], "", "100", time[1].replace("잔여좌석","").replace("석","").replace("마감","0").replace("매진","0").replace("준비중","0"))
        else :
            for time in tuples :
                insert_moviePlay(str(movie_seq), theatercode, time[0], "", "100", time[1].replace("잔여좌석","").replace("석","").replace("마감","0").replace("매진","0").replace("준비중","0"))


def split_movies_by_no_Lotte(response) :
    movie_no_list = get_movie_no_list_Lotte(response)
    tuples2 = []
    for movie_no in movie_no_list :
        movies = [item for item in response if item["MovieCode"] == movie_no]
        title = movies[0]["MovieNameKR"]
        timetable = get_time_table_Lotte(movies)
        tuple2 = (title,timetable)
        tuples2.append(tuple2)
        #print(title,timetable,"\n")
    return tuples2



def get_movie_no_list_Lotte(response) :
    movie_no_list = []
    for item in response :
        movie_no = item["MovieCode"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list



def get_time_table_Lotte(movies):
    tuples = []
    for movie in movies :
        time = movie["StartTime"]
        seats = movie["BookingSeatCount"]
        tuple = (time,seats)
        tuples.append(tuple)
    return tuples


#특정 영화관만 좌석수 최신화하기
def updateTimetableLOTTE(theaters,thName) :
    theatercode = get_seq_by_theaterName(theaters, thName)
    print(theatercode)
    url2 = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
    dic2 = {
        "MethodName":"GetPlaySequence",
        "channelType":"MA",
        "osType":"",
        "osVersion":"",
        "playDate":str(datetime.today().strftime("%Y-%m-%d")),
        "cinemaID":"1|1|"+str(theatercode).replace("L-",""),
        "representationMovieCode":""
    }
    parameters2 = {"paramList":str(dic2)}
    response2 = requests.post(url2,data=parameters2).json()
    movies_response2 = response2['PlaySeqs']['Items']
    timetables = split_movies_by_no_Lotte(movies_response2)
    for li in timetables : #time[0] - 영화제목, time[1]는 시간표리스트
        title = li[0]
        timetable = li[1]
        print(title, timetable, '\n')
        movie_seq = select_movie_bySubject(title)
        add_seq = get_movie_seq() + 1
        print(movie_seq)
        if movie_seq == 0 :
            insert_movie(str(add_seq), "대한민국", title, "", "", "", "")
            for time in timetable :
                insert_moviePlay(str(add_seq), theatercode, time[0], "", "100", str(time[1]))
        else :
            for time in timetable :
                insert_moviePlay(str(movie_seq), theatercode, time[0], "", "100", str(time[1]))


def split_movies_by_no_Megabox(response) :
    movie_no_list = get_movie_no_list_Megabox(response)
    tuples2 = []
    for movie_no in movie_no_list :
        movies = [item for item in response if item["movieNo"] == movie_no]
        title = movies[0]["movieNm"]
        timetable = get_time_table_Megabox(movies)
        tuple2 = (title,timetable)
        tuples2.append(tuple2)
        #print(title,timetable,"\n")
    return tuples2


def get_movie_no_list_Megabox(response) :
    movie_no_list = []
    for item in response :
        movie_no = item["movieNo"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


def get_time_table_Megabox(movies):
    tuples = []
    for movie in movies :
        time = movie["playStartTime"]
        seats = movie["restSeatCnt"]
        tuple = (time,seats)
        tuples.append(tuple)
    return tuples



#특정 영화관만 좌석수 최신화하기
def updateTimetableMEGABOX(theaters,thName) :
    theatercode = get_seq_by_theaterName(theaters, thName)
    print(theatercode)
    url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
    parameters = {
                "masterType":"brch",
                "detailType":"area",
                "brchNo":theatercode.replace("M-",""),
                "firstAt":"N",
                "brchNo1":theatercode.replace("M-",""),
                "crtDe":str(datetime.today().strftime("%Y%m%d")),
                "playDe":str(datetime.today().strftime("%Y%m%d")),
    }
    response = requests.post(url,data=parameters).json()
    movie_response2 = response['megaMap']['movieFormList']
    timetables= split_movies_by_no_Megabox(movie_response2)
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    for li in timetables : #time[0] - 영화제목, time[1]는 시간표리스트
        title = li[0]
        timetable = li[1]
        print(title, timetable, '\n')
        movie_seq = select_movie_bySubject(title)
        add_seq = get_movie_seq() + 1
        print(movie_seq)
        if movie_seq == 0 :
            insert_movie(str(add_seq), "대한민국", title, "", "", "", "")
            for time in timetable :
                insert_moviePlay(str(add_seq), theatercode, time[0], "", "100", str(time[1]))
        else :
            for time in timetable :
                insert_moviePlay(str(movie_seq), theatercode, time[0], "", "100", str(time[1]))


def select_theaters_all() :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select * from theaters"
            curs.execute(sql)
            rs = curs.fetchall()
            #for row in rs :
            #    print(row[0])
        return rs
    finally :
        conn.close()


#현재 상영중인 영화 목록 가져오기
#select distinct(B.subject) from movie_play A, movie B where A.MOVIE_SEQ = B.MOVIE_SEQ;
def select_playMovieList_all() :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'select distinct(B.subject), A.movie_seq from movie_play A, movie B where A.MOVIE_SEQ = B.MOVIE_SEQ AND date_format(A.REGIST_DATE, "%Y-%m-%d") = CURDATE() AND A.START_TIME > curtime() ORDER BY SUBJECT '
            curs.execute(sql)
            rs = curs.fetchall()
            #for row in rs :
            #    print(row[0])
        return rs
    finally :
        conn.close()

movieOpenAPI = MovieOpenAPI()
movieOpenAPI.gatherBoxOfficeInfos() #박스오피스 정보 OpenAPI에서 가져오기

#선택된 영화 정보를 OpenAPI에서 가져오기
def select_movie_info_by_movie_name(movieName):
    movieInfo = {}
    movieInfo["genres"] = movieOpenAPI.getMovieGenres(movieName)
    movieInfo["directors"] = movieOpenAPI.getMovieDirectors(movieName)
    movieInfo["actors"] = movieOpenAPI.getMovieActors(movieName, True)
    return movieInfo

#선택된 인물 정보를 OpenAPI에서 가져오기
def select_people_info_by_people_name(peopleName, isActor):
    peopleName = peopleName.split("-")[0]
    peopleInfo = {}
    peopleInfo["filmos"] = movieOpenAPI.getPeopleFilmos(peopleName, isActor, True)
    return peopleInfo

app = Flask(__name__)
 
@app.route('/')
def hello_world():
    return render_template (
                'theaterList.html',
                title="영화관 리스트",
                notice = "서울지역 영화관 목록입니다.",
                theaterList = select_theaters_all()
            )

@app.route('/movieTable')
def getMovieTable():
    return render_template(
                'movieList.html',
                title="상영중인 영화",
                notice = "현재 상영중인 영화 목록입니다.",
                movieList = select_playMovieList_all()
            )

@app.route('/movieInfo/<movieName>')
def getMovieInfo(movieName):
    return render_template(
                'movieInfo.html',
                title="영화 정보",
                notice="영화 " + movieName + " 정보입니다.",
                movieInfo=select_movie_info_by_movie_name(movieName)
    )

@app.route('/peopleInfo/<peopleName>/<isActor>')
def getPeopleInfo(peopleName, isActor):
    return render_template(
                'peopleInfo.html',
                title="인물 정보",
                notice="인물 " + peopleName + " 정보입니다.",
                peopleInfo=select_people_info_by_people_name(peopleName, isActor)
    )
    
@app.route('/timetable/<movie_seq>')
def getTimetableForMovie(movie_seq):
    movieName = get_movieSubject_by_seq(movie_seq)
    #선택한 영화가 상영중인 영화관들을 가져와서 갱신시켜줘야함
    pts = get_movie_play_s_timetable_by_s2(movie_seq)
    for pt in pts :
        updateTimetable(pt[1],pt[2])
    return render_template(
                'moviePlayList.html',
                title="Today's Movie -"+movieName,
                notice = movieName+" 상영 시간표입니다.",
                theaterList = get_movie_play_s_timetable_by_s(movie_seq)
            )

@app.route('/timetable/<theaters>/<thName>')
def getTimetable(theaters,thName) :
    updateTimetable(theaters,thName)

    return render_template(
                'timetable.html',
                title="영화시간표",
                notice = theaters+" "+thName+"의 영화 상영시간표입니다.",
                timeList = get_movie_play_s_timetable_by_t(theaters,thName)
            )

@app.route('/boxOffice')
def getBoxOffice():
    return render_template(
                'boxOffice.html',
                title="박스오피스",
                notice="박스오피스 순위",
                boxOfficeList = movieOpenAPI.boxOfficeInfos
            )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)


ts = select_theaters_seq("CGV")
for theatercode in ts :
    req3 = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode='+theatercode[0].replace("C-","")+'&date=20200529')
    html3 = req3.text
    soup3 = BeautifulSoup(html3, 'html.parser')
    movies3 = soup3.select('body > div > div.sect-showtimes > ul > li')
    conn = dbConnection()
    for movie in movies3 :
        title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
        timetable = get_timetable(movie)
        print(title, timetable, '\n')
        movie_seq = select_movie_bySubject(title)
        add_seq = get_movie_seq() + 1
        print(movie_seq)
        if movie_seq == 0 :
            insert_movie(str(add_seq), "대한민국", title, "", "", "", "")
            for time in timetable :
                insert_moviePlay(str(add_seq), theatercode, time[0], "", "100", time[1].replace("잔여좌석","").replace("석","").replace("마감","0").replace("매진","0").replace("준비중","0"))
        else :
            for time in timetable :
                insert_moviePlay(str(movie_seq), theatercode, time[0], "", "100", time[1].replace("잔여좌석","").replace("석","").replace("마감","0").replace("매진","0").replace("준비중","0"))


ts = select_theaters_seq("LOTTE")
for theatercode in ts :
    url2 = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
    dic2 = {
        "MethodName":"GetPlaySequence",
        "channelType":"MA",
        "osType":"",
        "osVersion":"",
        "playDate":str(datetime.today().strftime("%Y-%m-%d")),
        "cinemaID":"1|1|"+theatercode[0].replace("L-",""),
        "representationMovieCode":""
    }
    parameters2 = {"paramList":str(dic2)}
    response2 = requests.post(url2,data=parameters2).json()
    movies_response2 = response2['PlaySeqs']['Items']
    timetables = split_movies_by_no_Lotte(movies_response2)
    for li in timetables : #time[0] - 영화제목, time[1]는 시간표리스트
        title = li[0]
        timetable = li[1]
        print(title, timetable, '\n')
        movie_seq = select_movie_bySubject(title)
        add_seq = get_movie_seq() + 1
        print(movie_seq)
        if movie_seq == 0 :
            insert_movie(str(add_seq), "대한민국", title, "", "", "", "")
            for time in timetable :
                insert_moviePlay(str(add_seq), theatercode, time[0], "", "100", str(time[1]))
        else :
            for time in timetable :
                insert_moviePlay(str(movie_seq), theatercode, time[0], "", "100", str(time[1]))


ts = select_theaters_seq("MEGABOX")
for theatercode in ts :
    url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
    parameters = {
                "masterType":"brch",
                "detailType":"area",
                "brchNo":theatercode[0].replace("M-",""),
                "firstAt":"N",
                "brchNo1":theatercode[0].replace("M-",""),
                "crtDe":str(datetime.today().strftime("%Y%m%d")),
                "playDe":str(datetime.today().strftime("%Y%m%d")),
    }
    response = requests.post(url,data=parameters).json()
    movie_response2 = response['megaMap']['movieFormList']
    timetables= split_movies_by_no_Megabox(movie_response2)
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    for li in timetables : #time[0] - 영화제목, time[1]는 시간표리스트
        title = li[0]
        timetable = li[1]
        print(title, timetable, '\n')
        movie_seq = select_movie_bySubject(title)
        add_seq = get_movie_seq() + 1
        print(movie_seq)
        if movie_seq == 0 :
            insert_movie(str(add_seq), "대한민국", title, "", "", "", "")
            for time in timetable :
                insert_moviePlay(str(add_seq), theatercode, time[0], "", "100", str(time[1]))
        else :
            for time in timetable :
                insert_moviePlay(str(movie_seq), theatercode, time[0], "", "100", str(time[1]))