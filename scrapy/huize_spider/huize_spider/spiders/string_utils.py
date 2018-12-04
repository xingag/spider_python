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
@time: 12/4/18 19:52 
@description：TODO
"""


def remove_space_words(source):
    """
    去掉字符串中的特殊空格，包含\n、\t、\xa0
    :param source:
    :return:
    """
    result = "".join(source.split())
    return result
