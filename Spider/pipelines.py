# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import leancloud
from scrapy.exceptions import DropItem

class SpiderPipeline(object):

    def __init__(self):
        self.appid = "xxx"
        self.appkey = "xxx"

    def open_spider(self, spider):
        leancloud.init(self.appid, self.appkey)

    def process_item(self, item, spider):
        if spider.name == 'luoxiaBook':
            name = item['title']
            query = leancloud.Query('Book')
            query.equal_to('title', name)
            books = query.find()
            if len(books) > 0:
                # 更新数据 
                book = books[0]
                book.set('title', item['title'])
                book.set('author', item['author'])
                book.set('category', item['category'])
                book.set('begin_time', item['begin_time'])
                book.set('end_time', item['end_time'])
                book.set('read_url', item['read_url'])
                book.set('description', item['description'])
                book.set('book_cover', item['book_cover'])
                book.save()
                return item
            else:
                Book = leancloud.Object.extend('Book')
                book = Book()
                book.set('title', item['title'])
                book.set('author', item['author'])
                book.set('category', item['category'])
                book.set('begin_time', item['begin_time'])
                book.set('end_time', item['end_time'])
                book.set('read_url', item['read_url'])
                book.set('description', item['description'])
                book.set('book_cover', item['book_cover'])
                book.save()
                return item
        else: 
            return item
