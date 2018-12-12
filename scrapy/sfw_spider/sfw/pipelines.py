# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import JsonLinesItemExporter
from .items import NewHouseItem, ESFHouseItem


class SfwPipeline(object):

    def __init__(self):
        self.fp_new_house = open('new_house.json', 'wb')
        self.fp_esf_house = open('esf_house.json', 'wb')

        self.exporter_new_house = JsonLinesItemExporter(self.fp_new_house, ensure_ascii=False)
        self.exporter_esf_house = JsonLinesItemExporter(self.fp_esf_house, ensure_ascii=False)

    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            print('写入一条新手房数据')
            self.exporter_new_house.export_item(item)
        else:
            print('写入一条二手房数据')
            self.exporter_esf_house.export_item(item)
        return item

    def close_spider(self, spider):
        self.fp_new_house.close()
        self.fp_esf_house.close()
