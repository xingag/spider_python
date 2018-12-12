# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    """
    新房的数据模型【10个属性：省份、城市、小区名称、价格、几居室、面积、地址、区域、是否在售、详情页面ull】
    """
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名称
    name = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 几居室【列表】【新房可能有多个房型】
    rooms = scrapy.Field()
    # 面积
    area = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 行政区
    district = scrapy.Field()
    # 是否在售
    sale = scrapy.Field()
    # 详情页面url
    origin_url = scrapy.Field()


class ESFHouseItem(scrapy.Item):
    """
    二手房数据模型【12个属性：省份、城市、小区名称、几室几厅、楼层、朝向、年代、地址、建筑面积、总价、单价、详情页面URL】
    """
    # 省份
    province = scrapy.Field()
    # 城市
    city = scrapy.Field()
    # 小区名称
    name = scrapy.Field()
    # 几室几厅
    rooms = scrapy.Field()
    # 楼层
    floor = scrapy.Field()
    # 朝向
    toward = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 地址
    address = scrapy.Field()
    # 建筑面积
    area = scrapy.Field()
    # 总价
    price = scrapy.Field()
    # 单价
    unit = scrapy.Field()
    # 详情页面url
    origin_url = scrapy.Field()
