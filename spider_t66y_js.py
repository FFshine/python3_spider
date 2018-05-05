import requests
from bs4 import BeautifulSoup
import os
import re


URL = 'http://t66y.com/thread0806.php?fid=7&search=&page='
BRFOREURL = 'http://t66y.com/'

proxy = '127.0.0.1:1080'

proxies = {
    'http': 'socks5h://' + proxy,
    'https': 'socks5h://' + proxy
}

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
}



def getPageHtml(url):
    '''获取主页html
    '''
    re = requests.get(url, headers = headers, proxies = proxies, timeout = 10)
    re.encoding = 'gb18030'
    return re.text

def cookTheMainPage(content):
    '''处理主页html
    获取含图片的html
    返回 [链接：名称]
    '''
    soup = BeautifulSoup(content, 'html.parser')
    pages = soup.select('.tal h3 a')
    urls = {}
    for i in pages:
        if re.search(r'\d+P', i.string):
            urls[(BRFOREURL + i.get('href'))] = i.string
    return urls

def mkdir(name):
    '''
    创建目录'''
    print('创建目录：\n')
    if not os.path.exists(name):
        os.makedirs(name)
        print(name + '\n\n')
    else:
        print('目录' + name + '已经存在！\n\n')
    return name

def cookPages(url):
    '''分析图片页 取得图片页面和图片名称
    返回 [图片URL：图片名称]
    '''
    imageUrlAndNames = {}
    html = getPageHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find('div',{'class': 'tpc_content do_not_catch'})
    imageUrl = temp.select('img')
    for i in imageUrl:
        image = i.get('src')
        imageUrlAndNames[image] = image[-15:].replace('/', '')
    return imageUrlAndNames

def downLoad(i, imageName, dir):
    '''
    下载图片
    '''
    imageSrc = i
    name = imageName
    print(imageSrc)
    try:
        file = requests.get(imageSrc, headers = headers, proxies = proxies, timeout = 15).content
        if file != "" and file !='bad request!':
            try:
                f = open(dir + '/' + name, 'wb')
                f.write(file)
                f.close()
            except:
                print("写入出错")
                return
        print('下载完成 =>=>' + name)
    except:
        print('download 出错！！')
        pass

def main():
    '''功能组装'''
    try:
        mkdir('t66y_git')
    except:
        pass
    os.chdir('t66y_git')
    os.system('clear')
    page = 1 #默认第一页
    page = input('请输入您要爬取的页数：')
    urls = cookTheMainPage(getPageHtml(URL + str(page)))
    for url in urls:
        mkdir(urls[url])
        image = cookPages(url)
        for i in image:
            downLoad(i, image[i], urls[url])

main()
