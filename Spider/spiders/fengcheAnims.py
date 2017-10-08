import scrapy
import json


class BilibiliSpider(scrapy.Spider):
    name = 'fengcheAnims'
    start_urls = ['http://www.dm530.net/list/-hot--.html']

    def parse(self, response):
        anim_list = response.css('.fire .pics ul li>a::attr(href)').extract();
        for anim in anim_list:
            detail_url = 'http://www.dm530.net' + anim;
            yield response.follow(detail_url, callback=self.parse_detail_page)
        
        if anim_list is not None:
            next_url = response.css('.pages a:nth-child(3)::attr(href)').extract_first()
            next_url = 'http://www.dm530.net' + next_url
            yield response.follow(next_url, callback=self.parse)

    def parse_detail_page(self, response):
        title = response.css('.names::text').extract_first()
        alias = response.css('.alex p::text').extract_first()
        cover = response.css('.tpic img::attr(src)').extract_first()
        zone = ""
        category = []
        year = ""
        tag = []
        all_info = response.css('.alex span')
        for info in all_info:
            name = info.css('span::text').extract_first()
            if isinstance(name, str) != True:
                continue
            if name.startswith('地区'):
                zone = info.css('span a::text').extract_first()
            elif name.startswith('类型'):
                category = info.css('span a::text').extract()
            elif name.startswith('年代'):
                year = info.css('span a::text').extract_first()
            elif name.startswith('标签'):
                tag = info.css('span a::text').extract()
        yield {
            'title': title,
            'cover': cover,
            'alias': alias,
            'zone': zone,
            'category': category,
            'year': year,
            'tag': tag,
            'url': response.url
        }