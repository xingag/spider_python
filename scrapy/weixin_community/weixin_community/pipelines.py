# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter,JsonItemExporter


# 由于数据量相比比较大，这里使用：JsonLinesItemExporter

class WeixinCommunityPipeline(object):

    def __init__(self):
        self.fp = open('wxjc.json', 'wb')
        self.exporter = JsonLinesItemExporter(self.fp, ensure_ascii=False, encoding='utf-8')

    def process_item(self, item, spider):
        # 获取一条item，就写入一条数据到文件中
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp.close()

