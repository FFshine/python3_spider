import requests
from bs4 import BeautifulSoup
import os

URL = 'http://www.mmjpg.com/home/'


headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
    'Referer': 'http://www.mmjpg.com'
}

def getUrl(index, imgUrl):
    response = requests.get(imgUrl + '/' + str(index), headers=headers,timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    elem = soup.find(id='content').find('img')
    imageSrc = elem.get('src')
    name = elem.get('alt')
    name = name[0:-4]
    r = (imageSrc, name, index)
    return r

def downLoad(i, dir):
    imageSrc = i[0]
    name = i[1] + str(i[2]) + '.jpg'
    print(imageSrc)
    f = open(dir + '/' + name, 'wb')
    f.write(requests.get(imageSrc,headers=headers, timeout=10).content)
    f.close()
    print('done' + name)

def getIndex(imgUrl):
    response = requests.get(imgUrl +'/' + str(1),headers=headers, timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    pageelem = soup.select('#page a')
    return pageelem[6].string

def getPage(page):
    response = requests.get(URL + page, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    href = soup.select('.pic a')
    imgDict = {}
    for i in range(0, 30, 2):
        imgDict[href[i].get('href')] = href[i].select('img')[0].get('alt')
    return imgDict

def mkdir(name):
    if not os.path.exists(name):
        os.makedirs(name)
    return name

def main():
    page  = str(input("你想下载哪页："))
    for elem in getPage(page):
        print(elem)
        print(getPage(page)[elem])
        index = getIndex(elem)
        for i in range(1, int(index) + 1):
             demo = getUrl(i ,elem)
             dir = mkdir(getPage(page)[elem])
             downLoad(demo, dir)



if __name__ == '__main__':
    main()

