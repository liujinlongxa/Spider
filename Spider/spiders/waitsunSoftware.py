# -*- coding: utf-8 -*-

import json
import scrapy


class WaitsunSpider(scrapy.Spider):
    name = 'software'
    start_urls = ['https://www.waitsun.com/']

    def parse(self, response):
        softwareList = response.css('.posts-list li.post')
        for software in softwareList:
            name = software.css('article header h2 a::text').extract_first()
            icon = software.css('a.thumbnail-link img::attr(src)').extract_first()
            desc = software.css('div.right-box p::text').extract_first()
            category = software.css('div.right-box ul li a::text').extract_first()
            link = software.css('article header h2 a::attr(href)').extract_first()
            if category == '守望爱情':
                continue
            yield {
                'name': name,
                'icon': icon,
                'desc': desc,
                'category': category,
                'link': link
            }
        next_url = response.css('.next-page a::attr(href)').extract_first()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)
