# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 为了方便使用Images Pipline，这里定义image_urls和images两个变量【必须】
class QczjItem(scrapy.Item):
    category = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
