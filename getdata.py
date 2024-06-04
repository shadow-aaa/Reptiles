# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/72.0.3626.109 Safari/537.36'}
url="http://db.foodmate.net/yingyang/type_1.html"
response=requests.get(url=url)
soup=BeautifulSoup(response.text,"html.parser")
a=soup.find("div",id="dibu")
for b in a:
    b=a.find("a")
    print(b.get("href"))
