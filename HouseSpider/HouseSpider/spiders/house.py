# -*- coding: utf-8 -*-
import scrapy
import urlparse
from ..items import HouseItem
import re
from HouseSpider.send_email import send_file_email
class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['zz.fang.lianjia.com']
    start_urls = [
        'http://zz.fang.lianjia.com/loupan/',
        'https://zz.lianjia.com/ershoufang/',#二手房
    ]

    def parse(self, response):
        if 'loupan' in response.url:
            yield scrapy.Request(url=response.url,callback=self.parse_loufang,dont_filter=True)
            pattern = re.compile(r"""page-data='{"totalPage":(.*?),"curPage":1}'>""", re.S)
            page = re.findall(pattern, response.body)
            page = "".join(page)
            if page != '':
                page = int(page)
                for x in xrange(2, page + 1):
                    url = "http://zz.fang.lianjia.com/loupan/pg%s/" % x
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)
        if 'ershoufang' in response.url:
            yield scrapy.Request(url=response.url,callback=self.parse_ershoufang,dont_filter=True)
            pattern = re.compile(r"""page-data='{"totalPage":(.*?),"curPage":1}'>""", re.S)
            page = re.findall(pattern, response.body)
            page = "".join(page)
            if page != '':
                page = int(page)
                for x in xrange(2, page + 1):
                    url = "https://zz.lianjia.com/ershoufang/pg%s/" % x
                    yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)




    def parse_loufang(self,response):
        li_list = response.xpath("//ul[@class='house-lst']/li")
        for li in li_list:
            yishoufang_imgs = li.xpath("div/a/img/@src").extract_first("")
            yishoufang_imgs = urlparse.urljoin(response.url ,yishoufang_imgs)
            yishoufang_names = li.xpath("div/div/h2/a/text()").extract_first("")
            yishoufang_where = li.xpath("div/div/div[@class='where']/span/text()").extract_first("")
            yishoufang_mianji = li.xpath("div/div/div[@class='area']").extract_first("").strip()
            pattern = re.compile(r'<.*?>| {10}', re.S)
            yishoufang_mianji = re.sub(pattern, '', yishoufang_mianji)

            pattern = re.compile(r'<span.*?>', re.S)
            yishoufang_mianji = re.sub(pattern, '', yishoufang_mianji)
            pattern = re.compile(r'</span>', re.S)
            yishoufang_mianji = re.sub(pattern, '', yishoufang_mianji)

            pattern = re.compile(r'<a.*?>', re.S)
            yishoufang_mianji = re.sub(pattern, '', yishoufang_mianji)
            pattern = re.compile(r'</a>', re.S)
            yishoufang_mianji = re.sub(pattern, '', yishoufang_mianji)

            pattern = re.compile(r'<div.*?>', re.S)
            yishoufang_mianji = re.sub(pattern, '', yishoufang_mianji)
            pattern = re.compile(r'</div>', re.S)
            yishoufang_mianji = re.sub(pattern, '', yishoufang_mianji)

            yishoufang_money = li.xpath("div/div/div/div[@class='average']//text()").extract_first("").strip()
            item = HouseItem()
            item['imgs'] = [yishoufang_imgs]
            item['title'] = yishoufang_names
            item['flood'] = yishoufang_where
            item['address'] = yishoufang_mianji
            item['money'] = yishoufang_money
            item['style'] = u'一手房'
            yield item



    def parse_ershoufang(self,response):
        li_list = response.xpath("//ul[@class='sellListContent']/li")
        for li in li_list:
            ershoufang_imgs = li.xpath("a/img/@src").extract_first("")
            ershoufang_imgs = urlparse.urljoin(response.url,ershoufang_imgs)
            ershoufang_title = li.xpath("div/div[@class='title']/a/text()").extract_first("").strip()
            ershoufang_address = li.xpath("div/div[@class='address']/div").extract_first("").strip()
            pattern = re.compile(r'<span.*?>', re.S)
            ershoufang_address = re.sub(pattern, '', ershoufang_address)
            pattern = re.compile(r'</span>', re.S)
            ershoufang_address = re.sub(pattern, '', ershoufang_address)

            pattern = re.compile(r'<a.*?>', re.S)
            ershoufang_address = re.sub(pattern, '', ershoufang_address)
            pattern = re.compile(r'</a>', re.S)
            ershoufang_address = re.sub(pattern, '', ershoufang_address)

            pattern = re.compile(r'<div.*?>', re.S)
            ershoufang_address = re.sub(pattern, '', ershoufang_address)
            pattern = re.compile(r'</div>', re.S)
            ershoufang_address = re.sub(pattern, '', ershoufang_address)
            ershoufang_address = ershoufang_address.split("|")
            ershoufang_address = ",".join(ershoufang_address)
            ershoufang_address = ershoufang_address.replace(' ','')


            ershoufang_flood = li.xpath("div/div[@class='flood']/div").extract_first("").strip()
            pattern = re.compile(r'<span.*?>', re.S)
            ershoufang_flood = re.sub(pattern, '', ershoufang_flood)
            pattern = re.compile(r'</span>', re.S)
            ershoufang_flood = re.sub(pattern, '', ershoufang_flood)


            pattern = re.compile(r'<a.*?>', re.S)
            ershoufang_flood = re.sub(pattern, '', ershoufang_flood)
            pattern = re.compile(r'</a>', re.S)
            ershoufang_flood = re.sub(pattern, '', ershoufang_flood)


            pattern = re.compile(r'<div.*?>', re.S)
            ershoufang_flood = re.sub(pattern, '', ershoufang_flood)
            pattern = re.compile(r'</div>', re.S)
            ershoufang_flood = re.sub(pattern, '', ershoufang_flood)


            ershoufang_money =  li.xpath("div/div[@class='priceInfo']/div//text()").extract_first("").strip()
            item = HouseItem()
            item['imgs'] = [ershoufang_imgs]
            item['title'] = ershoufang_title
            item['address'] = ershoufang_address
            item['flood'] = ershoufang_flood
            item['money'] = ershoufang_money
            item['style'] = u'二手房'
            yield item

    @staticmethod
    def close(spider, reason):
        closed = getattr(spider, 'closed', None)
        print u"爬虫项目关闭"
        send_file_email(
            "zhang864071694@163.com",
            u"<h1>爬取郑州所有的房源信息</h1>",
            "new_house.xlsx",
            u"王子寒",
        )
        if callable(closed):
            return closed(reason)





