# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
import json
import codecs
class Lingxi360Pipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingCnblogsPipeline(object):
    def __init__(self):
        self.file = codecs.open('lingxi.html', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        #line = json.dumps(dict(item), ensure_ascii=False) + "\n"\
        dicv=dict(item)
        str= dicv.get("title")+dicv.get("content")+"<br/>"
        self.file.write(str)
        return item
    
    def spider_closed(self, spider):
        self.file.close()
