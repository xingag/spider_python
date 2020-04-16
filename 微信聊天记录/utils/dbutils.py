#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: dbutils.py 
@time: 2020-04-11 16:57 
@description
"""

import sqlite3


class DUtil():

    def __init__(self, db_path="./weixin.db"):
        """
        数据库初始化
        """
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

    def execute(self, sql, param=None):
        """
        Sql语句，包含：增、删、改
        param：数据，可以为列表、字典，也可以为空
        """
        try:
            if param is None:
                self.cursor.execute(sql)
            else:
                if type(param) is list:
                    self.cursor.executemany(sql, param)
                else:
                    self.cursor.execute(sql, param)
            count = self.db.total_changes
            self.db.commit()
        except Exception as e:
            print(e)
            return False, e

        # 返回结果
        return True if count > 0 else False

    def query(self, sql, param=None):
        """
        查询语句
        sql：Sql语句
        param：参数，可以包含空
        retutn：成功返回True
        """
        if param is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, param)
        return self.cursor.fetchall()

    def close(self):
        """
        数据库关闭
        """
        self.cursor.close()
        self.db.close()

