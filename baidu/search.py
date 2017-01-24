import urllib2,urllib
import re
import sys
import Queue
import threading
from bs4 import BeautifulSoup as bs

user_agent='Mozilla/5.0 (x11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0'
headers = {'User-agent':user_agent}
requests = Queue.Queue()
links = Queue.Queue()

class CrawlBaidu(object):
    def __init__(self,urls_queue):
        self.urls_queue = urls_queue
    
    def download(self,request,num_retries=2):
        e = None
        response = None
        try:
            response = urllib2.urlopen(request)
            return response,e
        except urllib2.URLError as e:
            if num_retries > 0:
                if hasattr(e,'code') and 500<= e.code < 600:
                    return self.download(request,num_retries-1)
            return response,e
    
    #get links
    def choose(self,html,error_links,number):
        global links

        soup = bs(html,'lxml')
        urls = soup.find_all(name='a',attrs={'data-click':re.compile('.'),'class':None})# to match links

        for url in urls:
            response,e = self.download(url['href'])

            if e == None:
                links.put(response.geturl()) #add links to 'result'
                print "Catch "+response.geturl()+" ----is caught by thread %d"%number
            else:
                if hasattr(e,'code'):
                    print 'choose:'+str(e.code)
                    error_links.put(url['href']+':'+str(e.code)) #put error links into error_links queue

        return 0

    #get all links include baidus'
    def crawl_link(self,number,error_links):
        sys.stdout.write("Start:%d\n"%number)

        while not self.urls_queue.empty():
            request = self.urls_queue.get()
            response,e=self.download(request) #get request and then send request to target

            if response:
                html = response.read()
                self.choose(html,error_links,number)
            else:
                if hasattr(e,'code'):
                    print "crawl_link:"+str(e.code)
                    error_links.put(e.url+':'+str(e.code))
        return 0


def main():
    if len(sys.argv) != 2:
        print "%s [keyword]"%sys.argv[0]
        sys.exit(0)
    
    for i in range(0,760,10):
        url = 'https://www.baidu.com/s?wd=%s&pn=%d'%(urllib.quote(sys.argv[1]),i)
        request = urllib2.Request(url,headers=headers)
        requests.put(request)


    global links

    cache = []
    crawlbaidu = CrawlBaidu(requests)
    error_links = Queue.Queue()
    threads = []
    max_thread = 20
    
    for i in range(max_thread):
        threads.append(threading.Thread(target=crawlbaidu.crawl_link,args=(i,error_links)))

    for i in threads:
        i.setDaemon(True)

    for i in threads:
        i.start()
    
    for i in threads:
        i.join(30)
    
    with open('website.txt','w') as f:
        while not links.empty():
            link = links.get()
            if link not in cache:
                f.write(link+'\n')
                cache.append(link)
    
    print "There are %d websites"%len(cache)
    
    cache = []
    print error_links.qsize()
    with open('error.txt','w') as f:
        while not error_links.empty():
            link = error_links.get()
            if link not in cache:
                f.write(link+'\n\n')
                cache.append(link)
    
    print "There are %d error websites"%len(cache)

    return 0

if __name__=='__main__':
    main()
