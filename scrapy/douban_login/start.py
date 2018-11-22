#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: start.py 
@time: 11/15/18 21:04 
@description：方便执行 Python 文件【执行一个 Python 文件】
"""
from scrapy import cmdline

cmdline.execute('scrapy crawl douban'.split())
