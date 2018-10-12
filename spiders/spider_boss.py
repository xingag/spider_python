#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: xag
@license: Apache Licence
@contact: xinganguo@gmail.com
@site: http://www.xingag.top
@software: PyCharm
@file: spider_boss.py
@time: 2018/10/12 10:17
@description：使用selenium爬取boss直聘网并写入到csv文件中
"""

from selenium import webdriver
import re
from lxml import etree
import requests
import time
import string_utils
import csv

current_page = 1


class BossSpider(object):
    driver_path = "/usr/local/bin/chromedriver"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=BossSpider.driver_path)

        # 网页前缀
        self.domain = 'https://www.zhipin.com'

        # 爬取在首页
        self.url = 'https://www.zhipin.com/job_detail/?query=python&scity=100010000&industry=&position='

        self.positions = []

        # 保存数据到 csv 文件中【追加】
        fp = open('positions.csv', 'a', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(fp, ['company_name', 'name', 'salary', 'city', 'work_years', 'education', 'desc'])
        self.writer.writeheader()

    def run(self):
        self.driver.get(self.url)

        global current_page

        while True:

            print('爬取第%d页数据' % current_page)
            current_page = current_page + 1

            # 获取首页在源码内容
            source = self.driver.page_source

            # 爬去当前页面在数据
            self.parse_current_page(source)

            next_bt = self.driver.find_element_by_xpath("//a[@ka='page-next']")

            if 'disabled' in next_bt.get_attribute("class"):
                # 最后一页，爬取完成之后，退出应用
                self.driver.quit()
                break
            else:
                next_bt.click()

            time.sleep(1)

            # 由于boss直聘做了反爬【验证码】，这里只爬取一页数据
            break

    def parse_current_page(self, source):
        """
        解析当前页面在数据获取到详情页面在url:detail_url
        :param source:
        :return:
        """
        html = etree.HTML(source)

        # 获取到每一个职位在详情地址
        detail_urls_pre = html.xpath('//div[@class="info-primary"]//a/@href')
        # links = html.xpath("//div[@class='info-primary']//a[position()=1]/@href")

        # 利用lambda + map 对职位详情地址列表加入前缀
        detail_urls = list(map(lambda x: self.domain + x, detail_urls_pre))

        # 爬取详情页面的数据
        for detail_url in detail_urls:
            self.request_detail_page(detail_url)

            time.sleep(1)

    def request_detail_page(self, detail_url):
        """
        打开职位详情页面
        :param detail_url:
        :return:
        """

        # 1.切换到详情页面窗口
        self.driver.execute_script("window.open('%s')" % (detail_url))
        self.driver.switch_to.window(self.driver.window_handles[1])

        # 2.获取详情页面的源码数据
        page_source_detail = self.driver.page_source

        # 3.解析详情页面
        self.parse_detail_page(page_source_detail)

        # 4.关闭当前窗口并切换回列表
        self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

    def parse_detail_page(self, page_source_detail):
        """
        解析职位详情页面
        :param page_source_detail:
        :return:
        """
        html = etree.HTML(page_source_detail)

        # 数据 - 名称
        name = html.xpath('//h1/text()')[0]

        # 数据 - 公司名称
        company_name = html.xpath('//h3[@class="name"]/a[@ka="job-detail-company"]/text()')[0].strip()

        # 数据 - 薪水
        salary = html.xpath("//div[@class='name']/span[@class='badge']/text()")[0].strip()

        # 数据 - info
        infos = html.xpath("//div[@class='job-primary detail-box']/div[@class='info-primary']/p/text()")

        desc_pre = html.xpath('//div[@class="job-sec"]/div[@class="text"]/text()')

        # 每一项换行，去掉前后空格，最后去掉特殊符号
        desc = string_utils.remove_special_word('\n'.join(desc_pre).strip())

        city = infos[0]
        work_years = infos[1]
        education = infos[2]

        position = {
            'company_name': company_name,
            'name': name,
            'salary': salary,
            'city': city,
            'work_years': work_years,
            'education': education,
            'desc': desc

        }
        print('爬取一条数据成功')
        print("==" * 40)

        # 写入到csv文件中
        self.write_to_csv(position)

        self.positions.append(position)

    def write_to_csv(self, position):
        """
        把职位信息写入到 csv 文件中
        :param position:
        :return:
        """
        self.writer.writerow(position)


if __name__ == '__main__':
    # 定义爬虫类
    spider = BossSpider()

    # 开始执行爬虫
    spider.run()

    # 写入到csv文件中

    # 查看数据
    print('恭喜！爬取数据完成~')
    print(spider.positions)
