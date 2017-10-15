# -*- coding: utf-8 -*-
import scrapy
import leancloud

class LuoxiabooksectionSpider(scrapy.Spider):
    name = 'luoxiaBookSection'
    # start_urls = ['http://www.luoxia.com/santi/']

    def start_requests(self):
        appid = "xxx"
        appkey = "xxx"
        leancloud.init(appid, appkey)
        query = leancloud.Query('Book')
        books = query.find()
        for book in books:
            url = book.get('read_url')
            if url.startswith('http://www.luoxia.com'):
                yield scrapy.Request(url, meta={"book_Id":book.get('objectId')}, callback=self.parse)
            else:
                continue

    def parse(self, response):
        sub_books = response.css('.title')
        book_name = response.css('h1::text').extract_first()
        book_Id = response.meta['book_Id']
        if len(sub_books) > 0:
            for book in sub_books:
                sub_book_name = book.css('h3 a::text').extract_first()
                book_sections = book.css('.title + .book-list ul li')
                for i in range(len(book_sections)):
                    section = book_sections[i]
                    section_index = i + 1
                    section_url = section.css('a::attr(href)').extract_first()
                    yield response.follow(section_url, meta={"book_id":book_Id, "book_name":book_name, "sub_book_name":sub_book_name, "section_index":section_index}, callback=self.parser_section_detail)
        else:
            book_sections = response.css('.book-list ul li')
            for i in range(len(book_sections)):
                section = book_sections[i]
                section_index = i + 1
                section_url = section.css('a::attr(href)').extract_first()
                yield response.follow(section_url, meta={"book_id":book_Id, "book_name":book_name, "section_index":section_index}, callback=self.parser_section_detail)

    def parser_section_detail(self, response):
        section_title = response.css('.post-title::text').extract_first()
        author = response.css('.post-time b::text').extract_first()
        content = response.css('article>p').extract()
        content = "".join(content)
        book_name = response.meta['book_name']
        section_index = response.meta['section_index']
        book_Id = response.meta['book_id']
        if 'sub_book_name' in response.meta:
            sub_book_name = response.meta['sub_book_name']
        else:
            sub_book_name = ""
        yield {
            "bookId": book_Id,
            "bookName": book_name,
            "index": section_index,
            "sectionTitle": section_title,
            "author": author,
            "content": content,
            "subBookName": sub_book_name
        }
    
