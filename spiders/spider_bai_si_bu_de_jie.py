#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: spider_bai_si_bu_de_jie.py
@time: 2018/9/25 19:58 
@description：利用多线程爬取【百思不得姐】网站的文字和图片并下载到csv文件中
"""

import requests
from lxml import etree
import threading
from queue import Queue
import time
import csv
from urllib import request
import fileutils

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	'Referer': 'http://www.budejie.com/hot/1'
}


class BSSpider(threading.Thread):
	"""
	爬取每一页的数据
	"""

	def __init__(self, page_queue, joke_queue, name, *args, **kwargs):
		super(BSSpider, self).__init__(*args, **kwargs)

		# 1.初始化数据
		self.page_queue = page_queue
		self.joke_queue = joke_queue
		self.name = name

	def run(self):
		while True:
			# 2.如果页面队列为空，就退出循环
			if self.page_queue.empty():
				print(self.name + '任务完成~')
				# while not self.joke_queue.empty():
				# 	print(self.joke_queue.get())
				break

			# 3.从队列中获取页面地址
			page_url = self.page_queue.get()
			self.spider_page(page_url)

			# 6.休眠0.5秒
			time.sleep(0.5)

	def spider_page(self, page_url):
		"""
		爬取一页的数据
		:param page_url:页面的url
		:return:
		"""
		response = requests.get(page_url, headers=HEADERS)
		text_raw = response.text
		html_element = etree.HTML(text_raw)

		# 4.利用xpath去解析数据
		div_elements = html_element.xpath('//div[@class="j-r-list"]')

		for div_element in div_elements:
			duan_zi_elments = div_element.xpath('./ul/li')
			for duan_zi_elment in duan_zi_elments:
				# 【数据】用户名
				username = duan_zi_elment.xpath('.//a[@class="u-user-name"]/text()')[0]

				# 【数据】段子发布时间
				pubtime = duan_zi_elment.xpath('.//span/text()')[0]

				desc_element = duan_zi_elment.xpath('.//div[@class="j-r-list-c-desc"]')[0]
				# 【数据】段子描述内容
				content = desc_element.xpath('./a/text()')[0]

				img_div_element = duan_zi_elment.xpath('.//div[@class="j-r-list-c-img"]')[0]
				img = img_div_element.xpath('.//img/@data-original')[0]
				alt = img_div_element.xpath('.//img/@alt')[0]

				# 5.把解析后的数据以元组的方式放入到队列中去
				self.joke_queue.put((username, content, img, alt, pubtime))


class BSWriter(threading.Thread):
	"""
	下载图片、写入文字数据到csv文件中
	"""

	def __init__(self, page_queue, joke_queue, writer, gLock, name, *args, **kwargs):
		super(BSWriter, self).__init__(*args, **kwargs)

		# 1.初始化
		self.page_queue = page_queue
		self.joke_queue = joke_queue
		self.writer = writer
		self.gLock = gLock
		self.name = name

	def run(self):
		while True:
			if self.joke_queue.empty() and self.page_queue.empty():
				print(self.name + '任务完成~')
				break

			# 2.从joke_queue队列中获取数据
			joke_info = self.joke_queue.get(timeout=40)
			username, content, img, alt, pubtime = joke_info

			# 3.上锁
			self.gLock.acquire()

			# 4.写入数据到csv中
			self.writer.writerow((username, content, img, alt, pubtime))

			# 5.下载图片到本地
			# file_name = alt + fileutils.get_file_suffix(img)
			# request.urlretrieve(img, './imgs/%s' % file_name)

			# 6.释放锁
			self.gLock.release()

			print('写入一条数据成功')


class BSDownImg(threading.Thread):
	"""
	下载图片的消费者
	"""

	def __init__(self, page_queue, joke_queue, gLock, name, *args, **kwargs):
		super(BSDownImg, self).__init__(*args, **kwargs)
		self.page_queue = page_queue
		self.joke_queue = joke_queue
		self.gLock = gLock
		self.name = name

	def run(self):
		while True:
			if self.joke_queue.empty() and self.page_queue.empty():
				print(self.name + '任务完成~')
				break
			username, content, img, alt, pubtime = self.joke_queue.get(timeout=40)

			# 上锁并下载图片
			self.gLock.acquire()
			file_name = alt + fileutils.get_file_suffix(img)
			request.urlretrieve(img, './imgs/%s' % file_name)
			self.gLock.release()

			print('下载一张图片成功')


def spider():
	"""
	爬取百思不得姐的前20页数据
	:return:
	"""

	# 1.构建队列【生产者、消费者需要上锁的对象】
	page_queue = Queue(20)
	joke_queue = Queue(200)

	# 2.锁对象
	gLock = threading.Lock()

	# 3.写入
	fp = open('jokes.csv', 'a', newline='', encoding='utf-8')
	writer = csv.writer(fp)

	# 4.写入csv表头信息
	writer.writerow(['username', 'content', 'img', 'alt', 'pubtime'])

	# 5.前10页待爬取的地址，放入到队列中
	for page_num in range(1, 11):
		page_url = 'http://www.budejie.com/hot/%d' % page_num
		page_queue.put(page_url)

	# 6.构建10个生成者来进行爬虫
	for x in range(1, 6):
		t = BSSpider(page_queue, joke_queue, name='生产者%d' % x)
		t.start()

	# 7.构建 20 个消费者来写入数据到csv文件中
	for x in range(1, 21):
		t = BSWriter(page_queue, joke_queue, writer, gLock, name='消费者-文字%d' % x)
		t.start()

	# 8.构建 50 个消费者来下载图片
	for x in range(1, 51):
		t = BSDownImg(page_queue, joke_queue, gLock, name='消费者-图片%d' % x)
		t.start()


if __name__ == '__main__':
	spider()
