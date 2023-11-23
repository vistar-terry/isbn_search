#-*- coding:utf-8 -*-

"""
    Author：万俟淋曦
    Time：2019年10月13日11:00:28
    Function：通过isbn查询书籍详细信息
    Statement：仅供学习，勿作商用，如有违反，后果自负
    P.S.：如有问题可以联系我，qq1055311345，好友验证：isbn
"""

import re
import sys
import urllib
import requests
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions


def isbn_search(isbn):
    """
        输入：isbn
        输出：豆瓣搜索结果的书籍链接
    """
    # 创建浏览器对象
    browser = webdriver.PhantomJS(executable_path=".\webdriver\phantomjs.exe")  # windows
    # browser = webdriver.PhantomJS(executable_path="./webdriver/phantomjs_linux")  # linux
    # option = ChromeOptions()
    # option.add_argument("--headless")  # 指定无头模式
    # browser = webdriver.Chrome(executable_path="..\webdriver\chromedriver.exe", options=option)
    # 请求网址
    browser.get("https://book.douban.com/subject_search?search_text=" + isbn + "&cat=1001")
    # 解析网页信息
    soup = BeautifulSoup(browser.page_source, "lxml")
    # 读取标签内容
    tags = soup.select("#root > div > div > div > div > div > div > a")
    # print(type(tags))
    # print(browser.page_source)
    # 正则查找href链接
    link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", str(tags[0]))
    # 关闭浏览器
    browser.close()
    return link_list[0]

def get_rating(soup):
    """
    豆瓣评分及评价人数
    """
    rating = soup.find('div', {'class': 'rating_self clearfix'})
    rating_num = rating.find('strong').string.strip()
    if 0 == len(rating_num):
        rating_num = "-"
        rating_people = "评价人数不足"
    else:
        rating_people = rating.find('span', property="v:votes").string.strip()

    return rating_num, rating_people

def book_info(douban_link):
    """
        输入：豆瓣书籍链接
        输出：书籍信息
    """
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    # 请求网址
    g=requests.get(douban_link,headers=headers)
    # 解析网页信息
    soup=BeautifulSoup(g.content,"lxml")
    # 由于书名和其他信息不在一起，单独处理书名
    title = "书名: 《" + re.sub('[\f\n\r\t\v]','',re.sub('<([^>]+?)>','',str((soup.select("#wrapper > h1 > span"))[0]))) + "》"
    # 存储书籍信息
    infos = [title]
    # 返回特定区域的html代码块
    span_list = soup.findChild('div',{'id':'info'})
    # try:
    for item in str(span_list).split('<br/>'): # 将信息按项目分割,每个item是一个信息项
        # 用两次正则，一次去掉多余html代码，一次去掉制表换行空格等字符
        # .split(":")以：分割每个信息项目
        info_item = re.sub('[\f\n\r\t\v\s]','',re.sub('<([^>]+?)>','',item)).split(":")
        info_temp = [] # 存放以“/”分隔的item
        for info_item_item in info_item:
            sprit = info_item_item.partition("/") # 以“/”分隔info_item_item
            for sprit_item in sprit:
                info_temp += sprit_item.partition("]") # 以“/”分隔sprit_item, 并将处理后的列表合并

        # info_temp 存储单项信息的列表
        # temp_list 存储去空格处理后的单项信息
        temp_list = []
        for temp in info_temp:
            # 过滤掉空字符串
            if temp != '':
                temp_list.append(temp)
            else:
                continue
            # 在书籍属性后加“：”
            info = temp_list[0] + ': '
            for i in range(1, len(temp_list)):
                info += temp_list[i] # 拼接每个信息项目

        # 判断temp_list是否为空，为空则info为错误值，不存入infos
        if temp_list:
            pass
        else:
            continue 
        # print(info) 
        infos.append(info)

    rating = get_rating(soup)
    infos.append("豆瓣评分："+rating[0])
    infos.append("评价人数："+rating[1])
    return infos


def main():
    if len(sys.argv) == 1:
        print("请输入isbn码。\n例如：python book.py 9787121369421")
    elif len(sys.argv) == 2:
        douban_link = isbn_search(sys.argv[1])
        # print(douban_link)
        infos = book_info(douban_link)
        for info in infos:
            print(info)
    else:
        print("只接收一个isbn码。")


if __name__ == "__main__":
    main()




# 9787543632608  a标签不在span里，直接在div  author = "作者：" + f.xpath('//*[@id="info"]/a/text()')[0] + "\n"
# 9787115428028  a标签在span里，但有a标签不在span里，直接在div的其他项混淆  author = "作者：" + f.xpath('//*[@id="info"]/span[1]/a/text()')[0] + "\n"
# 9787564177560
# 9787030560896  
# 9787030189554
# 9787115130228  有/,且/两侧存在空格
# 9787510044823
# 9787510046834

