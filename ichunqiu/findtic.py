import requests
from bs4 import BeautifulSoup as bs
import Queue
import threading

link_queue = Queue.Queue()

class Find_List(object):
    def __init__(self):
        self.baseurl = 'http://bbs.ichunqiu.com/'
        self.sure = True
        self.links = Queue.Queue()
        pass
    
    def download(self,url=None,data=None,param=None,headers=None,deep=2):
        r=None
        if deep:
            try:
                if self.sure:
                    r = requests.get(url,params=param,headers=headers)
                    print "Get"
                else:
                    r = requests.post(url,data=data,params=param,headers=headers)
                    print "Post"
            except Exception as e:
                deep -= 1
                print e

        return r

    def find_module(self,module='forum.php'):
        url =self.baseurl+module
        r = self.download(url)
        
        soup = bs(r.content,'lxml')
        styles = soup.find_all(name='h2',attrs={'style':'line-height:18px;font-size:18px;margin-bottom:28px;'})
        for style in styles:
            soup = bs(str(style),'lxml')
            links = soup.find_all(name='a')
            for link in links:
                self.links.put(self.baseurl+link['href'])
        
    def find_all_links(self):
        global link_queue
        while not self.links.empty():
            url = self.links.get()
            print url
            r = self.download(url)
            html = r.content

            #find tic links
            soup = bs(html,'lxml')
            names = soup.find_all(name='a',attrs={'class':'s xst'})
            for link in names:
                l = self.baseurl+link['href']
                link_queue.put(l)
                print l
            
            #store next page's link
            next_link = soup.find_all(name='a',attrs={'class':'nxt'})
            if next_link != []:
                next_link=self.baseurl+next_link[0]['href']
                self.links.put(next_link)
                print next_link


def main():
    global link_queue

    #define variable
    find_list = Find_List()
    threads = []
    max_thread = 10

    find_list.find_module('forum.php')

    #create threads
    for i in range(max_thread):
        threads.append(threading.Thread(target=find_list.find_all_links))
    
    for i in threads:
        i.setDaemon(True)

    for i in threads:
        i.start()

    for i in threads:
        i.join(9)

    with open('lists.txt','w') as f:
        while not link_queue.empty():
            f.write(link_queue.get()+'\n')

if __name__ == "__main__":
    main()