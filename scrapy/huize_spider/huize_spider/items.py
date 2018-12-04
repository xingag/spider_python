# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuizeSpiderItem(scrapy.Item):
    title = scrapy.Field()
    sales = scrapy.Field()
    tips = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
