# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

# 作用：定义数据模型

import scrapy


class QsbkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    定义数据模型
    """
    # 段子作者
    author = scrapy.Field()

    # 段子内容
    content = scrapy.Field()
