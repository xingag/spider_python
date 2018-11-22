# 使用scrapy登录豆瓣网
### 准备

```
scrapy startproject douban_login
cd douban_login
scrapy genspider douban "douban.com"
```



### 配置

配置 `settings.py` 文件

编写 `start.py` 文件，利用 `cmdline` 快速指定爬虫代码



### 开发

场景：使用 `scrapy` 登录豆瓣网，然后到个人中心页面，修改个性签名

请求：初始请求【GET】、登录请求【POST】、个人中心请求【GET】、修改签名请求【POST】

注意：

1. 初始请求的地址是：`start_urls`
2. 使用 `urllib + PIL` 下载验证码图片，并人工识别验证码【可以付费调用识别验证码的接口】
3. `captcha-id` 和 `ck` 两个请求参数都在源码中的某个元素里



### 运行

运行 `start.py` 

