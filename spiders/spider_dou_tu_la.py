#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: spider_dou_tu_la
@time: 2018/9/25 14:40 
@description：多线程去爬取斗图啦网站的表情
@spider_to：http://www.doutula.com/
"""

import requests
from lxml import etree
from urllib import request
import re
import os
import threading
from queue import Queue
import time

# 技术点
# 1.使用request是获取html数据
# 2.使用xpath解析数据
# 3.使用正则表达式sub()函数过滤掉特殊的字符
# 4.使用urllib.request.urlretrieve()下载图片
# 5.生产者和消费者模式分离
# 6.使用queue[线程安全]去保存【每一页的爬取地址】和【表情图片地址】

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


class Procuder(threading.Thread):
	"""
	生产者
	爬取页面，获取图片地址加入到表情图片队列中
	"""

	def __init__(self, name, page_queue, img_queue, *args, **kwargs):
		super(Procuder, self).__init__(*args, **kwargs)
		self.name = name
		self.page_queue = page_queue
		self.img_queue = img_queue

	def run(self):
		while True:
			if self.page_queue.empty():
				print(self.name + '任务完成~')
				break
			# 1.获取每一页的url
			page_url = self.page_queue.get()

			# 2.爬取页面的数据
			self.spider_page(page_url)

			# 3.休眠0.5秒
			time.sleep(0.5)

	def spider_page(self, url):
		"""
		爬取每一页
		:param url: 每一页的地址
		:return:
		"""
		response = requests.get(url, headers=HEADERS)
		text_raw = response.text

		# 1.使用etree
		html_raw = etree.HTML(text_raw)

		# 2.使用xpath解析数据
		# 注意：过滤掉gif标签图片
		imgs = html_raw.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')

		# 3.获取图片的实际连接并下载到本地
		for img in imgs:
			# 3.1 图片的实际地址
			img_url = img.get('data-original')

			# 3.2 图片名称替换特殊符号
			alt = re.sub(r'[\?？\.，。！!\*]', '', img.get('alt'))

			# 3.3 提取图片的后缀,组装成文件的名字
			img_name = alt + os.path.splitext(img_url)[-1]

			# 3.4 把爬取到的表情【图片地址+图片名称】以【元组】的形式加入到队列图片队列中
			self.img_queue.put((img_url, img_name))


class Consumer(threading.Thread):
	"""
	消费者
	获取图片的地址下载到本地
	"""

	def __init__(self, name, page_queue, img_queue, *args, **kwargs):
		super(Consumer, self).__init__(*args, **kwargs)
		self.name = name
		self.page_queue = page_queue
		self.img_queue = img_queue

	def run(self):
		while True:

			if self.img_queue.empty() and self.page_queue.empty():
				print(self.name + '任务完成~')
				break

			# 1.解包，获取图片的地址 + 图片的名称
			img_url, img_name = self.img_queue.get()

			# 2.使用urlretrieve()函数下载图片到本地
			request.urlretrieve(img_url, './imgs/%s' % img_name)

			print(img_name + "下载完成")


def spider():
	# 1.页面的队列
	page_queue = Queue(100)

	# 2.表情图片的队列
	# 注意：队列的大小尽量设置大一些，保证线程减少等待的时间
	img_queue = Queue(1000)

	# 3.爬取页面的地址
	for x in range(1, 10):
		url = 'http://www.doutula.com/photo/list/?page=%d' % x

		# 3.1 存入到页面地址队列中
		page_queue.put(url)

	# 创建5个生成者和5个消费者
	# 生产者：爬取每一页的数据，获取表情图片的url
	# 消费者：从表情队列中获取表情图片的实际地址并下载到本地
	for x in range(5):
		t = Procuder(name='生产线程-%d' % x, page_queue=page_queue, img_queue=img_queue)
		t.start()

	for x in range(5):
		t = Consumer(name='消费线程-%d' % x, page_queue=page_queue, img_queue=img_queue)
		t.start()


if __name__ == '__main__':
	spider()
