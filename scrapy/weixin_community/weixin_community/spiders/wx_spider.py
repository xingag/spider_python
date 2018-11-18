# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from weixin_community.items import WeixinCommunityItem


class WxSpiderSpider(CrawlSpider):
    name = 'wx_spider'
    allowed_domains = ['wxapp-union.com']
    # 起始页从第 1 页开始
    start_urls = ['http://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    # 定义规则
    rules = (
        # 列表【页面】
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d'), follow=True),

        # 详情【页面】
        Rule(LinkExtractor(allow=r'article-.+\.html'), callback='parse_detail', follow=False)
    )


    def parse_detail(self, response):
        # 标题
        title = response.xpath('//h1[@class="ph"]/text()').get()

        # p 标签元素
        author_element_p = response.xpath('//p[@class="authors"]')

        # 作者
        author = author_element_p.xpath('./a/text()').get()

        # 发布时间
        pub_time = author_element_p.xpath('./span/text()').get()

        # 内容
        content_pre = response.xpath('//td[@id="article_content"]//text()').getall()

        content = "".join(content_pre).strip()

        # 把解析完的数据交个 Pipline 去处理
        yield WeixinCommunityItem(title=title, author=author, pub_time=pub_time, content=content)
