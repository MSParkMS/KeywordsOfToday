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


# In[10]:


req = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0056&date=20200528')
html = req.text
soup = BeautifulSoup(html, 'html.parser')


# In[11]:


movies = soup.select('body > div > div.sect-showtimes > ul > li')


# In[12]:


for movie in movies :
    title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
    print(title)


# In[13]:


def get_timetable(moive):
    tuples = []
    timetables = movie.select('div > div.type-hall > div.info-timetable > ul > li')
    for timetable in timetables:
        time = timetable.select_one('em').get_text()        
        seat = timetable.select_one('span').get_text()
        tuple = (time,seat)
        tuples.append(tuple)
    return tuples


# In[14]:


for movie in movies :
    title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
    timetable = get_timetable(movie)
    print(title, timetable, '\n')

극장 코드를 가져와야함 -> 스크립트로 되어있어서 그냥 JSON데이터 긁어와서 박도록함
url : http://www.cgv.co.kr/reserve/show-times/
selector : #contents > div.sect-common > div > div.sect-city > ul > li.on > div > ul > li.on

<CGV>
영화관 정보는 CGV는 일단 JSON 긁어와서 다 담고
상영정보는 TheaterCode를 이용해서 모두 긁어올 수 있다.
영화 정보는 어떻게하지????

영화가 주 키가 되어야 한다.
상영키에 넣을 때 극장키랑 영화키랑 동시에 돌려서 맞으면 넣어야하나???

상영관을 가져옵니다. -> 영화 이름을 가져옵니다. -> 영화가 있으면 시퀀스번호를 가져오고 없으면 새로 등록합니다.
-- 시퀀스번호와 상영관 모두 구할수 있습니다. 상영정보 넣으면서 조지면 됩니다.
키는 이름으로 할 수 밖에 없을듯....
# In[124]:


#서울
#theaters = {"RegionCode":"01","TheaterCode":"0056","TheaterName":"강남","TheaterName_ENG":"","IsSelected":"true"},{"RegionCode":"01","TheaterCode":"0001","TheaterName":"강변","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0229","TheaterName":"건대입구","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0010","TheaterName":"구로","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0063","TheaterName":"대학로","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0252","TheaterName":"동대문","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0230","TheaterName":"등촌","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0009","TheaterName":"명동","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0105","TheaterName":"명동역 씨네라이브러리","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0011","TheaterName":"목동","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0057","TheaterName":"미아","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0030","TheaterName":"불광","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0046","TheaterName":"상봉","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0300","TheaterName":"성신여대입구","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0088","TheaterName":"송파","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0276","TheaterName":"수유","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0150","TheaterName":"신촌아트레온","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0040","TheaterName":"압구정","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0112","TheaterName":"여의도","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0059","TheaterName":"영등포","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0074","TheaterName":"왕십리","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0013","TheaterName":"용산아이파크몰","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0131","TheaterName":"중계","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0199","TheaterName":"천호","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0107","TheaterName":"청담씨네시티","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0223","TheaterName":"피카디리1958","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0164","TheaterName":"하계","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"0191","TheaterName":"홍대","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"P001","TheaterName":"CINE de CHEF 압구정","TheaterName_ENG":"","IsSelected":"false"},{"RegionCode":"01","TheaterCode":"P013","TheaterName":"CINE de CHEF 용산아이파크몰","TheaterName_ENG":"","IsSelected":"false"}


# In[15]:


for theater in theaters :
    print(theater["TheaterName"]+", "+theater["TheaterCode"])


# 파이썬, mysql 연동 :: https://myjamong.tistory.com/53

# In[8]:


#req2 = requests.get('http://www.cgv.co.kr/reserve/show-times/')
#html2 = req2.text
#print(html2)
#soup2 = BeautifulSoup(html2, 'html.parser')
#print(soup2)
#theaters = soup2.select('#contents > div.sect-common > div > div.sect-city > ul > li.on > div > ul > li')


# In[9]:


#for theater in theaters :
#    th_name = theater.select_one('a').get_text()
#    print(th_name, '\n')


# In[147]:


def select_theaters_all() :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    try :
        with conn.cursor() as curs :
            sql = "select * from theaters"
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs :
                print(row)
    finally :
        conn.close()


# In[148]:


select_theaters_all()


# In[126]:


