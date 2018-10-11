#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: xag
@license: Apache Licence
@contact: xinganguo@gmail.com
@site: http://www.xingag.top
@software: PyCharm
@file: spider_lagou.py
@time: 2018/10/10 10:17
@description：使用selenium爬去拉勾网数据
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
from lxml import etree
import time
import re


# 封装一个爬虫类
class LagouSpider(object):

    driver_path = "/usr/local/bin/chromedriver"

    def __init__(self):
        # 初始化driver
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        # init base url
        self.base_url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        # init spider result data
        self.positions = []

    def run(self):
        """
        使用selenium取爬虫
        :return:
        """

        # 1.open the base_url
        self.driver.get(self.base_url)

        while True:

            # 2.get detail page url
            # 适用于第 1 页，第 2 页，第 3 页
            source = self.driver.page_source

            # 2.1 wait for the element had be presented【 下一页 】
            WebDriverWait(driver=self.driver, timeout=20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='pager_container']/span[last()]"))
            )

            # 3.parse the first page
            self.parse_list_page(source)

            # 4.use selenium to click the next page
            # 找到最后一个 span 标签：下一页
            next_btn = self.driver.find_element_by_xpath("//div[@class='pager_container']/span[last()]")

            # 5.perform the click method
            # 注意：确保不是在最后一页
            if "pager_next_disabled" in next_btn.get_attribute('class'):
                # 最后一页面的时候，退出应用
                self.driver.quit()
                break
            else:
                next_btn.click()

            # 6.爬一页完成，就休息 1 秒钟
            time.sleep(1)

    def parse_list_page(self, source):
        """
        解析一个页面的数据,获取详情页面的链接地址
        :param source:页面源码数据
        :return:
        """
        # 思路：通过 a 标签【class='position_link'】
        html = etree.HTML(source)
        links = html.xpath('//a[@class="position_link"]/@href')

        # 解析每一个职位的详情页面
        for link in links:
            self.request_detail_page(link)
            # 注意：爬完一个详情页面，就休息 1 秒钟
            time.sleep(1)

    def request_detail_page(self, detail_url):
        """
        打开详情页面
        :param detail_url:详情页面的 URL
        :return:
        """
        # 注意：重新切换窗口，不能覆盖之前的窗口
        # 1.保证有且只有两个窗口，第一个窗口：列表页面；第二个窗口：详情页面
        # self.driver.get(detail_url)
        self.driver.execute_script("window.open('%s')" % detail_url)
        self.driver.switch_to.window(self.driver.window_handles[1])

        # 2.获取详情页面的内容
        detail_page_source = self.driver.page_source

        # 3.解析详情页面
        self.parse_detail_page(detail_page_source)

        # 4.关闭详情页面的窗口【关闭当前页面]】，并把 driver 句柄切换回列表页面
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def parse_detail_page(self, detail_page_source):
        """
        解析详情页面
        :param detail_page_source:
        :return:
        """

        html_element = etree.HTML(detail_page_source)

        # 1.利用xpath解析页面
        # 【数据】职位名称
        position_name = html_element.xpath("//div[@class='job-name']/span/text()")[0]

        job_request_spans = html_element.xpath("//dd[@class='job_request']//span")

        # 【数据】薪水
        salary = job_request_spans[0].xpath('./text()')[0].strip()

        # 【数据】城市
        # 【注意：利用正则表达式去除特殊符号和空格】
        city_pre = job_request_spans[1].xpath('./text()')[0].strip()

        city = re.sub(r'[\s/]', '', city_pre)

        # 【数据】工作年限
        work_years_pre = job_request_spans[2].xpath('./text()')[0].strip()

        work_years = re.sub(r'[\s/]', '', work_years_pre)

        # 【数据】学历
        # 去掉空格、/ 符号
        education_pre = job_request_spans[3].xpath('./text()')[0].strip()

        education = re.sub(r'[\s/]', '', education_pre)

        # 【数据】全职
        full_time = job_request_spans[4].xpath('./text()')[0].strip()

        # 【数据】职位的详情信息 - 列表
        desc_pre = html_element.xpath('//dd[@class="job_bt"]//text()')

        # 把列表转换拼接为字符串，并去掉首位的空字符
        desc = ''.join(desc_pre).strip()

        # 【数据】公司名称
        company_name = html_element.xpath('//h2[@class="fl"]/text()')[0].strip()

        position = {
            'position_name': position_name,
            'salary': salary,
            'city': city,
            'work_years': work_years,
            'education': education,
            'full_time': full_time,
            'desc': desc,
            "company_name": company_name

        }

        print('==' * 30)
        print('爬取一个职位数据成功')
        print(position)
        print("==" * 30)

        self.positions.append(position)


if __name__ == '__main__':
    # 1.init spider instance
    spider = LagouSpider()

    # 2.start to spider
    spider.run()

    # 3.测试数据
    print(spider.positions)
