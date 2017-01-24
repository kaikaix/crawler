import proxyclass
from filterclass import *

headers = {'User-agent':'Mozilla/5.0 (x11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0'}
url = 'http://www.xicidaili.com/nn'

def to_crawl_all():
	crawlproxy = proxyclass.CrawlProxy(url=url,headers=headers)
	crawlproxy.resolvedatas()
	print "There are %s proxies."%crawlproxy
	return crawlproxy

def main():
	i = 0
	crawlproxy = to_crawl_all()
	proxies = Queue.Queue()
	while True:
		try:
			proxies.put(crawlproxy[i])
			i+=1
		except IndexError:
			break

	threads = []
	max_threads = 20


	filter_proxy = Filterproxy(proxies)
	open('proxies.txt','a+')
	
	for i in range(max_threads):
		threads.append(
			threading.Thread(target=(filter_proxy.filter_proxy))
		)

	for i in threads:
		i.setDaemon(True)

	for i in threads:
		i.start()

	for i in threads:
		i.join(30)

	print "There are %s proxies can use"%filter_proxy

if __name__ == '__main__':
	main()