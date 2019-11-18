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
@time: 2019-11-16 10:12
@description：修改图片地理位置
"""

import requests
import time
from PIL import Image
import piexif
import json
from gps_utils import *
from position_utils import *


# 依赖：pip3 install piexif

class Exif():
    def __init__(self):
        self.time = '2019:11:17 14:13:22'

        # 地理编码（地址转为经纬度）
        self.url_geo = 'https://restapi.amap.com/v3/geocode/geo'

        # 逆地理编码（经纬度转为地址）
        self.url_regeo = 'https://restapi.amap.com/v3/geocode/regeo?parameters'

        # key
        self.ak = '你的ak'

        # 数字签名
        self.sign = '你的sign'

    def read_image(self, image_path):
        """
        开始处理图片
        exifread:读取图片属性
        :return:
        """
        exif_dict = piexif.load(image_path)

        if exif_dict['GPS']:

            # 纬度
            gps_lati_pre = exif_dict['GPS'][2]

            gps_lati = dms_to_gps(gps_lati_pre)

            # 经度
            gps_long_pre = exif_dict['GPS'][4]
            gps_long = dms_to_gps(gps_long_pre)

            # GPS坐标转为高德坐标
            lng, lat = wgs84togcj02(gps_long, gps_lati)

            # print(lng, lat)

            print(f"原图地理位置如下\n经度：{lng}\n纬度:{lat}\n")

            return f'{lng}, {lat}'
        else:
            print(f'抱歉！这张图片不包含地理位置！')

    def current_time(self):
        """
        获取当前时间
        :return:
        """
        time_now = time.strftime('%Y:%m:%d %H:%M:%S', time.localtime(time.time()))

        result = bytes(time_now, encoding='utf-8')

        return result

    def str_to_bytes(self, str_content):
        """
        字符串转bytes
        :return:
        """
        return bytes(str_content, encoding='utf-8')

    def is_image(self, filename):
        """
        判断文件是否是一张图片
        :param filename:
        :return:
        """
        file_suffix = filename.split('.')[-1]

        if file_suffix == 'jpg' or file_suffix == 'png':
            return True
        else:
            return False

    def write_image(self, image_path, gps_long, gps_lati):
        """
        修改文件夹下所有文件的属性
        :param image_path: 文件夹路径
        :return:
        """
        # 读取图片
        img = Image.open(image_path)

        try:
            exif_dict = piexif.load(img.info['exif'])
        except:
            print('加载文件地理位置异常！')
            return

        # 修改地理位置
        # GPS GPSLatitudeRef:N
        # GPS GPSLatitude:[22, 32, 189/20]
        # GPS GPSLongitudeRef:E
        # GPS GPSLongitude:[114, 1, 689/20]
        exif_dict['GPS'][2] = gps_to_dms(gps_lati)
        exif_dict['GPS'][4] = gps_to_dms(gps_long)

        exif_bytes = piexif.dump(exif_dict)

        # 写入到新的图片中去
        img.save(image_path, 'jpeg', exif=exif_bytes)

    def get_address_by_location(self, location):
        """
        通过经纬度拿到地理位置
        :param location:
        :return:
        """
        params = {
            'key': self.ak,
            'location': location,
            'sig': self.sign
        }

        resp = json.loads(requests.get(url=self.url_regeo, params=params).text)

        if resp and resp.get('regeocode') and resp.get('regeocode').get('formatted_address'):
            address = resp.get('regeocode').get('formatted_address')
            print(f'原图的拍摄地址为:{address}\n')
        else:
            print('api解析地址出错，请检查ak！\n')

    def get_location_by_address(self, city, address):
        """
        通过地理位置到拿到经纬度
        地理编码：https://lbs.amap.com/api/webservice/guide/api/georegeo/
        :param address:
        :return:
        """
        params = {
            'key': self.ak,
            'city': city,
            'address': address,
            'sig': self.sign
        }

        resp = json.loads(requests.get(url=self.url_geo, params=params).text)

        # 获取坐标地址
        if resp and len(resp.get('geocodes')) >= 1 and resp.get('geocodes')[0].get('location'):
            location = resp.get('geocodes')[0].get('location')
            gps_data = location.split(',')

            # 得到经度和纬度
            gps_long = float(gps_data[0])
            gps_lati = float(gps_data[1])

            return gps_long, gps_lati
        else:
            print('api解析地址出错，请检查ak！')
            return None


if __name__ == '__main__':
    exif = Exif()

    image_path = './WechatIMG1439.jpeg'

    # 1、读取原图的属性
    location = exif.read_image(image_path)

    if location:
        # 2、原图的详细地址
        exif.get_address_by_location(location)

        # 3、输入地址（市+目的地，例如：深圳莲花山公园）
        city = input('请输入定位城市(例如：深圳)：')
        address = input('请输入具体的定位地址(例如：莲花山公园)：')

        if address:
            # 通过地址拿到坐标地址
            location = exif.get_location_by_address(city, address)

            if location:
                # 4、修改图片属性,写入经度和纬度
                exif.write_image(image_path, location[0], location[1])
                print('修改图片地理成功！')
        else:
            print('请先输入具体地址！')
