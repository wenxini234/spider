# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urljoin
from scrapy.http  import Request
from lingxi360.items import Lingxi360Item
import re


import codecs
class LingxiSpider(scrapy.Spider):
    name = 'lingxi'
    #allowed_domains = ['lingxi360.com']
    start_urls = ['http://www.lingxi360.com/category/news']
    domain = 'http://www.lingxi360.com'
    def parse(self, response):
        #print((response.text.encode('utf-8')))
        node=response.css("#news")
        #每一页的文章列表
        # href_list=node.css('a.more::attr(href)').extract()

        node1 = response.css(".row")
        for url in node1:
            link=url.css('.new-title a::attr(href)').extract_first('')
            link =urljoin(response.url,link)

            title=url.css('.new-title a::text').extract_first('')
            addtime=url.css('.new-time::text').extract_first('').strip().replace(' ',"").strip()
            img=url.css(".mobile-img::attr(src)").extract_first('')
            img=urljoin(response.url,img)

            yield Request(url=link,callback=self.article_detail, meta={'proxy': '','title':title,'addtime': addtime,'img':img,'link':link})
        #获取总页数
        #解析下一页的url链接

        next_url=node.css('div.pagestring li:nth-last-child(2) a.img-button::attr(href)').extract_first('')
        #next_url = node.css('div.pagestring a img').extract_first('')
        next_url=urljoin(response.url,next_url)
        if next_url:
            yield Request(url=next_url,callback=self.parse,meta={'proxy': '',})





    def article_detail(self,response):

        item=Lingxi360Item()
        #print(response.text)
        content=response.css('.info-content').extract_first('')
        #获得正文内容，提取出图片 依次替换成带有域名的图片
        # body中的img标签的src相对路径改成绝对路径
        pattern = "(<img .*?src=\")(.*?)(\")"
        def func(m):
            if not m.group(2).startswith("http"):
                rtn = "".join([m.group(1),self.domain , m.group(2), m.group(3)])
                print(response.meta.get('link'))
                #print(rtn)
                return rtn
            else:
                return "".join([m.group(1), m.group(2), m.group(3)])
        content = re.compile(pattern).sub(func, content)
        #print(content)
        item['title']=response.meta.get('title')
        item['content'] = content
        item['img'] = response.meta.get('img')
        item['link'] = response.meta.get('link')
        item['addtime'] = response.meta.get('addtme')
        return item



        #print(response.meta.get('title'))






