#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: spider_tencent_recruit
@time: 2018/9/17 11:22 
@description：爬腾讯招聘职位信息
"""

import requests

from lxml import etree

import time

# 每页的职位数
PAGE_SIZE = 10

BASE_DOMAIN = 'https://hr.tencent.com/'

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
	'Referer': 'https://hr.tencent.com/position.php?lid=&tid=&keywords=python&start=10',
	'Cookie': '_ga=GA1.2.1222789966.1535530525; pgv_pvi=8193187840; pgv_si=s2985358336; PHPSESSID=22e3m8aknd19s1gqkh0i9eisk0; Hm_lvt_0bd5902d44e80b78cb1cd01ca0e85f4a=1536726429,1536908218,1537154694,1537166987; Hm_lpvt_0bd5902d44e80b78cb1cd01ca0e85f4a=1537167106'
}


def get_jo_detail_urls(page_url):
	"""
	1.根据当前页面url地址获取每一个职位的详情页面url
	:param page_url:当前页面的url
	:return:
	"""
	response = requests.get(page_url, headers=HEADERS)

	html_element = etree.HTML(response.text)

	# print(etree.tostring(html_element, encoding='utf-8').decode('utf-8'))

	detail_urls = html_element.xpath('//tr[@class="even" or @class="odd"]//a/@href')

	# 获取所有职位详情页面的url
	detail_urls = map(lambda detail_url: BASE_DOMAIN + detail_url, detail_urls)

	return detail_urls


def get_detail_msg(detail_url):
	"""
	2.获取某个职位的详细数据
	:param detail_url: 职位详细页面的url
	:return: 职位数据
	"""
	# print('请求的详细地址是:' + detail_url)
	response = requests.get(detail_url, headers=HEADERS)
	html_element = etree.HTML(response.text)

	position = {}

	# 【数据】获取职位标题
	title = html_element.xpath('//tr[@class="h"]/td/text()')[0]
	position['title'] = title

	# 【数据】工作地点/职位类别
	top_infos = html_element.xpath('//tr[@class="c bottomline"]//text()')
	position['location'] = top_infos[top_infos.index('工作地点：') + 1]
	position['category'] = top_infos[top_infos.index('职位类别：') + 1]

	content_infos = html_element.xpath('//ul[@class="squareli"]')
	# 【数据】工作职责
	work_do_info = content_infos[0]
	position['duty'] = work_do_info.xpath("./li/text()")

	# 【数据】工作要求
	work_ask_info = content_infos[1]
	position['ask'] = work_ask_info.xpath('./li/text()')

	return position


def spider():
	# 0.待返回的职位数据
	positions = []

	# 1.获取前10页的职位数据
	for page_num in range(0, 10):
		print('开始爬取第{}页数据'.format(page_num + 1))

		# 2.每一页的地址
		url = 'https://hr.tencent.com/position.php?keywords=python&lid=0&tid=0&start={}#a'.format(page_num * PAGE_SIZE)

		# 3.获取【当前页】所有职位的【详情页面的url】
		detail_urls = get_jo_detail_urls(url)

		# 4.一个个去解析详情页面的数据
		for detail_url in detail_urls:
			position = get_detail_msg(detail_url)
			positions.append(position)

		time.sleep(1)

	print('爬取完成！')
	print(positions)


if __name__ == '__main__':
	spider()
