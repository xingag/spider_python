# -*- coding: utf-8 -*-
"""
Created on 2021-04-08 12:03:28
---------
@summary:
---------
@author: xingag
"""

import re

import feapder
from fake_useragent import UserAgent
from feapder.db.mysqldb import MysqlDB


# 爬取数据并入库

class TophubSpider(feapder.AirSpider):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = MysqlDB()

    def start_requests(self):
        yield feapder.Request("https://tophub.today/", download_midware=self.download_midware)

    def parse(self, request, response):
        # print(response.text)
        card_elements = response.xpath('//div[@class="cc-cd"]')

        # 过滤出对应的卡片元素【什么值得买】
        buy_good_element = [card_element for card_element in card_elements if
                            card_element.xpath('.//div[@class="cc-cd-is"]//span/text()').extract_first() == '什么值得买'][0]

        # 获取内部文章标题及地址
        a_elements = buy_good_element.xpath('.//div[@class="cc-cd-cb nano"]//a')

        for a_element in a_elements:
            # 标题和链接
            title = a_element.xpath('.//span[@class="t"]/text()').extract_first()
            href = a_element.xpath('.//@href').extract_first()

            # 再次下发新任务，并带上文章标题
            yield feapder.Request(href, download_midware=self.download_midware, callback=self.parser_detail_page,
                                  title=title)

    def parser_detail_page(self, request, response):
        """
        解析文章详情数据
        :param request:
        :param response:
        :return:
        """
        title = request.title

        url = request.url

        # 解析文章详情页面，获取点赞、收藏、评论数目及作者名称
        author = response.xpath('//a[@class="author-title"]/text()').extract_first().strip()

        print("作者：", author, '文章标题:', title, "地址：", url)

        desc_elements = response.xpath('//span[@class="xilie"]/span')

        print("desc数目:", len(desc_elements))

        # 点赞
        like_count = int(re.findall('\d+', desc_elements[1].xpath('./text()').extract_first())[0])
        # 收藏
        collection_count = int(re.findall('\d+', desc_elements[2].xpath('./text()').extract_first())[0])
        # 评论
        comment_count = int(re.findall('\d+', desc_elements[3].xpath('./text()').extract_first())[0])

        print("点赞：", like_count, "收藏:", collection_count, "评论:", comment_count)

        # 插入数据库
        sql = "INSERT INTO topic(title,auth,like_count,collection,comment) values('%s','%s','%s','%d','%d')" % (
        title, author, like_count, collection_count, comment_count)

        # 执行
        self.db.execute(sql)

    def download_midware(self, request):
        # 随机UA
        # 依赖：pip3 install fake_useragent
        ua = UserAgent().random
        request.headers = {'User-Agent': ua}
        return request


if __name__ == "__main__":
    TophubSpider(thread_count=10).start()
