# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from huize_spider.items import HuizeSpiderItem
from .string_utils import remove_space_words


# 使用 CrawlSpider 爬取某保险网的数据

class HuizeSpider(CrawlSpider):
    name = 'huize'
    allowed_domains = ['huize.com']
    start_urls = ['http://huize.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.*http://www.huize.com/product/ins-.*'), callback=None, follow=False),
        Rule(LinkExtractor(allow=r'.*http://www.huize.com/product/detail-.*'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        # 标题
        title = response.xpath('//h2[@class="product-title f30"]/text()').get().strip()

        # 销量
        sales = response.xpath('//p[@class="count-item fc6"]/text()').get().strip()

        # 保险特色
        # 去掉特殊空格符号
        tips = remove_space_words("、".join(response.xpath('//li[@class="ensure-support-item"]/text()').getall()))

        # 价格
        price = response.xpath('//span[@class="product-price"]/i[@class="preminum-result"]/text()').get()+" 元"

        item = HuizeSpiderItem(title=title, sales=sales, tips=tips, price=price, url=response.url)

        yield item