def insert_theaters_all(obj) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    try :
        with conn.cursor() as curs :
            for theater in obj :
                sql = 'insert into theaters (THEATERS, THEATERS_SEQ, TH_NAME) values ("CGV",%s,%s)'
                curs.execute(sql,("C-"+theater["TheaterCode"],theater["TheaterName"]))
            conn.commit()
            print("입력 성공!")
    finally :
        conn.close()


# In[127]:


#insert_theaters_all(theaters)


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

# In[149]:


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


# In[70]:


#insert_movie("2","test","test","test","test","test","test")


# In[162]:


def get_movie_seq() :
    SEQ=0
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    try :
        with conn.cursor() as curs :
            sql = "select MOVIE_SEQ from MOVIE ORDER BY MOVIE_SEQ DESC"
            curs.execute(sql)
            rs = curs.fetchall()
            if rs == 0 :
                SEQ = 0
            else :
                SEQ = rs[0][0]
    finally :
        conn.close()
        return SEQ


# In[163]:


#get_movie_seq()


# In[157]:


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


# In[158]:


#select_movie_bySubject("TEST")


# In[135]:


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

# In[136]:


#theatercode = "0056"
#def insert_CGV_Movie_play(theatercode) :
#    req3 = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode='+theatercode+'&date=20200528')
#    html3 = req3.text
#    soup3 = BeautifulSoup(html3, 'html.parser')
#    movies3 = soup3.select('body > div > div.sect-showtimes > ul > li')
#    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
#    for movie in movies3 :
#        title = movie.select_one('div > div.info-movie > a > strong').get_text().strip()
#        timetable = get_timetable(movie)
#        print(title, timetable, '\n')
#        movie_seq = select_movie_bySubject(title)
#        add_seq = get_movie_seq() + 1
#        print(movie_seq)
#        if movie_seq == 0 :
#            insert_movie(str(add_seq), "", title, "", "", "", "")
#            for time in timetable :
#                insert_moviePlay(str(add_seq), theatercode, time[0], "", "100", time[1].replace("잔여좌석","").replace("석","").replace("마감","0"))
#        else :
#            for time in timetable :
#                insert_moviePlay(str(movie_seq), theatercode, time[0], "", "100", time[1].replace("잔여좌석","").replace("석","").replace("마감","0"))


# In[91]:


#insert_CGV_Movie_play("0229")


# In[137]:


def select_theaters_seq_all() :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
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


# In[165]:


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


# In[173]:


ts = select_theaters_seq("CGV")
for theatercode in ts :
    req3 = requests.get('http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode='+theatercode[0].replace("C-","")+'&date=20200529')
    html3 = req3.text
    soup3 = BeautifulSoup(html3, 'html.parser')
    movies3 = soup3.select('body > div > div.sect-showtimes > ul > li')
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
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

# In[196]:


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


# In[51]:


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


# In[180]:


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


# In[89]:


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


# In[90]:


#get_movie_play_by_s_t("3","0001")


# In[200]:


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


# In[199]:


#test = get_movie_play_t_by_s('기생충')


# In[182]:


#선택한 영화관에서 상영중인 영화를 알고싶다
def get_movie_play_s_by_t(theaters, theaterName) :
    conn = pymysql.connect(host='localhost',user='root',password='ha223740',db='todays_movie', charset='utf8')
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    try :
        with conn.cursor() as curs :
            sql = "select distinct(MOVIE_SEQ) from MOVIE_PLAY WHERE THEATERS_SEQ = %s"
            curs.execute(sql,(theaterSeq))
            rs = curs.fetchall()
           # for r in rs :
           #     print(get_movieSubject_by_seq(r[0]))
    finally :
        conn.close()
        return rs


# In[183]:


#get_movie_play_s_by_t('CGV','강남')


# In[191]:


#선택한 영화관에서 상영중인 영화를 알고싶은데 시간표도 같이 가져와주라
def get_movie_play_s_timetable_by_t(theaters, theaterName) :
    theaterSeq = get_seq_by_theaterName(theaters, theaterName)
    subjectsSeq = get_movie_play_s_by_t(theaters, theaterName) #상영중인 영화
    print(theaters, theaterName)
    for subject in subjectsSeq :
        #print(subject[0], theaterSeq)
        timetable = get_movie_play_by_s_t(subject[0], theaterSeq)
        print(get_movieSubject_by_seq(subject[0]), timetable)


# In[198]:


get_movie_play_s_timetable_by_t('CGV','목동')

