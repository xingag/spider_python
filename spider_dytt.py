#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: xag
@license: Apache Licence
@contact: xinganguo@gmail.com
@site: http://www.xingag.top
@software: PyCharm
@file: 4.dytt.py
@time: 2018/9/16 18:46
@description：爬电影天堂【 lxml + xpath + requests】【2018新片精品，包含更多】
"""

import requests
from lxml import etree
import time

# url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_1.html'

# 主页地址
BASE_DOMAIN = 'http://www.dytt8.net'

HEADERS = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
}


def get_detail_urls(url):
	"""
	获取电影详情页面的url
	:param url: 每一页电影列表的地址url
	:return:
	"""
	response = requests.get(url, headers=HEADERS)

	# 注意：右键查看源代码，charset=gb2312" 编码方式【网站编码不规范，解码必须用响应的编码方式进行解码】
	# print(response.content.decode('gbk'))

	# html_element = etree.HTML(response.content.decode('gbk'))

	# 注意：电影天堂第3页使用默认的gbk会有乱码，这里使用默认的解码方式【href为英文，解析不会受影响】
	html_element = etree.HTML(response.text)

	# 【数据 - 字符串列表】详情页面地址
	# 所有class为tbspan的table标签/子孙标签中的a标签的href属性
	detail_urls = html_element.xpath('//table[@class="tbspan"]//a/@href')

	# 深拷贝一份列表数据，实现一变遍历列表，一边删除列表数据
	# 过滤掉【综合电影】导致的脏数据
	detail_urls_new = detail_urls
	for index, detail_url in enumerate(detail_urls_new):
		if detail_url == '/html/gndy/jddy/index.html':
			detail_urls.remove(detail_url)

	# print(detail_urls)

	# print(BASE_DOMAIN + detail_url)
	# 组装详情页面的地址
	detail_urls = map(lambda x: BASE_DOMAIN + x, detail_urls)

	return detail_urls


def parse_detail_page(detail_url):
	"""
	解析电影详情页面
	:param detail_url: 详情页面的地址
	:return:
	"""
	response = requests.get(detail_url, headers=HEADERS)
	text = response.content.decode('gbk')
	html_element = etree.HTML(text)

	# 【数据 - 电影标题】
	title = html_element.xpath('//div[@class="title_all"]//font[@color="#07519a"]/text()')[0]

	# 获取zoom标签
	zoom_element = html_element.xpath('//div[@id="Zoom"]')[0]

	# 【数据 - 电影封面和电影截图】
	imgs = zoom_element.xpath(".//img/@src")

	# 注意：为了避免脏数据导致应用挂掉，提前初始化
	year, country, type, rating, duration, director, actors, cover, screen_shot, download_url = '', '', '', '', '', '', '', '', '', ''

	if len(imgs) > 0:
		cover = imgs[0]

	# 【数据 - 电影截图】
	if len(imgs) > 1:
		screen_shot = imgs[1]

	# 获取div[@id='zoom']标签下面的所有的文本数据【子孙所有的text文本数据】
	infos = zoom_element.xpath('.//text()')

	# 解析具体内容的函数
	def parse_info(info, rule):
		return info.replace(rule, '').strip()

	# 遍历infos每一项去获取有用的数据
	for key, info in enumerate(infos):

		# print('遍历第{}项'.format(key))
		# print(info)
		# print('结束==================================================')

		if info.startswith('◎年　　代'):
			# 年代
			year = parse_info(info, '◎年　　代')
		elif info.startswith('◎产　　地'):
			# 产地
			country = parse_info(info, '◎产　　地')
		elif info.startswith('◎类　　别'):
			# 类别
			type = parse_info(info, '◎类　　别')
		elif info.startswith('◎豆瓣评分'):
			# 豆瓣评分
			rating = parse_info(info, '◎豆瓣评分')
		elif info.startswith('◎片　　长'):
			# 片长
			duration = parse_info(info, '◎片　　长')
		elif info.startswith('◎导　　演'):
			# 导演
			director = parse_info(info, '◎导　　演')
		elif info.startswith('◎主　　演'):
			# 演员【第一个演员】
			actor_first = parse_info(info, '◎主　　演')

			actors = [actor_first]

			# 继续往下面遍历
			for index in range(key + 1, len(infos)):
				item = infos[index].strip()
				if item.startswith('◎简　　介'):
					break
				# 获取所有的演员
				# print(item)
				actors.append(item)
		elif info.startswith('◎简　　介'):
			# desc = parse_info(info, '◎简　　介')

			for index in range(key + 1, len(infos)):
				item = infos[index].strip()
				if item.startswith('【下载地址】'):
					break
				desc = item

	print(detail_url)

	# 下载地址
	if len(html_element.xpath('//td[@bgcolor="#fdfddf"]/a/text()')) > 0:
		download_url = html_element.xpath('//td[@bgcolor="#fdfddf"]/a/text()')[0]
	elif len(html_element.xpath('//td[@bgcolor="#fdfddf"]/text()')) > 0:
		download_url = html_element.xpath('//td[@bgcolor="#fdfddf"]/text()')[0]

	film = {
		'title': title,
		'cover': cover,
		'screen_shot': screen_shot,
		'year': year,
		'country': country,
		'type': type,
		'rating': rating,
		'duration': duration,
		'director': director,
		'actors': actors,
		'desc': desc,
		'download_url': download_url
	}

	return film


def spider():
	"""
	爬虫的入口
	:return:
	"""
	base_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'

	films = []

	# 1.获取第1-10页的数据
	for index in range(1, 11):
		print('开始爬第{}页'.format(index))

		# 2.电影列表的地址url
		url = base_url.format(index)

		# 3.获取当前页面包含的所有电影【详情地址】
		detail_urls = get_detail_urls(url)

		# 4.解析每一项电影的详情页面

		for key, detail_url in enumerate(detail_urls):
			# print('索引:' + str(key) + ',地址：' + detail_url)
			# print('解析详情页面:' + detail_url)
			film = parse_detail_page(detail_url)

			films.append(film)

		# 5.每爬取一页，就休眠2秒钟
		time.sleep(1)

	print(films)


if __name__ == '__main__':
	spider()
