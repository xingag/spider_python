# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 文章详情Item
class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    # 文章id
    article_id = scrapy.Field()
    # 原始的url
    origin_url = scrapy.Field()

    # 作者
    author = scrapy.Field()

    # 头像
    avatar = scrapy.Field()

    # 发布时间
    pubtime = scrapy.Field()
