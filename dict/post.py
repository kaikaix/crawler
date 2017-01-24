# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup as bs
import urllib
import requests
import pprint
import re

def main():
    data={}
    url = 'http://www.caimima.net'
    proxy = {'http':'127.0.0.1:8080'}

    bd_session = requests.Session()
    r = bd_session.get(url)
    soup = bs(r.content.decode('UTF-8'),'lxml')
    form = soup.find_all(name='form')[0]
    names = form.find_all(name='textarea',attrs={'name':re.compile('.')})

    for name in names:
        content = None
        print name['name']
        content = raw_input('输入:')
        data[name['name']] = content

    r = bd_session.post(url,data)
    soup = bs(r.content,'lxml')
    link = soup.find_all(name='a',attrs={'href':re.compile('/index.php\?.+?')})[0]
    
    last = url+link['href']
    print last
    pwd_html = bd_session.get(last).content
    
    pwds_txt = re.findall('(.+?)<br />',pwd_html)
    with open('pwd.txt','w') as f:
        for pwd_txt in pwds_txt:
            f.write(pwd_txt+'\n')

if __name__ == '__main__':
    main()
