
import scrapy

class LuoxiaSpider(scrapy.Spider):
    name = 'luoxiaBook'
    start_urls = [
        'http://www.luoxia.com/indb/',
        'http://www.luoxia.com/top/',
        'http://www.luoxia.com/hot/',
        'http://www.luoxia.com/jingdian/',
        'http://www.luoxia.com/jinyong/',
        'http://www.luoxia.com/hao/',
        'http://www.luoxia.com/yuanzhu/'
    ]

    def parse(self, response):
        res_url = response.url
        if res_url.endswith('/indb/') or res_url.endswith('/top/'):
            for book in response.css('#content-list li'):
                url = book.css('.book-describe-indb a::attr(href)').extract_first()
                yield response.follow(url, callback=self.parse_book_detail)
            next_page = response.css('.nextpostslink::attr(href)').extract_first()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        else:
            for book in response.css('li.pop-book2'):
                url = book.css('a::attr(href)').extract_first()
                yield response.follow(url, callback=self.parse_book_detail2)

    def parse_book_detail2(self, response):
        title = response.css('h1::text').extract_first()
        author = response.css('h1+ p::text').extract_first().split('：')[1]
        category = response.css('.book-describe p:nth-child(3)::text').extract_first().split('：')[1]
        begin_time = response.css('.book-describe p:nth-child(4)::text').extract_first().split('：')[1]
        end_time = response.css('.book-describe p:nth-child(5)::text').extract_first()
        read_url = response.css('p:nth-child(6) a::attr(href)').extract_first()
        if len(response.css('.book-list')) > 0:
            read_url = response.url
        description = response.css('.describe-html p::text').extract()
        book_cover = response.css('.book-img img::attr(src)').extract_first()
        yield {
            'title':title,
            'author':author,
            'category':category,
            'begin_time':begin_time,
            'end_time':end_time,
            'read_url':read_url,
            'description':description,
            'book_cover':book_cover
        }

    def parse_book_detail(self, response):
        title = response.css('h1::text').extract_first()
        author = response.css('h1+ p::text').extract_first().split('：')[1]
        category = response.css('.book-describe p:nth-child(3)::text').extract_first().split('：')[1]
        begin_time = response.css('.book-describe p:nth-child(4)::text').extract_first().split('：')[1]
        end_time = response.css('.book-describe p:nth-child(5)::text').extract_first()
        read_url = response.css('p:nth-child(6) a::attr(href)').extract_first()
        description = response.css('.post2 > p::text').extract()
        book_cover = response.css('.wp-post-image::attr(src)').extract_first()
        yield {
            'title':title,
            'author':author,
            'category':category,
            'begin_time':begin_time,
            'end_time':end_time,
            'read_url':read_url,
            'description':description,
            'book_cover':book_cover
        }





