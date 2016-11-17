# coding:utf-8
import re

from scrapy import Request
from scrapy.selector import Selector

from BaseSpider import BaseSpider
from reaperXXxiao.helper.MongoHelper import MongoHelper
from reaperXXxiao.helper.JsonHelper import JsonHelper
from reaperXXxiao.model.Video import Video
from scrapy import Request


# 视频爬虫,xxxiao视频和美拍视频
class VideoSpider(BaseSpider):
    def __init__(self):
        super(VideoSpider, self).__init__()

    name = "xxxiao"
    allowed_domains = ["xxxiao.com"]
    reaper_video_url = 'http://v.xxxiao.com/'
    reaper_video_url_meipai = 'http://www.meipai.com/square/19'
    jsonHelper = JsonHelper()
    start_urls = [
        # reaper_video_url,
        # reaper_video_url_meipai
        "http://www.meizitu.com/a/5476.html"
    ]
    url_already_scrapy = []
    db = MongoHelper.getDb()
    collVideo = MongoHelper.getCol(db, 'videoDbTest')

    def generateVideoIntVideoType(self, category):
        if category == '搞笑视频':
            return 1
        elif category == '美女视频':
            return 2
        elif category == '内涵视频':
            return 3
        elif category == '技巧视频':
            return 4
        elif category == '酷炫视频':
            return 5
        else:
            return 0

    def saveVideo(self, video):
        print video.width, video.height
        info = {
            'time_stamp': self.time_stamp,
            'describe': video.describe,
            'linkPageUrl': video.linkPageUrl,
            'width': video.width,
            'height': video.height,
            'publishTime': video.publishTime,
            'videoCategory': video.videoCategory,
            'videoCategoryType': video.videoCategoryType,
            'videoPlayUrl': video.videoPlayUrl
        }
        MongoHelper.updateOrInsert(self.collVideo, info)

    # 解析推荐页面,存储album_recommend
    def parse(self, response):
        url = response.url
        print url
        if url in self.url_already_scrapy:
            print url, "已经爬取过"
            return
        selector = Selector(response)
        print selector.extract()
        return
        self.url_already_scrapy.append(url)
        video = Video('new video')
        if url.startswith("http://v.xxxiao.com"):
            self.parseXXXiao(response, video)
        elif url.startswith("http://www.meipai.com"):
            self.parseMeipai(response, video)
        self.saveVideo(video)

    def parseMeipai(self, response, video):
        selector = Selector(response)
        for path_li in selector.xpath('//li[@class="pr no-select loading  J_media_list_item"]'):
            video.publishTime = self.generatePublishTime(self.extract(path_li, "meta/@content"))
            video.videoCoverUrl = self.extract(path_li, 'img/@src')
            video.width = self.extract(path_li, 'img/@width')
            video.height = self.extract(path_li, 'img/@height')
            desc = self.extract(path_li, 'img/@alt')
            reobj = re.compile('@(.*)|#(.*)#')
            video.describe = reobj.sub('', desc)
            video.videoPlayUrl = self.extract(path_li, 'div/@data-video')
            print video.videoPlayUrl, video.publishTime, video.videoCoverUrl, video.width, video.height, video.describe

    def parseXXXiao(self, response, video):
        selector = Selector(response)
        for path_article in selector.xpath('//article'):
            # header 获取视频描述和链接的URL
            path_header = path_article.xpath('header[@class="entry-header"]')
            video.videoCategory = self.extract(path_header, 'div/span/a/text()')
            video.videoCategoryType = self.generateVideoIntVideoType(video.videoCategory)
            video.describe = self.extract(path_header, 'h2[@class="entry-title"]/a/text()')
            video.linkPageUrl = self.extract(path_header, 'h2[@class="entry-title"]/a/@href')

            # 内容
            path_content = path_article.xpath('div/div/video')
            video.width = self.extract(path_content, '@width')
            video.height = self.extract(path_content, '@height')
            video.videoPlayUrl = self.extract(path_content, 'a/@href')

            # footer发布时间
            structTime = path_article.xpath('//footer/div/div/div/div/span/a/time/@datetime').extract()[0]
            video.publishTime = self.generatePublishTime(structTime)

        pathPreUrl = selector.xpath('//nav/div/div[@class="nav-previous"]/a/@href').extract()
        pathNextUrl = selector.xpath('//nav/div/div[@class="nav-next"]/a/@href').extract()
        if len(pathPreUrl) != 0:
            preUrl = pathPreUrl[0]
            yield Request(preUrl, callback=self.parse)
        if len(pathNextUrl) != 0:
            nextUrl = pathNextUrl[0]
            yield Request(nextUrl, callback=self.parse)
