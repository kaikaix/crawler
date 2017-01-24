from bs4 import BeautifulSoup as bs
import urllib
import requests
import sys
import re
import pickle


class CrawlProxy(object):
    def __init__(self,headers=None,url=None):
        self.headers = headers
        self.url = url
        self.proxies_data = []

    def __getitem__(self,n):
        return self.proxies_data[n]

    def __str__(self):
        return str(len(self.proxies_data))

    def download(self,url=None,proxy=None,timeout=6):
        try:
            response = requests.get(url=url,headers=self.headers,proxies=proxy,timeout=timeout)
            return response
        except Exception as e:
            return False

    def resolvedatas(self):
        response = self.download(self.url)

        soup = bs(response.content,'lxml')
        datas = soup.find_all(name='tr',attrs={'class':'odd'})
        for data in datas:
            proxy = []
            proxy_soup = bs(str(data),'lxml')
            tmp = proxy_soup.find_all(name='td')
            for i in [1,2,5]:
                proxy.append(str(tmp[i].string).lower())

            self.proxies_data.append({'%s'%proxy[2]:'%s:%s'%(proxy[0],proxy[1])})
