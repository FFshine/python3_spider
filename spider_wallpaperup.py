import requests
from bs4 import BeautifulSoup
import os
import re

proxy = '127.0.0.1:1080'

proxies = {
    'http': 'socks5://' + proxy,
    'https': 'socks5://' + proxy
}

#import socket
#import socks

#socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080)
#socket.socket = socks.socksocket

URL = 'https://www.wallpaperup.com/most/downloaded/'
BEFOREURL = 'https://www.wallpaperup.com'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
}


def getHTML(url):
    '''获取html
    返回html'''
    try:
        r = requests.get(url, headers=headers, proxies = proxies, timeout=10)  
        r.encoding = 'utf-8'
        return r.text
    except:
        return False

def cookMainPage(html):
    '''分析主页中html
    获取图片页html
    并返回[link]'''
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        thumbLinks = soup.select('.thumb-adv .black a')
        links = []
        for i in thumbLinks:
            links.append(i.get('href'))
        return links

def cookTheScondePage(html):
    '''分析图片页html
    获取下载链接
    并返回'''
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        imagelinks = soup.select('.card-block a')
        link = imagelinks[0].get('href')
        return link

def downloadImage(link, name):
    '''下载并保存'''
    imageSrc = link
    print(imageSrc)
    try:
        file = requests.get(imageSrc,headers=headers, proxies = proxies, timeout=100).content
        if file != "" and file !='bad request!':
            try:
                f = open(name + '.jpg', 'wb')
                f.write(file)
                f.close()
            except:
                print("写入出错")
                return
        print('下载完成 =>=>' + name + '.jpg')
    except:
        print('download 出错！！')
        pass

def main(index=1):
    os.chdir('/home/ss/Wallpapers')
    mainPageHTML = getHTML(URL + str(index))
    for link in cookMainPage(mainPageHTML):
        name = re.findall(".*\/(.*)\..*",link)[0]
        if getHTML(BEFOREURL + link):
            scondeHTML = getHTML(BEFOREURL + link)
        imageLink =BEFOREURL + cookTheScondePage(scondeHTML)
        downloadImage(imageLink, name)

if __name__ == '__main__':
    index = input('请输入你要爬取的页数：')
    main(index)