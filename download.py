#coding=utf-8
import sqlite3
import requests
import bs4
import os

keywords="刀剣乱舞1000users入り"
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6','Referer':'http://www.pixiv.net/'} 
pixiv_id=
password=
ps=1
pe=25
# f=open('cookie.txt')
# _cookies = f.read()

s = requests.Session()
data = {
	'mode': 'login',
	'skip': '1',
	'pixiv_id': pixiv_id,
	'pass': password
		}
r = s.post('https://www.secure.pixiv.net/login.php', data=data)
if r.url == 'http://www.pixiv.net/mypage.php':
	print('Login succet3ssfully')
else:
	print('Login failed')
def islogin():
	r = s.get('http://www.pixiv.net')
	if r.url != 'http://www.pixiv.net/mypage.php':
		print('Session expired')
		return False;
	else :
		return True;

def numlize(s,oth=''):   
    fomart = '0123456789'   
    for c in s:   
        if not c in fomart:   
             s = s.replace(c,'');   
    return s;   
def createFilename(url, name, folder):
    dotSplit = url.split('.')
    if name == None:
        # use the same as the url
        slashSplit = dotSplit[-2].split('/')
        name = slashSplit[-1]
    ext = dotSplit[-1]
    file = '{}{}.{}'.format(folder, name, ext)
    return file
def getImageFast(url, name=None, folder='./result'):
    file = createFilename(url, name, folder)
    r = s.get(url,headers=headers)
    f = open(file, 'wb')
    f.write(r.content)
    f.close()
def catchmangalink(a):
	response = s.get('http://www.pixiv.net/member_illust.php?mode=manga&illust_id='+a)
	soup = bs4.BeautifulSoup(response.text)
	total = int(soup.select('span.total')[0].contents[0])
	lurls=[]
	for i in range(0,total-1):
		response = s.get('http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id='+a+'&page='+str(i))
		soup = bs4.BeautifulSoup(response.text)
		urls = soup.select('img')[0].attrs.get('src')
		getImageFast(urls)
		print (a+'downloaded'+str(i))
def catchpiclink(a):
	response = s.get('http://www.pixiv.net/member_illust.php?mode=medium&illust_id='+ a)
	soup = bs4.BeautifulSoup(response.text)
	urls = soup.select('img.original-image')[0].attrs.get('data-src')
	getImageFast(urls)
	print (a+'downloaded')
	return urls;

if islogin():
	for i in range(ps,pe):
		response = s.get('http://www.pixiv.net/search.php?s_mode=s_tag_full&word='+keywords+'&type=illust&p='+str(i))
		print ("now eating "+str(i))
		soup = bs4.BeautifulSoup(response.text)
		pic = soup.select('li.image-item')
		lis = []
		for li in pic:
			a=numlize(li.contents[0].attrs.get('href'))
			cl=li.contents[0].attrs.get('class')
			typ = 0
			if 'multiple' in cl:
				typ = 1
			urls=""
			if typ ==0:
				if os.path.isfile('result'+a+'_p0.jpg')==False:				
					urls = catchpiclink(a)
				else:
					print (a+"exist!")
			else:
				#urls=catchmangalink(a)
				pass
else:
	print ("error")
