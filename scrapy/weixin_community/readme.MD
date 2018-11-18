# 使用 `CrawlSpider` 爬取微信小程序论坛
1. 创建一个项目

   ```
   scrapy startproject weixin_community
   ```

2. 创建一个爬虫

   ```
   # 先进入文件夹中
   cd weixin_community
   
   # 创建一个爬虫
   scrapy genspider -t crawl wx_spider "wxapp-union.com"
   ```

3. 使用 `Pycharm` 打开项目

4. 设置 `setting.py` 文件

   ```
   ROBOTSTXT_OBEY = False
   
   DOWNLOAD_DELAY = 1
   
   DEFAULT_REQUEST_HEADERS = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Language': 'en',
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
   }
   
   ITEM_PIPELINES = {
      'weixin_community.pipelines.WeixinCommunityPipeline': 300,
   }
   ```

5. 编写爬虫

6. 编写数据模型

7. 编写 `Pipline` 管道

8. 运行测试


