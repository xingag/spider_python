# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# 爬取到数据后，保存到Mysql数据中

import pymysql


class JianshuSpiderPipeline(object):

    def __init__(self):
        db_params = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'jianshu',
            'charset': 'utf8'
        }
    
        # 数据库【连接对象】
        self.conn = pymysql.connect(**db_params)
        
        # 数据库【游标对象】【操作数据库】
        self.cursor = self.conn.cursor()

        # sql语句
        self._sql = """
                insert into article(id,title,content,author,avatar,pubtime,article_id,origin_url) 
                values(null,%s,%s,%s,%s,%s,%s,%s)
            """

    def process_item(self, item, spider):
        # 执行sql语句
        self.cursor.execute(self._sql, (
            item['title'], item['content'], item['author'], item['avatar'], item['pubtime'], item['article_id'],
            item['origin_url']))

        # 插入到数据库中
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # 关闭游标
        self.cursor.close()


