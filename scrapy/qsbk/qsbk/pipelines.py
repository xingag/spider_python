# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 作用：保存数据【Json】【Xml、CSV类似，详情查看 exporters 类】

import json
from .items import QsbkItem

from scrapy.exporters import JsonLinesItemExporter

class QsbkPipeline(object):

    def __init__(self):
        # JsonLinesItemExporter 必须要以二进制的方式打开
        # 注意：以二进制的方式打开写入，不需要指定编码格式；以字符串的形式打开写入，就需要指定编码格式
        self.fp = open('duanzi.json', 'wb')

        # 定义一个 exporters
        self.exporter = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')

    def open_spider(self, spider):
        print('爬虫开始了...')

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()
        print('爬虫结束了。')
