# -*- coding:utf-8 -*-
import requests
import csv
import re
import matplotlib.pyplot as plt  # 暂未使用的库
import lxml.etree
import numpy as np


# 爬取数据
def getData(url, xpathList):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.109 Safari/537.36'}
    try:
        # 发送HTTP GET请求
        response = requests.get(url, headers=headers)
        # 解析HTML内容
        response = lxml.etree.HTML(response.text)
    except:
        # 请求失败处理
        print('打开网址失败！！！请检查！')
        return

    dataList = []
    for i in range(len(xpathList)):
        # 根据XPath提取数据
        data = response.xpath(xpathList[i])
        if len(data) == 0:
            # 数据为空时的提示
            print(f"爬取数据为空！请检查xpath路径xpathList[{i}]!")
        dataList.append(data)
    # 返回数据列表
    return dataList


# 数据写入csv文件
def dataWriteToCsv(filename, data, headers=None, isHeaders=False):
    if headers is None:
        headers = []
    try:
        # 打开CSV文件，以追加模式写入
        with open(filename, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            # 是否写入标题头
            if isHeaders:
                writer.writerow(headers)
            # 写入数据
            for i in range(len(data)):
                writer.writerow(data[i])
        print(f'数据写入成功{filename}中！')
    except:
        # 写入文件失败处理
        print('写入文件失败！！！')


# 爬取食物种类类别
def getFoodKind():
    url3 = f'http://db.foodmate.net/yingyang/type_1.html'
    xpathList3 = ['//*[@id="top"]/a']
    dataElem3 = getData(url3, xpathList3)
    # 手动添加的一些食物种类
    kindfood_temp = ['鱼类', '婴儿食品类', '小吃类']
    kindFood = []
    i = 0
    sign = 0
    signList = [11, 12, 13]
    while i < len(dataElem3[0]):
        if sign in signList:
            # 添加手动指定的食物种类
            kindFood.append(kindfood_temp[sign - 11])
            sign += 1
        else:
            # 添加爬取到的食物种类
            kindFood.append(dataElem3[0][i].text)
            i += 1
            sign += 1
    return kindFood


# 爬取表头
def getCsvHeaders():
    headers = ['食物', '别名', '特征', '分类', 'Wiki百科']
    ur = 'http://db.foodmate.net/yingyang/type_0%3A1%3A0_1.html'
    xp = ['//*[@id="rightlist"]/div[@class="list"]//text()']
    da = getData(ur, xp)
    for i in range(len(da[0]) // 2):
        headers.append(da[0][2 * i])
    headers.append('备注')
    return headers


# 读取食物营养库一类食物数据并保存到csv文件中
def getFoodDataToCsv(foodKindId, foodKind, headers):
    # 食物名称及详细页面
    url0 = f'http://db.foodmate.net/yingyang/type_{foodKindId}.html'
    xpathList1 = ['/html/body/div[@id="main2"]/div/div[@id="leftcontent"]/div[@id="dibu"]/li[@class="lie"]/a']
    dataElem = getData(url0, xpathList1)
    
    # 正则表达式匹配
    pattan1 = re.compile('\[.*?\]')
    pattan2 = re.compile('\(.*?\)')
    dataList = []
    for i in range(len(dataElem[0])):
        string_temp = dataElem[0][i].text
        # 提取名称中‘【】’的别名
        other_name = pattan1.search(string_temp)
        # 提取名称中‘（）’的特性
        features = pattan2.search(string_temp)
        if other_name is None:
            other_name = 'Empty'
        else:
            other_name = other_name.group()
            other_name = other_name.replace('[', '')
            other_name = other_name.replace(']', '')
        if features is None:
            features = 'Empty'
        else:
            features = features.group()
            features = features.replace('(', '')
            features = features.replace(')', '')
        # 将名称中的别名与特征去除
        f_Name = pattan1.sub('', string_temp)
        f_Name = pattan2.sub('', f_Name)
        # 写入data列表
        data = [f_Name, other_name, features, foodKind[foodKindId - 1]]
        # 一种食物的数据页面
        url1 = 'http://db.foodmate.net/yingyang/' + dataElem[0][i].attrib['href']
        xpathList2 = ['//*[@id="rightlist"]/div[@class="list"]//text()', '//*[@id="rightlist"]/center/a']
        data2Elem = getData(url1, xpathList2)
        try:
            # 获取Wiki链接
            data.append(data2Elem[1][0].attrib['href'])
        except:
            data.append('Empty')
        for j in range(len(headers) - 6):
            try:
                data.append(float(data2Elem[0][2 * j + 1]))
            # 数据为空设置为nan
            except:
                data.append(np.nan)
        data.append('Empty')
        dataList.append(data)
    # 写入CSV文件
    dataWriteToCsv('Data\\food.csv', dataList, headers=headers, isHeaders=(foodKindId == 1))


# 主函数
if __name__ == '__main__':
    # 爬取食物种类
    fK = getFoodKind()
    # 爬取表头
    header = getCsvHeaders()
    # 爬取食物数据
    for num in range(20):
        getFoodDataToCsv(num + 1, fK, header)
