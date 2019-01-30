#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: tools_string.py 
@time: 1/28/19 23:50 
@description：TODO
"""

import random
import string


def remove_space(str):
    return ''.join(str.split(' ')).replace("\t", '').replace("\n", '')


def make_random_string(num):
    """
    生成随机字符串
    :param num:
    :return:
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, num))
