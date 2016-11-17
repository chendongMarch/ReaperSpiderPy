# coding:utf-8
from scrapy import Request
from scrapy.selector import Selector

from BaseSpider import BaseSpider


# xxxiao.com的 funny image 搞笑动图和图片
class FunnyImageSpider(BaseSpider):
    def __init__(self):
        pass

    name = "xxxiao"
    allowed_domains = ["xxxiao.com"]
    reaper_gif_url = 'http://xxxiao.com/new'
    reaper_img_url = 'http://t.xxxiao.com/'
    start_urls = [
        reaper_gif_url,
        reaper_img_url
    ]

    #  防止页面重定向
    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]
        })

    # 解析推荐页面,存储album_recommend
    def parse(self, response):
        selector = Selector(response)
        for article in selector.xpath('//article'):
            # image,获取宽高和资源url
            pathImg = article.xpath('div[@class="post-thumb"]/a/img')
            width = self.extract(pathImg, '@width')
            height = self.extract(pathImg, '@height')
            imgSrc = self.extract(pathImg, '@src')

            # header数据,获取图片的标签
            pathHeader = article.xpath('div[@class="post-thumb"]/header[@class="entry-header"]')
            categoryTag = self.extract(pathHeader, 'div/span/a/text()')

            #  详情数据,获取链接到的网页和显示的文案
            pathDetails = pathHeader.xpath('h2/a')
            linkPageUrl = self.extract(pathDetails, "@href")
            imgDesc = self.extract(pathDetails, "text()")

            # footer数据,获取发布时间
            publishTime = self.extract(article, 'footer/div/div/div/div/span/a/time/@datetime')
            print imgSrc, width, height, categoryTag, linkPageUrl, imgDesc, publishTime
        # 上一个和下一个链接
        pathPreUrl = selector.xpath('//nav/div/div[@class="nav-previous"]/a/@href').extract()
        pathNextUrl = selector.xpath('//nav/div/div[@class="nav-next"]/a/@href').extract()
        if len(pathPreUrl) != 0:
            preUrl = pathPreUrl[0]
            print preUrl
        if len(pathNextUrl) != 0:
            nextUrl = pathNextUrl[0]
            print nextUrl
