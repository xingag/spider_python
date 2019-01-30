#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: Film.py
@time: 1/28/19 23:33 
@description：爬取【新片场】的电影
"""
import requests
from lxml import etree
from tools_string import *
import re
import time
from models import *
import json
from tools_file import *
import asyncio
import aiohttp
from random import randint


file_path = mkdir('/Volumes/V-D/films/')


class FilmSpider(object):
    def __init__(self):
        self.main_url = 'http://www.xinpianchang.com/channel/index/type-0/sort-like/duration_type-0/resolution_type-/page-{}'
        self.download_url = 'https://openapi-vtom.vmovier.com/v3/video/{}?expand=resource,resource_origin?'

        self.headers = {
            'Origin': 'http://www.xinpianchang.com',
            'Host': 'www.xinpianchang.com',
            'Cookie': 'Device_ID=5c1912ff76a7a; _ga=GA1.2.1413678234.1545147137; UM_distinctid=167c1f258ec1c0-0d7191732886e3-10306653-1aeaa0-167c1f258edd10; zg_did=%7B%22did%22%3A%20%22167c1f263928f9-06bcbc1794cc9a-10306653-1aeaa0-167c1f263931277%22%7D; Authorization=56274F34526E804B1526E84CEC526E88C53526E8426B8C51016F; PHPSESSID=f98360flunqcekg9uk7rokpr4e; SERVER_ID=b52601c8-285bdd26; ts_uptime=1499141967; Hm_lvt_dfbb354a7c147964edec94b42797c7ac=1547604937,1548406735; _gid=GA1.2.1397121514.1548685414; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2210000837%22%2C%22%24device_id%22%3A%22167c1f2589dbc3-0f4517a7848615-10306653-1764000-167c1f2589ea1d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22167c1f2589dbc3-0f4517a7848615-10306653-1764000-167c1f2589ea1d%22%7D; Hm_lvt_31eb3c3fd6ffa0c0374d37ca2acb6f3b=1548685422; Hm_lpvt_31eb3c3fd6ffa0c0374d37ca2acb6f3b=1548685422; CNZZDATA1262268826=17098371-1545143244-%7C1548744894; _gat=1; channel_page=apY%3D; zg_c9c6d79f996741ee958c338e28f881d0=%7B%22sid%22%3A%201548744923.114%2C%22updated%22%3A%201548746725.644%2C%22info%22%3A%201548406734894%2C%22cuid%22%3A%2010000837%7D; Hm_lpvt_dfbb354a7c147964edec94b42797c7ac=1548746726; responseTimeline=169; cn_1262268826_dplus=%7B%22distinct_id%22%3A%20%22167c1f258ec1c0-0d7191732886e3-10306653-1aeaa0-167c1f258edd10%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201548736541%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201548736541%7D%2C%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201548746745%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201548746745%7D',
            'Referer': 'http://www.xinpianchang.com/channel/index/sort-like?from=tabArticle',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

        # 所有电影
        self.films = []

    def start(self, target_url):

        req = requests.get(target_url, headers=self.headers)
        html_element = etree.HTML(req.text)

        film_elements = html_element.xpath('//ul[@class="video-list"]/li')

        for film_element in film_elements:
            # 电影标题
            title = film_element.xpath('.//div[@class="video-con-top"]/a/p/text()')[0]

            # 电影类型
            type = remove_space('/'.join(
                film_element.xpath('.//div[@class="new-cate"]/span[@class="fs_12 fw_300 c_b_9"]/text()')))

            # 播放量和点赞数
            play_num = film_element.xpath('.//span[@class="fw_300 icon-play-volume"]/text()')[0]

            like_num = film_element.xpath('.//span[@class="fw_300 c_b_9 icon-like"]/text()')[0]

            # 封面图片
            img_cover = film_element.xpath('.//a[@class="video-cover"]/img/@_src')[0]

            # id
            id = film_element.xpath('./@data-articleid')[0]

            # 播放地址
            play_address = 'http://www.xinpianchang.com/a{}'.format(id)

            # 下载地址【关键】
            download_address = self.get_download_address(play_address)

            # 过滤不正常的数据
            if download_address:
                film_data = {
                    'title': title,
                    'type': type,
                    'play_num': play_num,
                    'like_num': like_num,
                    'img_cover': img_cover,
                    'play_address': play_address,
                    'download_address': download_address
                }

                model = FilmModel(**film_data)
                try:
                    model.save()
                    print('插入一条电影数据成功')
                    self.films.append(film_data)
                except Exception as e:
                    print('插入数据异常')
                    print(e)

                time.sleep(1)
            else:
                print('脏数据，播放地址：%s' % play_address)
        # =================================================
        time.sleep(2)

    def get_download_address(self, play_address):
        """
        获取下载地址
        :param play_address:
        :return:
        """
        # a10370525
        # https://openapi-vtom.vmovier.com/v3/video/5C4D33C0A4D57?expand=resource,resource_origin?

        # a10355437
        # https://openapi-vtom.vmovier.com/v3/video/5C28724081430?expand=resource,resource_origin?

        req = requests.get(play_address, headers=self.headers)

        # 隐藏在源码中
        # 注意：有部分视频源有问题，这里要过滤掉
        vid_pre = re.findall(r'vid: "(.*)",', req.text)

        # 下载请求地址
        download_url_pre = "" if len(vid_pre) == 0 else self.download_url.format(vid_pre[0])

        if not download_url_pre:
            return ""

        # 注意：这里要不能共用上面的Header，不然会请求不到数据
        download_headers = {
            'Origin': 'http://www.xinpianchang.com',
            'Referer': 'http://www.xinpianchang.com/a99200?from=ArticleList',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

        # Get请求获取到视频数据
        download_resp = json.loads(requests.get(download_url_pre, headers=download_headers).text)

        # 获取真实的下载地址
        if 'resource' in download_resp['data']:
            download_url = download_resp['data']['resource']['default']['url']
        else:
            download_url = ''

        print('当前播放地址是:%s，下载地址：%s' % (play_address, download_url))

        return download_url


async def download_a_film(title, download_address):
    """
    下载一部电影
    :param title:
    :param download_address:
    :return:
    """
    print('下载标题：%s,下载地址:%s' % (title, download_address))
    if not download_address:
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(download_address) as response:
            # 注意：由于标题中包含空格、/等特殊符号，这里要做一些处理
            file_full_path = file_path + title.replace(" ", "").replace("/", "") + ".mp4"
            video = await response.read()
            with open(file_full_path, 'wb') as file:
                file.write(video)
                print('电影：%s下载成功' % title)


if __name__ == '__main__':
    # 爬取1-100页的电影数据
    filmSpider = FilmSpider()
    target_urls = list(map(lambda x: filmSpider.main_url.format(x), range(1, 101)))
    for target_url in target_urls:
        filmSpider.start(target_url)

    print('一共有%d部电影,开始下载视频...' % len(filmSpider.films))

    loop = asyncio.get_event_loop()

    tasks = []

    for film in filmSpider.films:
        tasks.append(download_a_film(film.get('title'), film.get('download_address')))

    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    print('下载完成')
