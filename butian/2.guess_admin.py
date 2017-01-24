import threading
import urllib2
import urllib
import sys
import Queue

urls = Queue.Queue()
user_agent='Mozilla/5.0 (x11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0'
headers = {'User-agent':user_agent}
url = None
background = []

with open('host.txt','r') as file:
    for url in file.readlines():
        urls.put(url)

with open('dic.txt','r') as file:
    for i in file.readlines():
        background.append(i.rstrip())

class Guessbackgroud(object):
    def __init__(self,urls_queue,headers,background):
        self.urls_queue = urls_queue
        self.headers = headers
        self.dic = background

    def download(self,url):
        res = None
        e = None
        request = urllib2.Request(url,headers=headers)
        try:
            res = urllib2.urlopen(request)
            return res,e
        except urllib2.URLError as e:
            return res,e
    
    def guess(self,number,normalfile,abnormalfile):
        print "Start %d"%number

        while not self.urls_queue.empty():
            url = self.urls_queue.get().rstrip()

            urls = self.get_urls(url)
            
            for target in urls:
                res,e = self.download(target)
            
                if res == None:
                    if hasattr(e,'code'):
                        if e.code != 404:
                            abnormalfile.write(target+':'+str(e.code)+'\n')
                else:
                    normalfile.write(target+'\n')
            
        return 0
    
    def get_urls(self,url):
        urls = []
        for back in self.dic:
            urls.append('http://'+url+'/'+back)
        return urls


def main():
    threads = []
    max_thread = 20
    file = open('normal.txt','w')
    abfile = open('abnormal.txt','w')
    attack = Guessbackgroud(urls,headers,background)

    for i in range(max_thread):
        threads.append(
            threading.Thread(target=attack.guess,args=(i,file,abfile))
        )
    
    for i in threads:
        i.setDaemon(True)
    
    for i in threads:
        i.start()

    for i in threads:
        i.join(1)
    
    return 0

main()

