# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from PIL import Image
import ssl


# 使用Scrapy登录豆瓣网
# 验证码识别可以通过手动输入【PIL】和自动识别

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']

    # 默认首先请求这个地址【GET】，然后把请求结果返回给parse()函数解析
    start_urls = ['https://accounts.douban.com/login']

    # 登录url
    login_url = 'https://accounts.douban.com/login'

    # 个人中心url
    person_center_url = 'https://www.douban.com/people/165725759/'

    # 编辑签名的请求地址
    edit_signature = 'https://www.douban.com/j/people/165725759/edit_signature'

    def parse(self, response):
        """
        请求后的解析
        包含两种情况：1.第一次请求start_urls；2.某一次请求不包含callback
        :param response:
        :return:
        """
        # 注意：把最后的请求解析过滤掉
        # 如果解析到相应地址不是login_url就不做处理
        if response.url != self.login_url:
            return

        print('调用parse函数，此时的url:%s' % response.url)
        form_data = {
            'source': 'index_nav',
            'redir': 'https://www.douban.com/',  # 登录后跳转到哪个界面
            'form_email': '18520876423',
            'form_password': 'Hu881025',
            # 'captcha-solution': 'chemical',  # 验证码【需要识别图片】
            # 'captcha-id': 'ysCwMdnnq8YVpDJZdfmzHu1V:en',  # 验证码ID  【每次刷新都重新生成一个，放入到input标签的name为captcha-id的value中】
            'remember': 'on',
            'login': '登录'
        }

        # 获取id为captcha-id的img标签【css方式，也可以选择用xpath】
        # 验证码图片的url
        captcha_img = response.css('img#captcha_image::attr(src)').get()

        # 注意：如果存在验证码，就识别验证码;如果没有验证码，不传入以下两个参数直接登录
        if captcha_img:
            # 手动识别验证码
            captcha = self._regonize_captcha(captcha_img)
            form_data['captcha-solution'] = captcha

            # 验证码id【每次刷新都会变化】
            captcha_id = response.xpath('//input[@name="captcha-id"]/@value').get()
            form_data['captcha-id'] = captcha_id
            print('带有验证码的参数已经补充完整，现在开始发送请求')
        else:
            print('没有验证码，现在开始发送请求')

        # 发送登录请求【POST】
        yield scrapy.FormRequest(url=self.login_url, formdata=form_data, callback=self.parse_after_login)

    def _regonize_captcha(self, image_url):
        """
        人工识别验证码【urllib+PIL】
        :param image_url:
        :return:
        """
        print('验证码的地址:%s,开始下载图片' % image_url)

        # 下载图片到本地
        request.urlretrieve(image_url, 'captcha.png')

        print('下载图片完成，开始显示图片')

        # 显示在控制台，手动输入验证码
        # 打开图片
        image = Image.open('captcha.png')
        # 展示
        image.show()

        # 提示输入验证码
        captcha = input('请输入验证码:')

        return captcha

    def parse_after_login(self, response):
        """
        登录成功之后，请求【个人中心】
        :param response:
        :return:
        """
        # 当前url
        current_page_url = response.url
        print('调用登录接口后，现在的界面是：%s' % current_page_url)
        if current_page_url == 'https://www.douban.com/':
            print('登录成功')
            # 请求个人中心的页面
            request = scrapy.Request(url=self.person_center_url, callback=self.parse_person_center)
            yield request
        else:
            print('登录失败')

    def parse_person_center(self, response):
        """
        解析个人中心页面
        :param response:
        :return:
        """
        if response.url == self.person_center_url:
            print('进入到个人中心页面了')
            ck = response.xpath('//input[@name="ck"]/@value').get()
            print('获取的ck是:%s' % ck)
            formdata = {
                'ck': ck,
                'signature': '时光如水，岁月如斯'
            }
            # 发送post请求来更改签名
            yield scrapy.FormRequest(self.edit_signature, formdata=formdata)
        else:
            print('进入个人中心页面失败')
