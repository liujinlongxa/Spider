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
            return self.process_book_item(item)
        elif spider.name == 'luoxiaBookSection':
            return item
            # return self.process_book_section_item(item)

    # Private Method
    def process_book_section_item(self, item):
        book_name = item['bookName']
        section_title = item['sectionTitle']
        sub_book_name = item['subBookName']
        section_index = item['index']

        # 查询所属的书籍
        book_query = leancloud.Query('Book')
        book_query.equal_to('title', book_name)
        books = book_query.find()
        if len(books) <= 0:
            return DropItem('没有找到对应的书籍')
        else:
            book = books[0]

        # 查询对应的章节是否已经存在，如果已经存在则只做更新
        query = leancloud.Query('BookSections')
        query.equal_to('bookName', book_name)
        query.equal_to('sectionTitle', section_title)
        query.equal_to('index', section_index)
        if len(sub_book_name) > 0:
            query.equal_to('subBookName', sub_book_name)
        sections = query.find()
        if len(sections) > 0:
            # 更新
            section = sections[0]
            section.set('bookName', book_name)
            section.set('index', section_index)
            section.set('sectionTitle', section_title)
            section.set('author', item['author'])
            section.set('content', item['content'])
            section.set('subBookName', sub_book_name)
            section.set('book', book)
            section.save()
            pass
        else:
            # 创建
            BookSection = leancloud.Object.extend('BookSections')
            section = BookSection()
            section.set('bookName', book_name)
            section.set('index', section_index)
            section.set('sectionTitle', section_title)
            section.set('author', item['author'])
            section.set('content', item['content'])
            section.set('subBookName', sub_book_name)
            section.set('book', book)
            section.save() 
            pass
        

    def process_book_item(self, item):
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
            book.set('sub_book', item['sub_book'])
            book.save()
            return item
        else:
            # 创建数据
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
            book.set('sub_book', item['sub_book'])
            book.save()
            return item
