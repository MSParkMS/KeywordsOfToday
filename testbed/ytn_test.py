# -*- encoding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
import io
#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

#sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'ANSI')
#sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'ANSI')

source = requests.get("https://www.ytn.co.kr/").text
#source = requests.get("https://www.chosun.com/").text

soup = BeautifulSoup(source, "html.parser")

hotKeys = soup.select("dd.arti_text a")
#hotKeys = soup.select("dl.news_item")


index = 0
for key in hotKeys :
	index += 1
	print(str(index) + ", "+key.text)
	print("https://www.ytn.co.kr"+key.get('href'))