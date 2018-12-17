#!/usr/bin/env python
# encoding: utf-8

"""
    @version: v1.0
    @author: xag
    @license: Apache Licence
    @contact: xinganguo@gmail.com
    @site: http://www.xingag.top
    @software: PyCharm
    @file: spider_china_weather.py
    @time: 2018/9/20 0:04
    @description：利用requests + bs4 + html5lib + pyecharts爬取中国天气网的最低气温并可视化
    @install:# pip install pyecharts/pyecharts-snapshot
    """

import requests
from bs4 import BeautifulSoup
import time
from pyecharts import Bar


# 一共8个区域，包含：华北、东北、华东、华中、华南、西北、西南、港澳台
# 华北
url_hb = 'http://www.weather.com.cn/textFC/hb.shtml'

# 东北
url_db = 'http://www.weather.com.cn/textFC/db.shtml'

# 华东
url_hd = 'http://www.weather.com.cn/textFC/hd.shtml'

# 华中
url_hz = 'http://www.weather.com.cn/textFC/hz.shtml'

# 华南
url_hn = 'http://www.weather.com.cn/textFC/hn.shtml'

# 西北
url_xb = 'http://www.weather.com.cn/textFC/xb.shtml'

# 西南
url_xn = 'http://www.weather.com.cn/textFC/xn.shtml'

# 港澳台【比较特殊】
url_gat = 'http://www.weather.com.cn/textFC/gat.shtml'

url_areas = [url_hb, url_db, url_hd, url_hz, url_hn, url_xb, url_xn, url_gat]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Referer': 'http://www.weather.com.cn/textFC/hb.shtml'
}

# 数据【城市+最低温度】列表
ALL_DATA = []


def parse_page(url):
    """
        解析一个区域：华北、东北、华东等
        :param url:
        :return:
        """
    response = requests.get(url, headers=HEADERS)
    
    # 1.获取页面的原始html数据
    text = response.content.decode('utf-8')
    
    
    # 注意：港澳台中香港的table标签没有正确的关闭，使用lxml解析器不能正确解析。需要使用html5lib【容错性强】去自动补全代码，然后进行解析
    soup = BeautifulSoup(text, 'html5lib')
    
    div_conMidtab = soup.find('div', class_='conMidtab')
    
    # 3.获取所有的table子Tag【天气信息都保存在table标签下面】
    tables = div_conMidtab.find_all('table')
    
    # 4.遍历片区下面的省份
    for table in tables:
        # 4.1过滤掉表头的两个tr数据
        trs = table.find_all('tr')[2:]
        
        # 5.遍历省份下面的市区
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            
            # 5.1 城市名称【第 1 个td标签】
            # 注意：一个省份第一个城市取第 2 个td标签；其余城市取第 1 个td标签
            city_td = tds[1] if index == 0 else tds[0]
            
            city = list(city_td.stripped_strings)[0]
            
            # 5.2 最低气温【倒数第 2 个td标签】
            temp_low_td = tds[-2]
            
            temp_low = list(temp_low_td.stripped_strings)[0]
            
            ALL_DATA.append({"city": city, "temp_low": int(temp_low)})


def spider():
    for index, url in enumerate(url_areas):
        print('开始爬取第{}个区域'.format(index + 1))
        parse_page(url)
        time.sleep(1)


def analysis_data():
    """
        分析爬下来的数据
        :return:
        """
    
    # 1.默认的排序方式是升序【通过最低气温进行排序】
    ALL_DATA.sort(key=lambda data: data['temp_low'])
    
    # 2.获取前面10条数据
    top_10 = ALL_DATA[:10]
    
    return top_10


def show_with_chart(top_10):
    """
        把最低的十个城市和温度生成饼状图
        :param top_10:
        :return:
        """
    # 1.获取城市列表
    citys = list(map(lambda item: item['city'], top_10))
    
    # 2.最低温度列表
    temp_lows = list(map(lambda item: item['temp_low'], top_10))
    
    # 3.生成饼状图并写入到html文件中
    bar = Bar("最低气温排行榜")
    
    bar.add("最低温度", citys, temp_lows)
    
    # 渲染
    bar.render('temperature.html')


if __name__ == '__main__':
    # 1.爬取数据
    spider()
    
    # 2.分析数据
    top_10 = analysis_data()
    
    # 3.使用pyecharts生成饼状图
    show_with_chart(top_10)
