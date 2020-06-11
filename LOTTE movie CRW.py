#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import json
import pymysql
#from openpyxl import Workbook
#from openpyxl import load_workbook
from bs4 import BeautifulSoup
from io import StringIO


# In[3]:


def dbConnection() :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    #conn.query("set character_set_connection=utf8;")
    #conn.query("set character_set_server=utf8;")
    #conn.query("set character_set_client=utf8;")
    #conn.query("set character_set_results=utf8;")
    #conn.query("set character_set_database=utf8;")
    return conn


# In[46]:


url = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
dic = {
    "MethodName":"GetPlaySequence",
    "channelType":"MA",
    "osType":"",
    "osVersion":"",
    "playDate":"2020-05-29",
    "cinemaID":"1|1|1008",
    "representationMovieCode":""
}
parameters = {"paramList":str(dic)}
response = requests.post(url,data=parameters).json()


# In[47]:


response


# In[48]:


movies_response = response['PlaySeqs']['Items']


# In[4]:


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


# In[5]:


def get_movie_no_list(response) :
    movie_no_list = []
    for item in response :
        movie_no = item["MovieCode"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


# In[6]:


def get_time_table(movies):
    tuples = []
    for movie in movies :
        time = movie["StartTime"]
        seats = movie["BookingSeatCount"]
        tuple = (time,seats)
        tuples.append(tuple)
    return tuples


# In[52]:


split_movies_by_no(movies_response)


# In[30]:


theaters = {"cinemaNm" : "가산디지털", "cinemaId": "1013"},{"cinemaNm" : "가양", "cinemaId": "1018"},{"cinemaNm" : "강동", "cinemaId": "9010"},{"cinemaNm" : "건대입구", "cinemaId": "1004"},{"cinemaNm" : "김포공항", "cinemaId": "1009"},{"cinemaNm" : "노원", "cinemaId": "1003"},{"cinemaNm" : "독산", "cinemaId": "1017"},{"cinemaNm" : "브로드웨이(신사)", "cinemaId": "9056"},{"cinemaNm" : "서울대입구", "cinemaId": "1012"},{"cinemaNm" : "수락산", "cinemaId": "1019"},{"cinemaNm" : "수유", "cinemaId": "1022"},{"cinemaNm" : "신도림", "cinemaId": "1015"},{"cinemaNm" : "신림", "cinemaId": "1007"},{"cinemaNm" : "에비뉴엘(명동)", "cinemaId": "1001"},{"cinemaNm" : "영등포", "cinemaId": "1002"},{"cinemaNm" : "용산", "cinemaId": "1014"},{"cinemaNm" : "월드타워", "cinemaId": "1016"},{"cinemaNm" : "은평(롯데몰)", "cinemaId": "1021"},{"cinemaNm" : "장안", "cinemaId": "9053"},{"cinemaNm" : "청량리", "cinemaId": "1008"},{"cinemaNm" : "합정", "cinemaId": "1010"},{"cinemaNm" : "홍대입구", "cinemaId": "1005"},{"cinemaNm" : "황학", "cinemaId": "1011"}


# In[31]:


for theater in theaters :
    print(theater["cinemaNm"]+", "+theater["cinemaId"])


# In[7]:


def insert_theaters_all(obj) :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            for theater in obj :
                sql = 'insert into theaters (THEATERS, THEATERS_SEQ, TH_NAME) values ("LOTTE",%s,%s)'
                curs.execute(sql,("L-"+theater["cinemaId"],theater["cinemaNm"]))
            conn.commit()
            print("입력 성공!")
    finally :
        conn.close()


# In[33]:


insert_theaters_all(theaters)


# In[8]:


def select_movie_bySubject(subject) :
    SEQ = 0
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select MOVIE_SEQ from MOVIE WHERE SUBJECT = %s"
            curs.execute(sql,(subject))
            rs = curs.fetchall()
            if rs == 0 :
                SEQ = 0
            else :
                SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


# In[9]:


def get_movie_seq() :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select MOVIE_SEQ from MOVIE ORDER BY MOVIE_SEQ DESC"
            curs.execute(sql)
            rs = curs.fetchall()
            SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


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


# In[13]:


def insert_movie(SEQ, COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE) :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "insert into MOVIE (MOVIE_SEQ, COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE) values ("+SEQ+",%s,%s,%s,%s,%s,%s)"
            curs.execute(sql,(COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE))
        conn.commit()
        print("입력 성공!")
    finally :
        conn.close()


# In[14]:


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


# In[24]:


ts = select_theaters_seq("LOTTE")
for theatercode in ts :
    url2 = "https://www.lottecinema.co.kr/LCWS/Ticketing/TicketingData.aspx"
    dic2 = {
        "MethodName":"GetPlaySequence",
        "channelType":"MA",
        "osType":"",
        "osVersion":"",
        "playDate":"2020-06-10",
        "cinemaID":"1|1|"+theatercode[0].replace("L-",""),
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


# In[18]:


#영화 번호로 영화이름 가져오기
def get_movieSubject_by_seq(movie_seq) :
    SEQ = 0
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select SUBJECT from MOVIE WHERE MOVIE_SEQ = %s"
            curs.execute(sql,(movie_seq))
            rs = curs.fetchall()
            if rs == 0 :
                SEQ = 0
            else :
                SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


# In[19]:


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


# In[20]:


#극장번호와 영화번호로 상영시간표 가져오기
def get_movie_play_by_s_t(subjectSeq, theaterSeq) :
    conn = dbConnection()
    tuples = []
    try :
        with conn.cursor() as curs :
            sql = 'select START_TIME, SEATS_LEFT from MOVIE_PLAY WHERE movie_seq = %s AND theaters_seq = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()'
            curs.execute(sql,(subjectSeq,theaterSeq))
            rs = curs.fetchall()
            return rs
    finally :
        conn.close()


# In[21]:


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


# In[22]:


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


# In[28]:


get_movie_play_t_by_s("그집")


# In[24]:


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


# In[25]:


#선택한 영화관에서 상영중인 영화를 알고싶은데 시간표도 같이 가져와주라
def get_movie_play_s_timetable_by_t(theaters, theaterName) :
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    subjectsSeq = get_movie_play_s_by_t(theaters, theaterName) #상영중인 영화
    print(theaters, theaterName)
    for subject in subjectsSeq :
        #print(subject[0], theaterSeq)
        timetable = get_movie_play_by_s_t(subject[0], theaterSeq)
        print(get_movieSubject_by_seq(subject[0]), timetable)


# In[29]:


get_movie_play_s_timetable_by_t("LOTTE","황학")


# In[ ]:




