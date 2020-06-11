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


# In[175]:


def dbConnection() :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    #conn.query("set character_set_connection=utf8;")
    #conn.query("set character_set_server=utf8;")
    #conn.query("set character_set_client=utf8;")
    #conn.query("set character_set_results=utf8;")
    #conn.query("set character_set_database=utf8;")
    return conn


# In[3]:


req = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0056&date=20200528')
html = req.text
soup = BeautifulSoup(html, 'html.parser')


# In[4]:


movies = soup.select('body > div > div.sect-showtimes > ul > li')


# In[5]:


for movie in movies :
    title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
    print(title)


# In[6]:


def get_timetable(moive):
    tuples = []
    timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
    for timetable in timetables:
        time = timetable.select_one('em').get_text()        
        seat = timetable.select_one('span').get_text()
        tuple = (time,seat)
        tuples.append(tuple)
    return tuples


# In[7]:


for movie in movies :
    title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
    timetable = get_timetable(movie)
    print(title, timetable, '\n')


# 극장 코드를 가져와야함 -> 스크립트로 되어있어서 그냥 JSON데이터 긁어와서 박도록함
# url : http://www.cgv.co.kr/reserve/show-times/
# selector : #contents > div.sect-common > div > div.sect-city > ul > li.on > div > ul > li.on
# 
# <CGV>
# 영화관 정보는 CGV는 일단 JSON 긁어와서 다 담고
# 상영정보는 TheaterCode를 이용해서 모두 긁어올 수 있다.
# 영화 정보는 어떻게하지????
# 
# 영화가 주 키가 되어야 한다.
# 상영키에 넣을 때 극장키랑 영화키랑 동시에 돌려서 맞으면 넣어야하나???
# 
# 상영관을 가져옵니다. -> 영화 이름을 가져옵니다. -> 영화가 있으면 시퀀스번호를 가져오고 없으면 새로 등록합니다.
# -- 시퀀스번호와 상영관 모두 구할수 있습니다. 상영정보 넣으면서 조지면 됩니다.
# 키는 이름으로 할 수 밖에 없을듯....

# In[17]:


#서울
theaters = {"RegionCode":"01","TheaterCode":"0056","TheaterName":"강남","TheaterName_ENG":"","IsSelected":"true"},{"RegionCode":"01","TheaterCode":"0001","TheaterName":"강변","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0229","TheaterName":"건대입구","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0010","TheaterName":"구로","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0063","TheaterName":"대학로","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0252","TheaterName":"동대문","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0230","TheaterName":"등촌","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0009","TheaterName":"명동","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0105","TheaterName":"명동역 씨네라이브러리","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0011","TheaterName":"목동","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0057","TheaterName":"미아","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0030","TheaterName":"불광","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0046","TheaterName":"상봉","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0300","TheaterName":"성신여대입구","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0088","TheaterName":"송파","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0276","TheaterName":"수유","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0150","TheaterName":"신촌아트레온","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0040","TheaterName":"압구정","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0112","TheaterName":"여의도","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0059","TheaterName":"영등포","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0074","TheaterName":"왕십리","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0013","TheaterName":"용산아이파크몰","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0131","TheaterName":"중계","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0199","TheaterName":"천호","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0107","TheaterName":"청담씨네시티","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0223","TheaterName":"피카디리1958","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0164","TheaterName":"하계","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0191","TheaterName":"홍대","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"P001","TheaterName":"CINE de CHEF 압구정","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"P013","TheaterName":"CINE de CHEF 용산아이파크몰","TheaterName_ENG":"","IsSelected":"false"}


# In[18]:


for theater in theaters :
    print(theater["TheaterName"]+", "+theater["TheaterCode"])


# 파이썬, mysql 연동 :: https://myjamong.tistory.com/53

# In[75]:


def select_theaters_all() :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            sql = "select * from theaters"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs :
                print(row)
    finally :
        conn.close()


# In[99]:


select_theaters_all()


# In[77]:


def insert_theaters_all(obj) :
    conn = dbConnection()
    try :
        with conn.cursor() as curs :
            for theater in obj :
                sql = 'insert into theaters (THEATERS, THEATERS_SEQ, TH_NAME) values ("CGV",%s,%s)'
                curs.execute(sql,("C-"+theater["TheaterCode"],theater["TheaterName"]))
            conn.commit()
            print("입력 성공!")
    finally :
        conn.close()


# In[73]:


insert_theaters_all(theaters)


# DB연결 -- conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
# 
# 순서
# - 극장 번호를 가져옵니다.
# - 극장별로 오늘날짜를 크롤링 합니다.
# - 그 극장의 영화별 상영시간을 집어넣습니다.
#     - 영화 이름 가져오기
#     - 현재 SEQ위 최고값을 가져와 1 더한값을 저장하고있는다.
#     - 영화 이름이 영화테이블에 있는지 확인 있으면 시퀀스번호를 가져온다.
#     - 영화테이블에 없다면 상위최고값으로 영화랑 상영정보를 동시에 넣는다.

# In[101]:


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


# In[87]:


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


# In[100]:


get_movie_seq()


# In[89]:


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


# In[170]:


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


# ################################################################################### 상영시간 넣기

# def get_timetable(moive):
#     tuples = []
#     timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
#     for timetable in timetables:
#         time = timetable.select_one('a > em').get_text()
#         seat = timetable.select_one('a > span').get_text()
#         tuple = (time,seat)
#         tuples.append(tuple)
#     return tuples

# In[91]:


#insert_CGV_Movie_play("0229")


# In[83]:


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


# In[138]:


#test = select_theaters_seq_all()
#for t in test :
#    insert_CGV_Movie_play(str(t[0]))


# In[84]:


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


# In[146]:


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


# In[167]:


#findPlaySeq("12","C-0010","16:30")


# In[172]:


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


# In[169]:


#seatsUpdate("2143","1000")


# In[183]:


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


# 이제 필요한것은 무엇인가...?
# - 영화관별 영화 상영목록 가져오기 : 영화관코드를 넣으면 그 영화관에서 상영중인 영화를 가져온다.
# - 영화별 상영관 목록 가져오기 : 영화코드를 넣으면 영화가 상영중인 영화관을 가져온다.
# -- 영화이름을 넣거나 영화관이름을 넣으면 나올 수 있도록 하면 더 좋을것같음....

# In[90]:


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


# In[112]:


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


# In[92]:


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


# In[185]:


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


# In[189]:


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


# In[190]:


test = get_movie_play_t_by_s('기생충')


# In[187]:


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


# In[183]:


get_movie_play_s_by_t('CGV','강남')


# In[114]:


#선택한 영화관에서 상영중인 영화를 알고싶은데 시간표도 같이 가져와주라
def get_movie_play_s_timetable_by_t(theaters, theaterName) :
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    subjectsSeq = get_movie_play_s_by_t(theaters, theaterName) #상영중인 영화
    print(theaters, theaterName)
    for subject in subjectsSeq :
        #print(subject[0], theaterSeq)
        timetable = get_movie_play_by_s_t(subject[0], theaterSeq)
        print(get_movieSubject_by_seq(subject[0]), timetable)


# In[188]:


get_movie_play_s_timetable_by_t('CGV','목동')


# In[ ]:




