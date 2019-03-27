#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: string_utils.py 
@time: 3/15/19 10:36 
@description：TODO
"""

import random
import string


def remove_space(source):
    """
    去除空格
    :param source:
    :return:
    """
    return "".join(source.split(' '))



def make_random_string(num):
    """
    生成随机字符串
    :param num:
    :return:
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, num))