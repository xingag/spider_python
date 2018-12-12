# -*- coding: utf-8 -*-
import scrapy
import re
from sfw.items import NewHouseItem, ESFHouseItem
import time


# 使用普通的爬虫来爬取【搜房网 - 房天下】

class SfwSpiderSpider(scrapy.Spider):
    name = 'sfw_spider'
    allowed_domains = ['fang.com']

    # 从城市开始爬
    start_urls = ['http://www.fang.com/SoufunFamily.htm']

    HTTPS = "https:"

    def parse(self, response):

        tr_elements = response.xpath('//div[@class="outCont"]//tr')

        # 定义一个临时省份数据【初始化为None】；
        province = None

        for tr_element in tr_elements:
            # 1.筛选掉 class="font01" 为 td 的标签
            # 获取没有 class 属性的所有 td 标签
            td_elememts = tr_element.xpath('.//td[not(@class)]')

            # 2.1 td标签【省份】
            province_td = td_elememts[0]

            # 2.2 获取省份标签下的内容
            province_content = province_td.xpath('.//text()').get().strip()

            # 注意：如果当前行能够获取到【省份】数据，就替换当前的省份；否则使用上一次获取到的【省份】数据
            if province_content:
                province = province_content
                # print('==' * 40)
                # print('省份:' + province)

            # 2.3 过滤掉海外城市
            if province_content == '其它':
                break

            # 3.1 td标签【城市】
            city_td_element = td_elememts[1]

            # 3.2 所有的城市
            city_td_a_elements = city_td_element.xpath('.//a')

            for city_td_a_element in city_td_a_elements:
                # 城市名字和URL地址
                city = city_td_a_element.xpath('.//text()').get()
                link = city_td_a_element.xpath('.//@href').get()

                # 4.1 构建新房和二手房的 URL 链接
                # http://hf.fang.com/
                link_pre = re.split('[.]', link)
                domain = link_pre[1] + "." + link_pre[2]

                # 4.2 北京作为默认的城市，要单独处理
                if city == '北京':
                    new_house_url = 'http://newhouse.fang.com/house/s/'
                    esf_url = 'http://esf.fang.com/'

                    # 新房的domain
                    domain_new_house = "http://newhouse.fang.com"
                else:
                    # 新房URL【首页】
                    new_house_url = link_pre[0] + ".newhouse." + domain + "house/s/"

                    # 二手房URL【首页】
                    esf_url = link_pre[0] + ".esf." + domain

                    # 新房的domain【domain】
                    domain_new_house = link_pre[0] + ".newhouse.fang.com"

                # 4.3.1 爬取新房数据【通过meta传递参数】
                yield scrapy.Request(url=new_house_url, callback=self.parse_new_house,
                                     meta={"info": (province, city, domain_new_house)})

                # 4.4.1 爬取二手房数据
                print('爬取二手房:%s' % esf_url)
                yield scrapy.Request(url=esf_url, callback=self.parse_esf,
                                     meta={"info": (province, city)}, cookies={})

                time.sleep(1)
                # break
            time.sleep(2)
            # break

    def parse_new_house(self, response):
        """
        爬取新房数据
        :param response:
        :return:
        """
        # 获取参数信息
        province, city, domain_new_house = response.meta.get('info')

        # 1.获取所有的列元素
        li_elements = response.xpath('//div[contains(@class,"nl_con")]/ul//li')

        # 遍历每一个楼盘
        # 注意：可能楼盘数据可能是【脏数据】
        for li_element in li_elements:
            # 2.获取数据
            # 2.1 楼盘名称
            name = li_element.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            if name:
                name = name.strip()

            # 2.2 几居室
            house_type_list_pre = li_element.xpath('.//div[contains(@class,"house_type ")]/a/text()').getall()
            # 2.2.2 去除列表中每一项中的空格
            house_type_list = list(map(lambda x: re.sub(r'\s', "", x), house_type_list_pre))
            # 2.2.3 如果居室不是以【居】结尾，就过滤掉，返回为空列表：[]
            rooms = list(filter(lambda x: x.endswith("居"), house_type_list))

            # 3.面积
            # 注意：这里必须调用getall()【获取的是一个列表】，因为下面的数据是多行显示
            area_pre = "".join(li_element.xpath('.//div[contains(@class,"house_type ")]/text()').getall())
            # 去除【空格、-、/ 三种特殊字符】
            # 注意：横线不是【英文输入法下面】的横线，直接拷贝过来就行了
            area = re.sub(r'\s|－|/', '', area_pre)

            # 4.地址
            # 注意：从a标签的title属性获取的地址比较完整
            address = li_element.xpath('.//div[@class="address"]/a/@title').get()
            # print(address)

            # 5.行政区【部分行政区有空】
            # 注意：有些列表中没有span标签，因此直接从a标签下面获取全部数据进行截取的方式更为保险
            district_pre = "".join(li_element.xpath('.//div[@class="address"]/a//text()').getall())

            if re.search(r".*\[(.+)\].*", district_pre):
                district = re.search(r".*\[(.+)\].*", district_pre).group(1)
            else:
                district = None

            # 6.是否在售
            sale = li_element.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()

            # 7.价格
            price_pre = "".join(li_element.xpath('.//div[@class="nhouse_price"]//text()').getall())

            # 替换【脏数据】为空
            price = re.sub(r'\s|广告', '', price_pre)

            # 8.详情页面url
            origin_url_pre = li_element.xpath('.//div[@class="nlcd_name"]/a/@href').get()

            if origin_url_pre:
                origin_url = self.HTTPS + origin_url_pre

            item = NewHouseItem(province=province, city=city, name=name, price=price, rooms=rooms, area=area,
                                address=address, district=district, sale=sale, origin_url=origin_url)

            yield item

        # 爬取下一页数据
        # 格式：【】http://gz.newhouse.fang.com + /house/s/b92/
        next_url_content = response.xpath('//div[@class="page"]//a[contains(@class,"next")]/@href').get()
        if next_url_content:
            next_url = domain_new_house + next_url_content
            print('准备开始爬下一页的数据%s' % next_url)
            yield scrapy.Request(url=next_url, callback=self.parse_new_house,
                                 meta={"info": (province, city, domain_new_house)})
        else:
            print('获取下一页的地址为空，当前url：' + response.url)

    def parse_esf(self, response):
        """
        爬取二手房数据
        :param response:
        :return:
        """
        province, city = response.meta.get('info')
        dl_elements = response.xpath('//dl[@class="clearfix"]')

        # 1.获取每一项的楼盘
        for dl_element in dl_elements:

            # 定义Item
            item = ESFHouseItem(province=province, city=city)

            # 楼盘名称
            name = dl_element.xpath('.//p[@class="add_shop"]/a/text()').get()

            item['name'] = re.sub('\s', '', name) if name else ''

            # 2.几室几厅、面积、层次、朝向、年代【4个数据 】
            infos_pre = dl_element.xpath('.//p[@class="tel_shop"]/text()').getall()

            # 2.1 去掉空格字符
            infos = list(map(lambda x: re.sub(r'\s', '', x), infos_pre))

            # 设置默认值
            item['rooms'] = ''
            item['floor'] = ''
            item['toward'] = ''
            item['year'] = ''
            item['area'] = ''

            # 注意：有些数据不是正常的楼盘数据
            if infos:
                # 2.2 遍历去设置数据
                for info in infos:
                    if '厅' in info:
                        item['rooms'] = info
                    elif '层' in info:
                        item['floor'] = info
                    elif '向' in info:
                        item['toward'] = info
                    elif '年建' in info:
                        item['year'] = info.replace("年建", "")
                    elif '㎡' in info:
                        item['area'] = info
                    else:
                        pass

            # 3.地址
            address = dl_element.xpath('.//p[@class="add_shop"]//span/text()').get()
            item['address'] = address if address else ''

            # 4.总价【包含单位】
            price = "".join(dl_element.xpath('.//dd[@class="price_right"]/span[@class="red"]//text()').getall())
            item['price'] = price if price else ''

            # 5.单价
            unit = dl_element.xpath('.//dd[@class="price_right"]/span[last()]/text()').get()
            item['unit'] = unit if unit else ''

            # 6.详情页面的URL
            detail_url = dl_element.xpath('.//h4/a/@href').get()
            # 组成一个完整的url
            origin_url = response.urljoin(detail_url)

            item['origin_url'] = origin_url if origin_url else ''

            # 7.如果楼盘名称不存在，就不做处理
            if name:
                yield item

        # 爬取下一页的数据
        # 注意：获取p标签下内容为【下一页】的a标签
        next_url = response.xpath('//div[@class="page_al"]//a[text()="下一页"]/@href').get()

        if next_url:
            print('下一页地址:' + response.urljoin(next_url))
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf,
                                 meta={"info": (province, city)})
