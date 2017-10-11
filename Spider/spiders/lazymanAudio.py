# -*- coding: utf-8 -*-
import scrapy
import json


class BilibiliSpider(scrapy.Spider):
    name = 'lazymanAudio'
    start_urls = ['http://www.lrts.me/book/5181']

    def parse(self, response):
        pass
        # json_str = response.body.decode()
        # json_obj = json.loads(json_str)
        # anim_list = json_obj['data']['archives']
        # for anim in anim_list:
        #     yield {
        #         'title': anim['title'],
        #         'image': anim['pic'],
        #         'desc': anim['description'],
        #         'b_url': 'http://www.bilibili.com/video/av' + str(anim['aid']),
        #         'video_count': anim['videos']
        #     }
        # if len(anim_list) > 0:
        #     self.pageNum += 1
        #     next_url = self.next_url % self.pageNum
        #     yield response.follow(next_url, callback=self.parse)
