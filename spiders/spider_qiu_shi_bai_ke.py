#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: spider_qiu_shi_bai_ke.py 
@time: 2018/9/21 23:16 
@description：利用正则表达式去爬取【糗事百科】的文字数据
@link：https://www.qiushibaike.com/text/
"""

import re
import requests

# 待爬取的地址
base_url = 'https://www.qiushibaike.com/text/page/%s/'

HEADERS = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	'Referer': 'https://www.qiushibaike.com/'
}


def spider_page(url):
	"""
	爬取某一页的数据
	:param url:
	:return:
	"""
	response = requests.get(url, headers=HEADERS)
	text_raw = response.text

	# 获取此页的段子数据
	# 1.获取作者列表数据
	authors_pre = re.findall(r'<div\sclass="article.*?<h2>(.*?)</h2>', text_raw, re.DOTALL)

	# 1.1 对获取的作者信息进一步进行处理【数据中包含\n】
	authors = []
	for author_pre in authors_pre:
		author = re.sub(r'\n', '', author_pre)
		authors.append(author)

	# 2.获取段子列表数据
	contents_pre = re.findall(r'<div\sclass="content">.*?<span>(.*?)</span>', text_raw, re.S)

	# 2.1 对段子数据进一步处理【数据中包含\n和<br/>】
	contents = []
	for content_pre in contents_pre:
		content = re.sub(r'<.*?>|\n', '', content_pre)
		contents.append(content)

	# 3.把两个列表数据组装成一个新的列表中
	jokes = []
	for temp in zip(authors, contents):
		author, content = temp
		jokes.append({
			'author': author,
			'content': content
		})

	# 4.返回当前页面获取的段子数据列表
	return jokes


def spider():
	jokes = []

	for page_num in range(1, 10):
		print('开始爬取第%s页数据' % page_num)

		# 爬取某一页的数据
		jokes.append(spider_page(base_url % page_num))

	# 打印爬取的数据
	for joke in jokes:
		print(joke)

	print('恭喜！爬取数据完成！')


if __name__ == '__main__':
	spider()
