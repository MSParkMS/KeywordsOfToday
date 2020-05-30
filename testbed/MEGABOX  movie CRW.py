#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pymysql
from openpyxl import Workbook
from openpyxl import load_workbook
from bs4 import BeautifulSoup
from io import StringIO


# In[49]:


#brchNo 가 극장 번호임
url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
parameters = {
            "masterType":"brch",
            "detailType":"area",
            "brchNo":"1372",
            "firstAt":"N",
            "brchNo1":"1372",
            "crtDe":"20200527",
            "playDe":"20200527"
}
response = requests.post(url,data=parameters).json()


# In[50]:


movie_response = response['megaMap']['movieFormList']
print(movie_response)


# In[34]:


def split_movies_by_no(response) :
    movie_no_list = get_movie_no_list(response)
    tuples2 = []
    for movie_no in movie_no_list :
        movies = [item for item in response if item["movieNo"] == movie_no]
        title = movies[0]["movieNm"]
        timetable = get_time_table(movies)
        tuple2 = (title,timetable)
        tuples2.append(tuple2)
        #print(title,timetable,"\n")
    return tuples2


# In[5]:


def get_movie_no_list(response) :
    movie_no_list = []
    for item in response :
        movie_no = item["movieNo"]
        if movie_no not in movie_no_list:
            movie_no_list.append(movie_no)
    return movie_no_list


# In[6]:


def get_time_table(movies):
    tuples = []
    for movie in movies :
        time = movie["playStartTime"]
        seats = movie["restSeatCnt"]
        tuple = (time,seats)
        tuples.append(tuple)
    return tuples


# In[36]:


test= split_movies_by_no(movie_response)
for t in test :
    print(t[0])


# In[90]:


theaters = {"brchNm" : "강남", "brchNo": "1372"},{"brchNm" : "강남대로(씨티)", "brchNo": "1359"},{"brchNm" : "강동", "brchNo": "1341"},{"brchNm" : "동대문", "brchNo": "1003"},{"brchNm" : "마곡", "brchNo": "1572"},{"brchNm" : "목동", "brchNo": "1581"},{"brchNm" : "상봉", "brchNo": "1311"},{"brchNm" : "상암월드컵경기장", "brchNo": "1211"},{"brchNm" : "성수", "brchNo": "1331"},{"brchNm" : "센트럴", "brchNo": "1371"},{"brchNm" : "송파파크하비오", "brchNo": "1381"},{"brchNm" : "신촌", "brchNo": "1202"},{"brchNm" : "은평", "brchNo": "1221"},{"brchNm" : "이수", "brchNo": "1561"},{"brchNm" : "창동", "brchNo": "1321"},{"brchNm" : "코엑스", "brchNo": "1351"},{"brchNm" : "홍대", "brchNo": "1212"},{"brchNm" : "화곡", "brchNo": "1571"},{"brchNm" : "ARTNINE", "brchNo": "1562"}


# In[91]:


for theater in theaters :
    print(theater["brchNm"]+", "+theater["brchNo"])


# In[92]:


def insert_theaters_all(obj) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    try :
        with conn.cursor() as curs :
            for theater in obj :
                sql = 'insert into theaters (THEATERS, THEATERS_SEQ, TH_NAME) values ("MEGABOX",%s,%s)'
                curs.execute(sql,("M-"+theater["brchNo"],theater["brchNm"]))
            conn.commit()
            print("입력 성공!")
    finally :
        conn.close()


# In[93]:


insert_theaters_all(theaters)


# In[40]:


def select_movie_bySubject(subject) :
    SEQ = 0
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
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


# In[41]:


def get_movie_seq() :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    try :
        with conn.cursor() as curs :
            sql = "select MOVIE_SEQ from MOVIE ORDER BY MOVIE_SEQ DESC"
            curs.execute(sql)
            rs = curs.fetchall()
            SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


# In[42]:


def insert_moviePlay(MOVIE_SEQ, THEATERS_SEQ, START_TIME, RUNNING_TIME, SEATS, SEATS_LEFT) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    try :
        with conn.cursor() as curs :
            sql = "insert into MOVIE_PLAY (MOVIE_SEQ, THEATERS_SEQ, START_TIME, RUNNING_TIME, SEATS, SEATS_LEFT) values (%s,%s,%s,%s,"+SEATS+","+SEATS_LEFT+")"
            curs.execute(sql,(MOVIE_SEQ, THEATERS_SEQ, START_TIME, RUNNING_TIME))
        conn.commit()
        print("입력 성공!")
    finally :
        conn.close()  


