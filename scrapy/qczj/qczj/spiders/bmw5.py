# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from qczj.items import QczjItem


# 爬取汽车之家宝马5系的数据，下载原图

class Bmw5Spider(CrawlSpider):
    name = 'bmw5'
    allowed_domains = ['car.autohome.com.cn']

    # 宝马5系（进口）汽车系列图地址
    start_urls = ['https://car.autohome.com.cn/pic/series/202.html']

    rules = {
        # follow=True:接下来解析第二页、第三页、、、
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/202-.+'), callback="parse_page", follow=True)
    }

    def parse_page(self, response):
        """
        解析满足rules的url【更多图片页面】  https://car.autohome.com.cn/pic/series/202-1-p1.html
        :param response: 
        :return:
        """
        # 1.获取类别【可以通过scrapy shell url局部测试，不需要运行整个项目】
        category = response.xpath('//div[@class="uibox"]/div[1]/text()').get()

        # 2.图片
        # 注意：xpath 包含语法【同样可以通过scrapy shell来局部测试正确性】
        srcs = response.xpath('//div[contains(@class,"uibox-con")]//li//img/@src').getall()

        # 3.1 对缩略图的地址补全
        # 3.2 转换缩略图的url为高清图片的url
        srcs = list(map(lambda x: response.urljoin(x).replace("t_", ""), srcs))

        item = QczjItem(category=category, image_urls=srcs)

        print("爬完页面：%s，类别：%s" % (response.url, category))

        yield item
