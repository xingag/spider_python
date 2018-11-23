# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 存储数据
import os
from urllib import request
from scrapy.pipelines.images import ImagesPipeline
from qczj import settings


# 场景：由于系统提供的ImagesPipline不能定义子文件件目录和文件名称，这里需要自定义
class CustomImagesPipline(ImagesPipeline):

    # 发送下载图片请求之前调用
    def get_media_requests(self, item, info):
        request_objs = super(CustomImagesPipline, self).get_media_requests(item, info)

        for request_obj in request_objs:
            request_obj.item = item

        # 注意：一定要返回请求对象列表
        return request_objs

    # 图片被存储之前才会被执行
    def file_path(self, request, response=None, info=None):
        path = super(CustomImagesPipline, self).file_path(request, response, info)

        # 获取分类
        category = request.item.get('category')

        # 实际要保存的目录下
        category_path = os.path.join(settings.IMAGES_STORE, category)

        if not os.path.exists(category_path):
            os.mkdir(category_path)

        # 图片的名称  full/%s.jpg
        image_name = path.replace("full/", "")

        # 图片要保存的完成路径【注意：这里要写相对路径,相对于：settings.IMAGES_STORE这个目录】【具体查看父类返回的路径】
        image_full_path = os.path.join(category, image_name)

        return image_full_path
