#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: xag
@license: Apache Licence
@contact: xinganguo@gmail.com
@site: http://www.xingag.top
@software: PyCharm
@file: gps_utils.py
@time: 2019-11-17 10:34
@description：TODO
"""

import math


def gps_to_dms(gps_data):
    """
    坐标转为度、分、秒(double)
    116.397451
    :param gps_data:
    :return:
    """
    # 度：向下取整
    gps_degree = math.floor(gps_data)

    gps_data_temp1 = (gps_data - gps_degree) * 60

    # 分
    gps_minute = math.floor(gps_data_temp1)

    gps_data_temp2 = gps_data_temp1 - gps_minute

    # 秒,取小数点后4位
    gps_second = round(gps_data_temp2 * 60, 2)

    # 注意：秒必须转换为整形
    result = ((gps_degree, 1), (gps_minute, 1), (int(gps_second * 100), 100))

    return result


def dms_to_gps(dms_data):
    """
    度、分、秒转为坐标值(double)
    :param dms_data:
    :return:
    """
    data1 = dms_data[0][0] / dms_data[0][1]

    data2 = dms_data[1][0] / dms_data[1][1] / 60

    data3 = dms_data[2][0] / dms_data[2][1] / 3600

    result = round(data1 + data2 + data3,6)

    return result
