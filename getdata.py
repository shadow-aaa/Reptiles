# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/72.0.3626.109 Safari/537.36'}
url = "http://db.foodmate.net/yingyang/type_1.html"


def getfoodname():
    datalist = []
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    a = soup.find("div", id="dibu")
    b = a.find_all("a")
    for c in b:
        datalist.append(c.string)


def geturl():
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    a = soup.find("div", id="dibu")
    b = a.find_all("a")
    urllist = []
    for c in b:
        urllist.append(c.get("href"))
    return urllist


def getfoodkind():
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    a = soup.find("div", id="top")
    b = a.find_all('a')
    kindfood_miss = ['鱼类', '婴儿食品类', '小吃类']
    kindfood = []
    temp = 0  # 用以加入列表中缺失的数据
    for c in b:
        if temp == 11:
            for i in range(3):
                kindfood.append(kindfood_miss[temp-11])
                temp += 1
            kindfood.append(c.string)
        else:
            kindfood.append(c.string)
            temp += 1
    print(kindfood)


getfoodkind()
# geturl()
# getfoodname()
# df = pd.DataFrame()
# df['wtf']=datalist
# df.to_csv("d:\\github_code\\Reptiles\\test.csv",encoding="utf_8_sig",index=False)
