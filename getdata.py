# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 大量复用代码分割出来的请求网页函数


def getdata(url, tag):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/72.0.3626.109 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    a = soup.find("div", id=str(tag))
    b = a.find_all("a")
    return b


def getfoodname(num):
    url = f"http://db.foodmate.net/yingyang/type_{num}.html"
    temp = getdata(url=url, tag="dibu")
    foodnamelist = []
    for c in temp:
        foodnamelist.append(c.string)
    return foodnamelist


def getfoodkind(num):
    url = f"http://db.foodmate.net/yingyang/type_{num}.html"
    b = getdata(url=url, tag="top")
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
    return kindfood

# 从主页面到具体数据页面的函数


def geturl(num):
    url = f"http://db.foodmate.net/yingyang/type_{num}.html"
    temp = getdata(url=url, tag="dibu")
    urllist = []
    for c in temp:
        urllist.append(c.get("href"))
    return urllist

# 获取数据页面数据


def getdatanumber(num):
    urllist = geturl(num=num)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/72.0.3626.109 Safari/537.36'}
    numbers = []
    for url in urllist:
        baseurl = "http://db.foodmate.net/yingyang/"
        url = baseurl+url
        response = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        a = soup.find_all("div", class_="list")
        templist = []
        for b in a:
            c = b.find("div", class_="list_m")
            number = b.text.replace(c.text, '').strip()
            templist.append(number)
        numbers.append(templist)
    return numbers
    # 嵌套列表

# 获取表头也就是第一行


def getheaders():
    head = []
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/72.0.3626.109 Safari/537.36'}
    url = "http://db.foodmate.net/yingyang/type_0%3A1%3A0_1.html"
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    a = soup.find_all("div", class_="list")
    for b in a:
        c = b.find("div", class_="list_m")
        head.append(c.string)
    return head

# 合成dataframe
def adddf(foodkindid, foodkind, foodname, datanumber, head):
    global df
    temp = pd.DataFrame(columns=head)
    temp['名字'] = foodname
    temp['分类'] = foodkind[foodkindid-1]
    for i, data in enumerate(datanumber):
        if i < len(temp):
            for j, value in enumerate(data):
                temp.iloc[i, j + 2] = value
    df = pd.concat([df, temp], ignore_index=True)


head = getheaders()
head.insert(0, '分类')
head.insert(0, '名字')
df = pd.DataFrame(columns=head)
for i in range(21):
    foodkind = getfoodkind(i+1)
    foodname = getfoodname(i+1)
    datanumber = getdatanumber(i+1)
    adddf(i+1, foodkind, foodname, datanumber, head)
df.to_csv("d:\\github_code\\Reptiles\\result.csv",
          encoding="utf_8_sig", index=False)