# In[57]:


def insert_movie(SEQ, COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    try :
        with conn.cursor() as curs :
            sql = "insert into MOVIE (MOVIE_SEQ, COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE) values ("+SEQ+",%s,%s,%s,%s,%s,%s)"
            curs.execute(sql,(COUNTRY, SUBJECT, GENRE, DIRECTOR, SUMMARY, GRADE))
        conn.commit()
        print("입력 성공!")
    finally :
        conn.close()


# In[56]:


#theatercode = "1372"
#def insert_MEGABOX_Movie_play(theatercode) :
url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
parameters = {
            "masterType":"brch",
            "detailType":"area",
            "brchNo":theatercode,
            "firstAt":"N",
            "brchNo1":theatercode,
            "crtDe":"20200527",
            "playDe":"20200527"
}
response = requests.post(url,data=parameters).json()
movie_response2 = response['megaMap']['movieFormList']
timetables= split_movies_by_no(movie_response2)
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


# In[62]:


def select_theaters_seq(THEATERS) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
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


# In[97]:


ts = select_theaters_seq("MEGABOX")
for theatercode in ts :
    url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
    parameters = {
                "masterType":"brch",
                "detailType":"area",
                "brchNo":theatercode[0].replace("M-",""),
                "firstAt":"N",
                "brchNo1":theatercode[0].replace("M-",""),
                "crtDe":"20200527",
                "playDe":"20200527"
    }
    response = requests.post(url,data=parameters).json()
    movie_response2 = response['megaMap']['movieFormList']
    timetables= split_movies_by_no(movie_response2)
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


# In[68]:


#영화 번호로 영화이름 가져오기
def get_movieSubject_by_seq(movie_seq) :
    SEQ = 0
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
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


# In[102]:


#극장 이름으로 극장번호 가져오기
def get_seq_by_theaterName(theaters, thName) :
    SEQ = 0
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
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


# In[88]:


#극장번호와 영화번호로 상영시간표 가져오기
def get_movie_play_by_s_t(subjectSeq, theaterSeq) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    tuples = []
    try :
        with conn.cursor() as curs :
            sql = 'select START_TIME, SEATS_LEFT from MOVIE_PLAY WHERE movie_seq = %s AND theaters_seq = %s AND date_format(REGIST_DATE,"%%Y-%%m-%%d") = CURDATE()'
            curs.execute(sql,(subjectSeq,theaterSeq))
            rs = curs.fetchall()
            return rs
    finally :
        conn.close()


# In[106]:


#선택한 영화가 상영중인 영화관을 알고싶다
def get_movie_play_t_by_s(subject) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    movieSeq = select_movie_bySubject(subject)
    try :
        with conn.cursor() as curs :
            sql = "select DISTINCT(THEATERS_SEQ) from MOVIE_PLAY WHERE movie_seq = %s"
            curs.execute(sql,(movieSeq))
            rs = curs.fetchall()
            for r in rs :
                print(get_theaterName_by_seq(r[0]))
    finally :
        conn.close()


# In[108]:


#극장 번호로 극장이름 가져오기
def get_theaterName_by_seq(th_seq) :
    name = []
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
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


# In[111]:


get_movie_play_t_by_s("그집")


# In[98]:


#선택한 영화관에서 상영중인 영화를 알고싶다
def get_movie_play_s_by_t(theaters, theaterName) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    try :
        with conn.cursor() as curs :
            sql = "select distinct(MOVIE_SEQ) from MOVIE_PLAY WHERE THEATERS_SEQ = %s"
            curs.execute(sql,(theaterSeq))
            rs = curs.fetchall()
            return rs
           # for r in rs :
           #     print(get_movieSubject_by_seq(r[0]))
    finally :
        conn.close()        


# In[103]:


#선택한 영화관에서 상영중인 영화를 알고싶은데 시간표도 같이 가져와주라
def get_movie_play_s_timetable_by_t(theaters, theaterName) :
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    subjectsSeq = get_movie_play_s_by_t(theaters, theaterName) #상영중인 영화
    print(theaters, theaterName)
    for subject in subjectsSeq :
        #print(subject[0], theaterSeq)
        timetable = get_movie_play_by_s_t(subject[0], theaterSeq)
        print(get_movieSubject_by_seq(subject[0]), timetable)


# In[104]:


get_movie_play_s_timetable_by_t("MEGABOX","동대문")

