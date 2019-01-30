#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: models.py 
@time: 12/15/18 23:08 
@description：数据模型
"""

from datetime import datetime
from mongoengine import StringField, URLField, IntField, Document, connect

__author__ = 'xag'

response = connect('admin', host='localhost', port=27017, username='root', password='xag')


class FilmModel(Document):
    """
    电影【模型】
    """
    title = StringField()  # 电影标题
    type = StringField()  # 电影类型
    play_num = StringField()  # 播放量
    like_num = StringField()  # 喜欢数
    img_cover = URLField()  # 封面地址
    play_address = URLField()  # 播放地址
    download_address = URLField()  # 下载地址
