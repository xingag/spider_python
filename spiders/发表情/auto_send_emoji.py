#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: auto_send_emoji.py 
@time: 3/14/19 16:22 
@description：根据要求选择表情，发给微信上对应的好友或者微信群
"""

import requests
from lxml import etree
import os
import re
from utils.string_utils import *
import time
import random
from urllib import request
import itchat
from utils.chat_utils import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from queue import Queue
import threading

# pip3 install itchat

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

url = 'https://www.doutula.com/search?type=photo&more=1&keyword={}&page={}'


class Spider(object):

    def __init__(self, emoji_type, send_to):
        self.emoji_type = emoji_type
        self.send_to = send_to
        self.emojis = []

        # 起始页码
        self.start_page = 1

    def get_emojis(self):

        while True:
            current_url = url.format(self.emoji_type, self.start_page)
            resp = requests.get(current_url, headers=HEADERS)
            html_raw = etree.HTML(resp.text)

            # 判断当前是否还有emoji表情
            container_element = html_raw.xpath('//div[@class="random_picture"]//img')
            if len(container_element) > 0:
                self.emojis.extend(self.__get_current_page_emoji(html_raw))
                self.start_page += 1
            else:
                print("当前页面没有表情数据,地址是:%s" % current_url)
                break

            time.sleep(0.5)

    def __get_current_page_emoji(self, html_raw):
        """
        获取当前页面所有的emoji图片
        :param current_url:
        :return:
        """

        a_elements = html_raw.xpath('//div[@class="pic-content text-center"]/div[@class="random_picture"]/a')

        print("第%d页一共有%d张图片" % (self.start_page, len(a_elements)))

        imgs = []

        for a_element in a_elements:
            # 获取img标签【最后一个img】【存储地址】
            img_element = a_element.xpath('./img[last()]')[0]

            # 获取p标签【存储名称】
            name = a_element.xpath('./p/text()')[0]

            # xpath获取兄弟节点p
            # 表情的名称
            # name = img_element.xpath('./../p/text()')[0]

            # 表情的下载地址
            img_url = img_element.get('data-original')

            # 表情的新名词，不带后缀
            # name_new = remove_space(re.sub(r'[\?？\.，。！!\*]', '', name))

            # 注意：由于itchat没法发送带中文的文件，这里随机生成一个名称
            name_new = make_random_string(6)

            # 表情的名称，加上后缀
            # print('==' * 60)
            # print(name_new)
            # print(img_url)
            # print('==' * 60)
            img_name = name_new + os.path.splitext(img_url)[-1]

            imgs.append({
                'name': img_name,
                'url': img_url
            })

        return imgs

    def download_emojis(self, target_emoji):
        """
        下载表情
        :param target_emojis:
        :return:
        """
        # 本地保存目录
        local_img = './imgs/%s' % target_emoji.get('name')

        request.urlretrieve(target_emoji.get('url'), local_img)

        print('emoji保存本地地址:%s' % local_img)

        return local_img

    def show_image(self, filename):
        lena = mpimg.imread(filename)

        plt.imshow(lena)  # 显示图片
        plt.axis('off')  # 不显示坐标轴
        plt.show()


if __name__ == '__main__':

    # 准备调用itchat发送图片
    itchat.auto_login(hotReload=True)

    emoji_type = input('想发哪类表情:')
    send_type = input('某个人：0/群聊：1【默认是单聊】')
    send_to = input('发给谁呢？')

    if not emoji_type:
        emoji_type = '装逼'

    if not send_type:
        send_type = 0
    else:
        send_type = int(send_type)

    if not send_to:
        if send_type == 0:
            send_to = '指定经常要发送的一个人'
        else:
            send_to = '指定经常要发送的一个群'

    spider = Spider(emoji_type, send_to)

    # 带发送的表情
    local_img = None

    # 获取这种类型的所有表情
    spider.get_emojis()

    while True:

        # 从所有emoji表情中选择一张
        choose_emoji = random.sample(spider.emojis, 1)

        # 下载到本地
        local_img = spider.download_emojis(choose_emoji[0])

        # 显示图片
        spider.show_image(local_img)

        ok = input('主人满意吗：')

        if ok:
            print('好的，就发送这张表情。')
            if send_type == 0:
                send_to_person(send_to, local_img)
            else:
                send_to_group_chat(send_to, local_img)

            # 需要再发一张吗
            go_on_send = input('需要再发一张吗?')
            if go_on_send:
                continue
            else:
                print('结束了')
                break
        else:
            print('不满意，继续找一张')
            continue
