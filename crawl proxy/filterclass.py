#!/usr/bin/python

import threading
import proxyclass
import Queue
import pickle
import sys
import re

class Filterproxy(proxyclass.CrawlProxy):
	def __init__(self,proxies=None):
		self.ip_url = "http://1212.ip138.com/ic.asp"
		self.proxies = proxies
		self.max = 0
		proxyclass.CrawlProxy.__init__(self)

	def __str__(self):
		return str(self.max)  #to return max number that store

	def filter_proxy(self):
		while not self.proxies.empty():
			proxy = self.proxies.get()
			response = self.download(url=self.ip_url,proxy=proxy)

			if response:
				html = response.text
			else:
				continue

			key = self.take_ip(html=html,proxy=proxy) #to take ip out from dict

	def take_ip(self,html,proxy):
		get_ip = re.findall('\[(.+?)\]',html)[0]

		key = proxy.keys()[0]
		proxy_tmp = proxy[key].split(':')

		if get_ip == proxy_tmp[0]:
			self.store_data(key+":"+proxy[key])
		else:
			return False


	def store_data(self,proxy):  #the method is like its name
		with open('proxies.txt','r') as f:
			for i in f.readlines():
				i = i.strip('\n')
				if i == proxy:
					proxy = None
					break
		if proxy:
			with open("proxies.txt",'a+') as f:
				f.write(proxy+'\n')
				self.max+=1

