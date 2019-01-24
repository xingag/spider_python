#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: file_tools.py 
@time: 1/23/19 15:41 
@description：TODO
"""


def get_file_content(filePath):
    """
    读取文件
    :param filePath: 文件路径
    :return: byte类型 <class 'bytes'>
    """
    with open(filePath, 'rb') as fp:
        return fp.read()
