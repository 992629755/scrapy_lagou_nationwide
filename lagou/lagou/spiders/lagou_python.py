# -*- coding: utf-8 -*-
from lxml import etree

import scrapy

from lagou.items import LagouItem


class LagouPythonSpider(scrapy.Spider):
    name = 'lagou_python'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/?filterOption=3']


    def parse(self, response):
        html_text=response.body.decode('utf-8')
        html = etree.HTML(html_text)
        master_xp = html.xpath("//ul[@class='item_con_list']//li")
        for i in master_xp:
            lagou_item = LagouItem()
            lagou_item['position_id'] = i.xpath("./@data-positionid")[0]
            lagou_item['company_id']= i.xpath(" ./@data-companyid")[0]
            lagou_item['position']= i.xpath("./@data-positionname")[0]
            lagou_item['publish_time']= i.xpath(".//span[@class='format-time']/text()")[0]
            lagou_item['pay']= i.xpath("./@data-salary")[0]
            lagou_item['exp_education']= i.xpath(".//div[@class='li_b_l']/text()[3]")[0].rstrip(' ').replace('\n','')
            lagou_item['company']= i.xpath(".//@data-company")[0]
            lagou_item['people_num']= i.xpath(".//div[@class='industry']/text()")[0].strip('\n').strip(' ').strip('\n')
            lagou_item['state']= i.xpath(".//div[@class='li_b_r']/text()")[0].strip(' ')
            lagou_item['province']= i.xpath(".//span[@class='add']//em/text()")[0].strip('[').strip(']')
            yield lagou_item

        try:
            url = response.xpath("//div[@class='pager_container']/a/@href").extract()[-1]
            yield scrapy.Request(url, callback=self.parse)
        except:
            print("error")














