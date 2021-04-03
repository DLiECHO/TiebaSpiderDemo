# 导入需要的包
import time
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re
import random

# get请求模版
url = "https://tieba.baidu.com/f?kw=hpv&ie=utf-8&pn={}"

# 爬取n页的数据
def search_n_pages(n):
    '''爬取n页数据'''
    target = []

    # 发起n次的get请求
    for i in range(n):
        # 跟踪进度
        print('page:', i)

        # 按照浏览贴吧的自然行为，每一页50条
        target_url = url.format(50*i)
        print("当前地址：" + target_url)
        res = requests.get(target_url)

        filename = "document.txt"
        with open(filename, "w", encoding='utf-8')as f:
            f.write(res.text)
        with open(filename, "r", encoding='utf-8')as f:
            cstr = f.read()
            #print(str)
            num = 0
            #帖子地址记录
            x = 0
            while cstr.find("href=\"/p/") != -1:
                num = cstr.find("href=\"/p/")
                target.append(cstr[num+9:num+19])
                #print(cstr[num+9:num+19])
                cstr = cstr[num+19 : len(cstr)-1]
                #print(i,x)
                x = x + 1
            if i%20 == 0:
                # 转化为pandas.DataFrame对象
                pdata = pd.DataFrame(target)
                # 导出到excel表格
                pdata.to_csv('a0temp.csv', index=False)
        time.sleep(random.randint(2,5))

    return target

#爬取贴吧前270页数据
data1 = search_n_pages(10)
#print(data1)

# 转化为pandas.DataFrame对象
pdata = pd.DataFrame(data1)

# 导出到excel表格
pdata.to_csv('a0.csv', index=False)


#获取帖子内容
def search_one_pages(code):
    '''抓取'''
    target = []
    # 第一页
    target_url = "https://tieba.baidu.com/p/"+ str(code) + "?pn=1"
    res = requests.get(target_url)
    # filename = "document1.txt"
    # with open(filename, "w", encoding='utf-8')as f:
    #     f.write(res.text)
    # with open(filename, "r", encoding='utf-8')as f:
    #     cstr = f.read()
    cstr = res.text
    while cstr.find("d_post_content j_d_post_content") != -1:
        print("qqq")
        num = cstr.find("d_post_content j_d_post_content")
        p1 = re.compile(r"[>](.*?)[<]", re.S)
        tstr = cstr[num+30:num+200]
        target.append(re.findall(p1,tstr))
            #print(cstr[num+9:num+19])
        cstr = cstr[num+200 : len(cstr)-1]
            #print(i,x)
    return target

data2 = []
acc = 1
for code in data1:
    ans = search_one_pages(code)
    for i in ans:
        data2.append(i)
    #print(acc)
    acc = acc + 1
    if acc%10 == 0:
        pdata = pd.DataFrame(data2)
        # 导出到csv
        pdata.to_csv('answerTemp.csv', index=False)
    #print(data2)
# 转化为pandas.DataFrame对象
pdata = pd.DataFrame(data2)

# 导出到csv
pdata.to_csv('answer.csv', index=False)