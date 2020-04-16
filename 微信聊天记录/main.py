#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: main.py 
@time: 2020-04-11 17:12 
@description：统计群聊信息及获取最活跃的用户
"""

import jieba
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot as driver
from wordcloud import WordCloud

from utils.dbutils import *
from utils.string_utils import *


# 依赖：pip3 install pyecharts -U
# pip3 install snapshot-selenium
# 欢迎关注微信公众号：AirPython，获取自动化、爬虫实战干货


class WeiXin(object):

    def __init__(self, chatroom_name):
        # 微信数据库初始化，包含数据库和游标对象
        self.db = DUtil()
        self.chatroom_name = chatroom_name

        # 发言排名靠前的群友
        self.top_data = []

        self.top_num = 15

    def run(self):
        # 0、创建一个群聊
        self.__create_top_table()

        # 1、通过群聊名称，从rcontact表中查询出群聊的id
        chatroom_id = self.__get_chartroom_id()

        # 2、查询群聊消息
        word = self.__query_chatroom_msgs(chatroom_id)

        # 3、根据群聊消息，生成词云
        self.generate_wordcloud(word)

        # 4、查看排名前10名
        self.get_top_partner()

        # 5、画图
        self.draw_image()

    def __get_chartroom_id(self):
        """
        获取群聊的id
        :return:
        """
        res = self.db.query('select username from rcontact where nickname=?;', (self.chatroom_name,))

        # 群聊id
        chatroom_id = res[0][0]

        return chatroom_id

    def __query_chatroom_msgs(self, chatroom_id):
        """
        查询群聊消息
        :param chatroom_id:
        :return:
        """
        # message表：聊天记录表
        # isSend=0:对方发送的；isSend=1：自己发送的
        sql = "SELECT content FROM message WHERE talker='{}' and isSend=0".format(chatroom_id)
        result = self.db.query(sql)

        # 定义一个列表，加入所有要统计的数据
        msg_pre = []

        # 词云列表
        words = []

        # 循环遍历消息
        for item in result:
            # 过滤数据
            if not item or not item[0] or item[0].find('xml') != -1 or item[0].find('sysmsg') != -1 or item[0].find(
                    '<msg>') != -1 or item[0].find('chatroom') != -1 or item[0].find('weixinhongbao') != -1:
                continue
            # 过滤掉自己发送的内容，不包含：
            temps = item[0].split(':')
            if len(temps) < 2:
                # print('自己发送的内容:' + item[0])
                continue
            # 每一条聊天记录，过滤掉发送者，只保留消息正文
            # 发送者
            send_from = item[0].split(':')[0]
            # 发送内容
            send_msg = "".join(item[0].split(':')[1:]).strip().replace("\"", "")

            if len(send_msg) > 200:
                continue

            msg_pre.append((send_from, send_msg))

            words.append(item[0].split(':')[-1])

        # 把要统计的数据，插入到top表中
        self.db.execute("insert into top(uid,name,msg) values (NULL,?,?);", msg_pre)

        # 合成一个字符串
        words = "\n".join(words)

        # 分词
        return " ".join(jieba.cut(words, cut_all=True))

    def __create_top_table(self):
        """
        创建Top表
        :return:
        """
        # 创建Top表，如果存在就不重新创建
        result = self.db.execute(
            "CREATE TABLE IF NOT EXISTS top(uid integer primary key,name varchar(200),msg varchar(200))")

    def generate_wordcloud(self, word):
        """
        生成词云
        :param word:词云内容
        :return:
        """

        img = WordCloud(font_path="./DroidSansFallbackFull.ttf", width=2000, height=2000,
                        margin=2, collocations=False).generate(word)
        plt.imshow(img)
        plt.axis("off")
        plt.show()
        img.to_file("{}.png".format("群聊"))

    def get_top_partner(self):
        """
        排名前十的成员
        :return:
        """
        sql = "SELECT name as 姓名,COUNT(*) as times FROM top GROUP BY name ORDER BY times DESC limit %d;" % self.top_num
        result = self.db.query(sql)

        for item in result:
            # 用户id
            id = item[0]
            # 发言次数
            count = item[1]

            # 获取用户的昵称，即：微信昵称
            username = self.get_username(id)

            self.top_data.append({
                'username': username,
                'count': count
            })

    def get_username(self, id):
        """
        查询获取用户的昵称
        :param id:
        :return:
        """
        # 从表rcontact中，查询到用户的昵称
        result = self.db.query('select * from rcontact where username="%s";' % id)
        return result[0][4]

    def draw_image(self):
        """
        画图
        :return:
        """
        usernames = []
        counts = []
        for user in self.top_data:
            # 去除昵称中的特殊符号
            usernames.append(get_ava_string(user.get('username').strip())[0:8])
            counts.append(user.get('count'))

        def bar_chart() -> Bar:
            c = (
                Bar()
                    .add_xaxis(usernames)
                    .add_yaxis("活跃度", counts)
                    .reversal_axis()
                    .set_series_opts(label_opts=opts.LabelOpts(position="right"))
                    .set_global_opts(title_opts=opts.TitleOpts(title="最活跃的%d个小伙伴" % self.top_num))
            )
            return c

        # 需要安装 snapshot-selenium 或者 snapshot-phantomjs
        make_snapshot(driver, bar_chart().render(), "bar.png")


if __name__ == '__main__':
    # 群聊名字
    chatname = 'AirPython 高质量副业交流群'
    wx = WeiXin(chatname)
    wx.run()
