#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: nzj.py 
@time: 1/11/19 16:00 
@description：看看大家今年大家都有年终奖吗？
"""

import json
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 文件名称
filename = 'comments.txt'

# 总共的评论数目
comment_count = 0


def response(flow):
    request = flow.request
    response = flow.response

    global comment_count

    # 请求的地址
    request_url = request.url

    # 筛选
    if 'comments' in request_url and 'zsxq' in request_url:
        # 返回的内容
        response_content = response.content.decode('utf-8')
        print('请求地址:' + request_url)
        print('请求方法：' + str(request.method))
        print('参数:' + str(request.data))

        obj = json.loads(response_content)

        comments = obj['resp_data']['comments']

        # 最后一页
        if len(comments) == 0:
            print('一共有%d个球友发表了自己的看法' % comment_count)

            # 生成词云
            generate_word_cloud()

        else:
            comment_count += len(comments)
            for comment in comments:
                comment_content = comment['text']
                with open(filename, 'a') as f:
                    f.write(comment_content + '\n')


def generate_word_cloud():
    """
    生成词云
    :return:
    """
    with open(filename, 'r') as f:
        word_content = f.read()

        # 使用jieba去分割
        wordlist = jieba.cut(word_content, cut_all=True)

        wl_space_split = " ".join(wordlist)

        font = r'/Users/xingag/Library/Fonts/SimHei.ttf'

        wordcloud = WordCloud(font_path=font, width=1080, height=1920, margin=2).generate(wl_space_split)

        # 显示图片
        plt.imshow(wordcloud)
        plt.axis("off")

        # 按照设置保存到本地文件夹
        wordcloud.to_file("./output.png")
