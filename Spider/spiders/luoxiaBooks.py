
import scrapy

class LuoxiaSpider(scrapy.Spider):
    name = 'luoxia'
    start_urls = [
        'http://www.luoxia.com/top/'
    ]

    def parse(self, response):
        for book in response.css('#content-list li'):
            url = book.css('.book-describe-indb a::attr(href)').extract_first()
            yield response.follow(url, callback=self.parse_book_detail)
        next_page = response.css('.nextpostslink::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

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





