import requests
import findtic
import Queue
import threading
import time

class SendMessage(findtic.Find_List):
    def __init__(self,links_queue):
        findtic.Find_List.__init__(self)
        self.links_queue = links_queue
        self.times = 0
        self.headers = {'Referer':'','Cookie':""""""}
        self.data = {'posttime':'1485183756','message':'666666666666','useig':'1','formhash':'d9ff73e8','subject':'++'}
        self.param = {'tid':'18289','handlekey':'fastpost','fid':'58','extra':'page%3D1','action':'reply','replysubmit': 'yes', 'inajax': '1', 'infloat': 'yes', 'mod': 'post'}
    
    def postdata(self):
        self.sure = False
        while not self.links_queue.empty():
            url = self.links_queue.get()
            print url
            self.headers['Referer'] = url
            r = self.download(url=url,param=self.param,data=self.data,headers=self.headers)
            print r.content

            time.sleep(6)

            self.times += 1
            if self.times == 50:
                time.sleep(3600)

def main():
    links_queue = Queue.Queue()
    threads = []

    with open('lists.txt','r') as f:
        for link in f.readlines():
            links_queue.put(link.strip('\n'))

    send = SendMessage(links_queue)

    send.postdata()

if __name__ == "__main__":
    main()
