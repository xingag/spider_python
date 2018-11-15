# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList, Selector


# 使用 scrapy 爬取糗事百科

class SpiderQsbkSpider(scrapy.Spider):
    name = 'spider_qsbk'
    allowed_domains = ['qiushibaike.com']
    start_urls = ['https://www.qiushibaike.com/text/page/1/']
    base_domain = "https://www.qiushibaike.com"

    def parse(self, response):
        """
        对 Download 下载回来的数据进行解释
        :param response: HtmlResponse
        :return:
        """

        # 1.利用 Xpath 获取所有的段子【divs】
        duan_zi_divs = response.xpath('//div[@id="content-left"]/div')

        # items = []

        # 2.遍历出段子进行解析
        for duan_zi_div in duan_zi_divs:
            # 2.1 获取作者
            author = duan_zi_div.xpath(".//h2/text()").get().strip()

            # 2.2 获取段子内容
            content_pre = duan_zi_div.xpath(".//div[@class='content']//text()").getall()  # 列表
            content = "".join(content_pre).strip()

            # 2.3 组装成一个数据模型
            item = QsbkItem(author=author, content=content)

            # 2.4 以生成器的方式传给 piplines 管道处理
            yield item

        # 查找下一页的链接地址
        next_url = None
        try:
            next_url = self.base_domain + response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        except:
            pass

        # 如果找不到下一页【最后一页】，就直接返回
        if not next_url:
            return
        else:
            # 执行下一页
            yield scrapy.Request(next_url, callback=self.parse)
