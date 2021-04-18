#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: test.py 
@time: 2021/4/8 下午12:26 
@description：TODO
"""

from fake_useragent import UserAgent

ua = UserAgent().random
print(ua)