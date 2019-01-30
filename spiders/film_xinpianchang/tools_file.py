#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: tools_file.py 
@time: 1/29/19 16:29 
@description：文件夹工具类
"""
import os


def mkdir(path):
    """
    新建一个目录
    :param path:完整路径
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)

    return path
