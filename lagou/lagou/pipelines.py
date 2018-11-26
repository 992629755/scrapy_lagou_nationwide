# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class LagouPipeline(object):
    #item of spider come in,then clearn data in this
    #if dont't clean next method
    def process_item(self, item, spider):
        return item

#save in databases
#create Class of database
class MongoLagouDB(object):
    # from classmethod getting argument value
    def __init__(self, mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    #the classmethod get mongodb data from setting.py
    @classmethod
    def from_crawler(cls,crawler):
        return  cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.mongo_db = self.client[self.mongo_db]

    #importance deal item process
    def process_item(self,item,spider):
        #this is select name
        nationwide_name = item.__class__.__name__
        self.mongo_db[nationwide_name].insert(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
