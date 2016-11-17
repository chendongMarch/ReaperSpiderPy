# coding:utf-8
import re
import time

import scrapy
from scrapy import Request
from scrapy.selector import Selector
from BaseSpider import BaseSpider
from reaperXXxiao.helper.MongoHelper import *


# meizitu.com的专辑和图片详情
class MeiZhiTuSpider(BaseSpider):
    def __init__(self):
        pass

    name = "xxxiao"
    allowed_domains = ["www.meizitu.com/"]
    url = "http://www.meizitu.com/a/5476.html"

    start_urls = [
        url
    ]

    findSize_reg = re.compile(r'-(\d+)x(\d+)')

    def parse(self, response):
        selector = Selector(response)
        print response.url, selector.extract()[0]
