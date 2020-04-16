#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: StringUtils.py 
@time: 2020-04-11 18:39 
@description：TODO
"""
import re


def get_ava_string(str):
    """
    去掉特殊符号，保留正常内容
    :param str:
    :return:
    """
    return re.sub(u"([^ \u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", str)
