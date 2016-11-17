# coding:utf-8
import scrapy
import time
from scrapy import Request


# 爬虫基类，实现公共方法
class BaseSpider(scrapy.spiders.Spider):
    time_stamp = time.strftime("%Y%m%d%H%M", time.localtime())

    def parse(self, response):
        pass

    def __init__(self):
        pass

    #  防止页面重定向
    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]
        })

    @staticmethod
    def code(unicode):
        # replace_reg = re.compile(r'-\d(.*).jpg')
        # url = replace_reg.sub('.jpg', unicode.encode())
        # return url
        return unicode.encode()

    @staticmethod
    def extract(self, baseline, xpath):
        return baseline.xpath(xpath).extract()[0]

    @staticmethod
    def generatePublishTime(self, timestr):
        index = timestr.find('+')
        timestr = timestr[0:index]
        format = '%Y-%m-%dT%H:%M:%S'
        structTime = time.strptime(timestr, format)
        return int(time.mktime(structTime))
