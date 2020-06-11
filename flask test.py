#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pymysql
from datetime import datetime
#from openpyxl import Workbook
#from openpyxl import load_workbook
from bs4 import BeautifulSoup
from io import StringIO


# In[2]:


def dbConnection() :
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


# In[17]:


#극장번호와 영화번호로 상영시간표 가져오기
def get_movie_play_by_s_t(subjectSeq, theaterSeq) :
    tuples = []
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'select START_TIME, SEATS_LEFT from movie_play WHERE movie_seq = %s AND theaters_seq = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()'
            curs.execute(sql,(subjectSeq,theaterSeq))
            rs = curs.fetchall()
            return rs
    finally :
        conn.close()


# In[18]:


#선택한 영화가 상영중인 영화관을 알고싶다
def get_movie_play_t_by_s(subject) :
    movieSeq = select_movie_bySubject(subject)
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'select DISTINCT(THEATERS_SEQ) from movie_play WHERE movie_seq = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()'
            curs.execute(sql,(movieSeq))
            rs = curs.fetchall()
            for r in rs :
                print(get_theaterName_by_seq(r[0]))
    finally :
        conn.close()


# In[19]:


#선택한 영화관에서 상영중인 영화를 알고싶다
def get_movie_play_s_by_t(theaters, theaterName) :
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = 'select distinct(MOVIE_SEQ) from movie_play WHERE THEATERS_SEQ = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()'
            curs.execute(sql,(theaterSeq))
            rs = curs.fetchall()
           # for r in rs :
           #     print(get_movieSubject_by_seq(r[0]))
    finally :
        conn.close()
        return rs


# In[20]:


#선택한 영화관에서 상영중인 영화를 알고싶은데 시간표도 같이 가져와주라
def get_movie_play_s_timetable_by_t(theaters, theaterName) :
    src = ''
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    subjectsSeq = get_movie_play_s_by_t(theaters, theaterName) #상영중인 영화
    print(theaters, theaterName)
    for subject in subjectsSeq :
        #print(subject[0], theaterSeq)
        timetable = get_movie_play_by_s_t(subject[0], theaterSeq)
        src = src + get_movieSubject_by_seq(subject[0]) +"|"
        for time in timetable :
            src = src + time[0] + "-" + str(time[1])+", "
        src = src + "||<br>"
    return src


# In[22]:


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


# In[ ]:


ts = select_theaters_seq("LOTTE")
for theatercode in ts :
    url2 = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
    dic2 = {
        "MethodName":"GetPlaySequence",
        "channelType":"MA",
        "osType":"",
        "osVersion":"",
        "playDate":"2020-06-01",
        "cinemaID":"1|1|1018",
        "representationMovieCode":""
    }
    parameters2 = {"paramList":str(dic2)}
    response2 = requests.post(url2,data=parameters2).json()
    movies_response2 = response2['PlaySeqs']['Items']
    timetables = split_movies_by_no(movies_response2)
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


# In[67]:


from flask import Flask
app = Flask(__name__)
 
@app.route('/')
def hello_world():
    src = '<table border="1"><tr><td>O</td><td>O</td></tr><tr><td>O</td><td>O</td></tr></table>'
    return src

@app.route('/test/')
def hello_world2():
    src = '<table border="1"><tr><td>X</td><td>X</td></tr><tr><td>X</td><td>X</td></tr></table>'
    return src

@app.route('/test2/')
def hello_world3():
    return src

@app.route('/timetable/<theaters>/<thName>')
def getTimetable(theaters,thName) :
    src= theaters+" "+thName+"의 영화 상영시간표입니다.<br>"
    theatercode = get_seq_by_theaterName(theaters, thName)
    print(theatercode)
    req3 = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode='+theatercode.replace("C-","")+'&date=20200609')
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

    data = get_movie_play_s_timetable_by_t(theaters,thName)
    src = src+"<p>"+data+"</p>"
    return src

if __name__ == '__main__':
    app.run()


# In[34]:


#특정 영화관만 좌석수 최신화하기
def updateTimetableCGV(theaters,thName) :
    theatercode = get_seq_by_theaterName(theaters, thName)
    print(theatercode)
    req3 = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode='+theatercode.replace("C-","")+'&date=20200609')
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


# In[29]:


def split_movies_by_no(response) :
    movie_no_list = get_movie_no_list(response)
    tuples2 = []
    for movie_no in movie_no_list :
        movies = [item for item in response if item["MovieCode"] == movie_no]
        title = movies[0]["MovieNameKR"]
        timetable = get_time_table(movies)
        tuple2 = (title,timetable)
        tuples2.append(tuple2)
        #print(title,timetable,"\n")
    return tuples2


# In[30]:


def get_movie_no_list(response) :
    movie_no_list = []
    for item in response :
        movie_no = item["MovieCode"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


# In[31]:


def get_time_table(movies):
    tuples = []
    for movie in movies :
        time = movie["StartTime"]
        seats = movie["BookingSeatCount"]
        tuple = (time,seats)
        tuples.append(tuple)
    return tuples


# In[32]:


def updateTimetableLotte(theaters,thName) :
    theatercode = get_seq_by_theaterName(theaters, thName)
    print(theatercode)
    url2 = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
    dic2 = {
        "MethodName":"GetPlaySequence",
        "channelType":"MA",
        "osType":"",
        "osVersion":"",
        "playDate":str(datetime.today().strftime("%Y-%m-%d")),
        "cinemaID":"1|1|"+theatercode.replace("L-",""),
        "representationMovieCode":""
    }
    parameters2 = {"paramList":str(dic2)}
    response2 = requests.post(url2,data=parameters2).json()
    movies_response2 = response2['PlaySeqs']['Items']
    timetables = split_movies_by_no(movies_response2)
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


# In[33]:


updateTimetableLotte("LOTTE","황학")


# In[26]:


str(datetime.today().strftime("%Y-%m-%d"))


# In[48]:


updateTimetable('CGV','압구정')


# In[69]:


tt = get_movie_play_s_timetable_by_t("CGV","압구정")
print(tt)


# In[70]:


select_theaters_seq_all()

