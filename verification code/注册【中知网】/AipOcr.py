#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: AipOcr.py 
@time: 1/23/19 15:19 
@description：AipOcr是OCR的Python SDK客户端，为使用OCR的开发人员提供了一系列的交互方法。
"""

from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '15474**'
API_KEY = 'VBoMZ6XUX119w***'
SECRET_KEY = 'GPvqLVeGIMOR57***'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
