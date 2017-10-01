# -*- coding: utf-8 -*-
import scrapy
import json


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    pageNum = 1;
    next_url = 'http://api.bilibili.com/archive_rank/getarchiverankbypartion?type=json&tid=32&pn=%d'
    start_urls = ['http://api.bilibili.com/archive_rank/getarchiverankbypartion?type=json&tid=32&pn=1']

    def parse(self, response):
        json_str = response.body.decode()
        json_obj = json.loads(json_str)
        anim_list = json_obj['data']['archives']
        for anim in anim_list:
            yield {
                'title': anim['title'],
                'image': anim['pic'],
                'desc': anim['description'],
                'b_url': 'http://www.bilibili.com/video/av' + str(anim['aid']),
                'video_count': anim['videos']
            }
        if len(anim_list) > 0:
            self.pageNum += 1
            next_url = self.next_url % self.pageNum
            yield response.follow(next_url, callback=self.parse)
