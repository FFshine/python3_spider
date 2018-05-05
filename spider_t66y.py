import requests
from bs4 import BeautifulSoup
import os

proxy = '127.0.0.1:1080'

proxies = {
    'http': 'socks5h://' + proxy,
    'https': 'socks5h://' + proxy
}

URL = 'http://t66y.com/thread0806.php?fid=8&search=&page='
BRFOREURL = 'http://t66y.com/'

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
}

def loadUrl(url):
    '''用requests处理url
    返回得到的html'''
    response = requests.get(url, headers = headers, proxies = proxies, timeout = 10)
    response.encoding = "gb18030"
    return response.text


def getThePage(html, page, vote):
    '''
    用beautifulsoup处理html
    返回处理得到的url，name，vote数
    '''
    vote = int(vote)
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.select('.tal h3 a')
    urls = {}
    upvotes = []
    if page[-1] == str(1):
        for i in range(5,len(pages)):
            upvote = int(soup.select('.tal')[i].parent.select('td')[3].string)
            if upvote >= vote:
                upvotes.append(upvote)
                urls[(BRFOREURL + pages[i].get('href'))] = pages[i].string
    else:
        for i in range(0,len(pages)):
            upvote = int(soup.select('.tal')[i].parent.select('td')[3].string)
            if upvote >= vote:
                upvotes.append(upvote)
                urls[(BRFOREURL + pages[i].get('href'))] = pages[i].string
    return [urls, upvotes]


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


def cookThePage(url):
    '''处理每页里的html
    得到每张图片链接
    返回链接'''
    text = loadUrl(url)
    soup = BeautifulSoup(text, 'html.parser')
    try:
        demo = soup.find('div',{'class': 'tpc_content do_not_catch'})
        demo2 = demo.select('input')
        cook = []
        for i in demo2:
            cook.append(i.get('src'))
        return cook
    except:
        print('cookThePage出错！！')
        return False


def downLoad(i, dir):
    '''
    下载图片
    '''
    imageSrc = i
    name = i[-15:].replace('/', '')
    print(imageSrc)
    try:
        file = requests.get(imageSrc,headers=headers, proxies = proxies, timeout=15).content
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


def main(page=1, vote=1):
    '''功能拼装'''
    try:
        url = loadUrl(page)
        elems = getThePage(url, page, vote)
        print('\n\n本页共有' + str(len(elems[0])) + '个链接满足您的要求！！\n\n')
        for elem, upvote in zip(elems[0], elems[1]):
            print('链接为：' + elem)
            print('赞数为：' + str(upvote) + '\n\n')
            dir = mkdir('【' + str(upvote) + '】 ' + elems[0][elem])
            print('开始下载...')
            try:
                for i in cookThePage(elem):
                    downLoad(i, dir)
            except:
                print('没有抓取到数据！！')
                os.removedirs('【' + str(upvote) + '】 ' + elems[0][elem])
                continue
    except:
        pass


def mainOfMain():
    '''call'''
    os.system('clear')
    page = URL + str(input('请输入您要爬取的页数：'))
    vote = int(input('输入你想筛选的最低赞数：'))
    mkdir('t66y')
    os.chdir('t66y')
    os.system('clear')
    main(page, vote)


if __name__ == '__main__':
    mainOfMain()
    '''for i in range(1, 101):
        print(i)
        page = URL + str(i)
        main(page, 15)'''
