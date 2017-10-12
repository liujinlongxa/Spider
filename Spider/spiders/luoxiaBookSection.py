# -*- coding: utf-8 -*-
import scrapy


class LuoxiabooksectionSpider(scrapy.Spider):
    name = 'luoxiaBookSection'
    start_urls = ['http://www.luoxia.com/santi/santi-1/']

    def parse(self, response):
        book_sections = response.css('.book-list ul li')
        for i in range(len(book_sections)):
            section = book_sections[i]
            section_index = i + 1
            book_name = response.css('h1::text').extract_first()
            section_url = section.css('a::attr(href)').extract_first()
            yield response.follow(section_url, meta={"book_name":book_name, "section_index":section_index}, callback=self.parser_section_detail)

    def parser_section_detail(self, response):
        section_title = response.css('.post-title::text').extract_first()
        author = response.css('.post-time b::text').extract_first()
        content = response.css('article>p').extract()
        content = "".join(content)
        book_name = response.meta['book_name']
        section_index = response.meta['section_index']
        yield {
            "title": book_name,
            "index": section_index,
            "sectionTitile": section_title,
            "author": author,
            "content": content
        }
