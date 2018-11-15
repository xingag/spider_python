# 使用 `Scrapy` 来爬取糗事百科

1. 修改 `settings.py` 配置文件

   ```
   # 1.修改 ROBOTSTXT_OBEY 为 False
   ROBOTSTXT_OBEY = False
   
   # 2.放开请求头的设置
   DEFAULT_REQUEST_HEADERS = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Language': 'en',
       'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
   }
   
   # 3.放开 PipLine 便于保存数据
   # 'qsbk.pipelines.QsbkPipeline'：Key；300：优先级；值越小，优先级越高。
   ITEM_PIPELINES = {
      'qsbk.pipelines.QsbkPipeline': 300,
   }
   ```

2. 编写爬虫代码 - `spiders/spider_xx.py`

   对 `Download` 下载后的数据，利用 `xpath` 进行解释，然后通过生成器传给 `PipLine`

3. 编写数据模型

   定义数据模型，便于管理

4. 编写 `Pipline` 管道

   编写保存数据的代码

   注意：需要在 `settings.py` 文件中激活 `Pipline`

















 