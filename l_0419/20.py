import bs4      #网页解析，获取数据
import re       #正则表达式，进行文字匹配
import urllib.request,urllib.error #指定URL，获取网页数据
import xlwt     #进行excel操作
import sqlite3  #进行SQLite数据库操作


def maim():
    baseurl = "https://movie.douban.com/top250?start="
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"

#爬取网页
def getData(baseurl):
    datalist = []
     #2.逐一解析数据
    return datalist

#3.保存数据
def saveData(savepath):
    print("save...")

if __name__ == "__main__":     #当程序执行时
# #调用函数
   main()

