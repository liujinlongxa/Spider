
import scrapy

class ThepaperaSpider(scrapy.Spider):
    name = 'news'
    pageNum = 2
    nextPageUrl = 'http://www.thepaper.cn/load_index.jsp?nodeids=26506&topCids=&pageidx=%d&lastTime=1502785671194&isList=true'
    start_urls = [
        'http://www.thepaper.cn/list_scroll.jsp?nodeid=26506&_=1506236465932'
    ]

    def parse(self, response):
        all_news = response.css('.news_li')
        for news in all_news:
            news_id = news.css('::attr(id)').extract_first();
            if news_id == 'last1':
                continue
            title = news.css('h2 a::text').extract_first()
            desc = news.css('p::text').extract_first()
            image = news.css('.news_tu img::attr(src)').extract_first()
            url = 'http://www.thepaper.cn/' + news.css('h2 a::attr(href)').extract_first()
            yield {
                'title':title,
                'desc': desc,
                'image': image,
                'url': url
            }
        if len(all_news) > 0:
            next_url = self.nextPageUrl % self.pageNum
            self.pageNum += 1
            yield response.follow(next_url, callback=self.parse)
