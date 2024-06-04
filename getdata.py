# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/72.0.3626.109 Safari/537.36'}
url="http://db.foodmate.net/yingyang/type_1.html"
def getfoodname():
    global datalist
    response=requests.get(url=url)
    soup=BeautifulSoup(response.text,"html.parser")
    a=soup.find("div",id="dibu")
    b=a.find_all("a")
    datalist=[]
    for c in b:
        datalist.append(c.string)

def geturl():
    response=requests.get(url=url)
    soup=BeautifulSoup(response.text,"html.parser")
    a=soup.find("div",id="dibu")
    b=a.find_all("a")
    for c in b:
        print(c.get("href"))
# geturl()
datalist=[]
getfoodname()
mydict={}
data=["this is a test"]
df = pd.read_csv("test.csv")
df.info()
