#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: spider_gushiwen 
@time: 2018/9/21 17:34 
@description：利用【正则表达式】爬取【古诗文】网
@link：https://www.gushiwen.org/
"""

import requests
import re
import time

HEADERS = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


# 利用正则表达式去爬虫的注意事项
# 1.正则表达式去爬取元素的时候，与 xpath、bs4 不同，没有结构关系，都是当成一个字符串进行匹配处理
# 2.re.DOTALL可以让【.符号】匹配到所有的字符【包含\n】
# 3.正则表达式匹配【任意多字符】一般采用非饥饿型方式【.*?】


def spider_page(url):
	"""
	爬取某一页的数据
	:param url:
	:return:
	"""
	response = requests.get(url, headers=HEADERS)
	text_raw = response.text

	# print(text_raw)

	# 1.获取所有的标题
	titles = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>', text_raw, re.DOTALL)

	# 2.获取所有的朝代
	dynasties = re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>', text_raw, re.DOTALL)

	# 3.获取作者信息
	authors = re.findall(r'<p\sclass="source">.*?<a.*?>.*?<a.*?>(.*?)</a>', text_raw, re.DOTALL)

	# 4.获取古诗文内容
	# 内容待进一步美化【去掉多余的元素】
	contents_pre = re.findall(r'<div\sclass="contson".*?>(.*?)</div>', text_raw, re.DOTALL)

	contents = []
	for content_pre in contents_pre:
		# 4.1 利用sub()函数把内容中的【<.*?>或者换行字符】替换为空
		content = re.sub(r'<.*?>|\n', "", content_pre)
		contents.append(content.strip())

	# 诗词列表数据
	poems = []

	# 5. 使用zip()把四个列表组合在一起
	for value in zip(titles, dynasties, authors, contents):
		# 5.1 自动进行解包放入到变量当中
		title, dynastie, author, content = value

		# 5.2 新建dict，并加入到诗词列表数据中
		poem = {
			'title': title,
			'dynastie': dynastie,
			'author': author,
			'content': content
		}

		poems.append(poem)

	return poems


def spider():
	# 全部诗词列表数据
	poems = []

	# 1.爬取前面10页数据
	for page_num in range(10):
		url = 'https://www.gushiwen.org/default_{}.aspx'.format(page_num + 1)

		print('开始爬取第{}页诗词数据'.format(page_num + 1))

		poems.append(spider_page(url))

		time.sleep(1)

	# 2.显示数据
	for poem in poems:
		print(poem)
		print("==" * 40)

	print('恭喜！爬取数据完成！')


if __name__ == '__main__':
	spider()
