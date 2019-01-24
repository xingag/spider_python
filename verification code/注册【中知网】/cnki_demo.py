#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: xag 
@license: Apache Licence  
@contact: xinganguo@gmail.com 
@site: http://www.xingag.top 
@software: PyCharm 
@file: cnki_demo.py
@time: 1/23/19 15:44 
@description：[中国知网注册]
"""
from PIL import Image
from selenium import webdriver
from file_tools import *
from AipOcr import *
import requests
import time
import json


class Cnki_Spider(object):
    driver_path = "/usr/local/bin/chromedriver"

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=Cnki_Spider.driver_path)

        # 包含验证码的页面的截图
        self.screen_shot_file_name = "screen_shot.png"

        # 验证码图片
        self.code_file_name = "image_code.png"

        # 注册主页面
        self.main_url = 'http://my.cnki.net/elibregister/commonRegister.aspx'

        # 待注册的内容
        # 昵称
        self.username = 'xingag2311'
        # 密码
        self.password = 'Hu9012782'
        # 邮箱地址
        self.email = '809900227@qq.com'

    def run(self):
        # 1.打开注册页面【包含验证码】
        self.driver.get(self.main_url)

        source = self.driver.page_source

        # 2.验证码图片、验证码输入框
        code_input_element = self.driver.find_element_by_id('txtOldCheckCode')
        code_img_element = self.driver.find_element_by_id('checkcode')


        # 外面容器
        container_element = self.driver.find_element_by_id('form1')

        # 3.获取验证码、填入输入框、点击外面
        # 如果没有出现出错的提示tips，就代表输入验证码成功
        while True:

            code = self.get_code().strip()

            error_tips_element = self.driver.find_element_by_id('span_oldcheckcode')

            print('验证码为:%s' % code)
            code_input_element.clear()
            code_input_element.click()
            code_input_element.send_keys(code)

            # 点击外围的容器，判断验证码是否输入正确
            container_element.click()

            # 显示了错误信息：验证码输入错误
            if error_tips_element.text:
                time.sleep(2)
                print('验证码验证失败，点击验证码图片')

                # 点击验证码图片，重新加载验证码
                code_img_element.click()
                continue
            else:
                print('验证码验证成功')
                break

        # 3.注册
        self.register(code)

    def get_code(self):

        # 1.截图并保存到本地
        self.driver.get_screenshot_as_file('./%s' % self.screen_shot_file_name)

        # 2.打开文件
        screenshot_image = Image.open('./%s' % self.screen_shot_file_name)

        # 3.设置要裁剪的区域（验证码所在的区域）
        code_box = (899, 819, 1048, 883)

        # 4.截图：生成只有验证码的图片
        code_image = screenshot_image.crop(code_box)

        # 5.保存到本地
        code_image.save("./%s" % self.code_file_name)

        # 6.以byte读取图片
        image = get_file_content("./%s" % self.code_file_name)

        # 7.使用百度OCR识别验证码
        result = client.basicAccurate(image)

        print(result)

        # 识别的文字内容
        word_result = result.get('words_result')[0].get('words')

        return word_result

    def register(self, code):
        # 用户名输入框
        username_input_element = self.driver.find_element_by_id('username')

        # 密码输入框
        password_input_element = self.driver.find_element_by_id('txtPassword')

        # 邮箱输入框
        txtEmail_input_element = self.driver.find_element_by_id('txtEmail')

        # 注册按钮
        submit_btn_element = self.driver.find_element_by_id('ButtonRegister')

        username_input_element.send_keys(self.username)
        password_input_element.send_keys(self.password)
        txtEmail_input_element.send_keys(self.email)

        submit_btn_element.click()


if __name__ == '__main__':
    spider = Cnki_Spider()
    spider.run()
