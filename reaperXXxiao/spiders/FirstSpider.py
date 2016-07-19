# coding:utf-8
import scrapy
from MongoUtils import *
from scrapy import Request
from scrapy.selector import Selector
import re
import time


class FirstSpider(scrapy.spiders.Spider):
    def __init__(self):
        pass

    name = "xxxiao"
    allowed_domains = ["m.xxxiao.com"]
    base_new = "http://m.xxxiao.com"
    base_xinggan = "http://m.xxxiao.com/cat/xinggan"
    base_shaonv = "http://m.xxxiao.com/cat/shaonv"
    base_mrxt = "http://m.xxxiao.com/cat/mrxt"
    base_wmxz = "http://m.xxxiao.com/cat/wmxz"
    base_wallpaper = "http://m.xxxiao.com/cat/wallpaper"
    base_swmt = "http://m.xxxiao.com/cat/swmt"
    start_urls = [
        base_new,
        base_xinggan,
        base_shaonv,
        base_mrxt,
        base_wmxz,
        base_swmt,
        base_wallpaper
    ]
    time_stamp = time.strftime("%Y%m%d%H%M", time.localtime())
    findSize_reg = re.compile(r'-(\d+)x(\d+)')

    #  防止页面重定向
    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True, meta={
            'dont_redirect': True,
            'handle_httpstatus_list': [301, 302]
        })

    # 获取数据库存储引用
    db = MongoUtils.getDb()

    # 推荐专辑 数据库集合,记录的首页分类型的推荐
    # 字段:
    # album_type : 推荐的类型,分new,xinggan,shaonv,mrxt,wmxz,wallpaper
    # album_link : 指向专辑详情的链接,通过这个链接作为主键,可以查询,这个专辑的详情
    # album_cover : 专辑的封面,图片链接
    # album_desc : 专辑的描述
    coll_album_recommend = MongoUtils.getCol(db, 'album_recommend')

    # 全部专辑 数据库集合,抽取的所有爬到的专辑列表
    # 字段:
    # album_link : 指向专辑详情的链接,通过这个链接作为主键,可以查询,这个专辑的详情
    # key_words : 关键字
    # album_cover : 专辑的封面,图片链接
    # album_desc : 专辑的描述
    coll_album_whole = MongoUtils.getCol(db, 'album_whole')

    # 详情 数据库集合,每一条字段存储一张图片
    # 字段:
    # album_link : 属于哪一个专辑
    # photo_src : 图片链接
    coll_album_detail = MongoUtils.getCol(db, 'album_detail')

    # 解析专辑详情页面,存储album_detail,album_whole
    def parse_detail(self, response):
        selector = Selector(response)
        # 页面中的其他链接
        for line in selector.xpath("//a[@class='pis-thumbnail-link']"):
            otherUrl = line.xpath('@href').extract()[0]
            yield Request(otherUrl, callback=self.parse_detail)
        # 上一个下一个的链接
        prevUrl = selector.xpath("//a[@rel='prev']/@href").extract()
        nextUrl = selector.xpath("//a[@rel='next']/@href").extract()
        if len(prevUrl) != 0:
            yield Request(prevUrl[0], callback=self.parse_detail)
        if len(nextUrl) != 0:
            yield Request(nextUrl[0], callback=self.parse_detail)
        # 如果当前链接已经爬取过了,终止数据抽取和存储的操作
        if self.isScrapyIt(response.url):
            print '这个链接 ' + response.url + '  已经爬取过了'
            return

        print '这个链接 ' + response.url + '  是一个新链接'
        album_link = selector.xpath('//head/link[@rel="canonical"]/@href').extract()[0]
        # 页面的title
        album_desc = selector.xpath('//head//title/text()').extract()[0]
        # 页面的关键字
        keywords = selector.xpath('//meta[@name="keywords"]/@content').extract()[0]

        # 专辑详情
        photo_src = ''
        for line in selector.xpath("//a[@class='rgg-a local-link']"):
            photo_src = self.code(line.xpath('@href').extract()[0])
            width = 0
            height = 0
            for x in self.findSize_reg.findall(photo_src):
                width = x[0]
                height = x[1]
            if width == 0 and height == 0:
                width = '1024'
                height = '638'
            detail_save = {
                'width': width,
                'height': height,
                'album_link': album_link,
                'photo_src': photo_src,
                'time_stamp': self.time_stamp}
            MongoUtils.updateOrInsert(self.coll_album_detail, detail_save)
        # whole专辑存入
        whole_save = {
            'album_link': album_link,
            'key_words': keywords,
            'album_cover': photo_src,
            'album_desc': album_desc,
            'time_stamp': self.time_stamp}
        MongoUtils.updateOrInsert(self.coll_album_whole, whole_save)

    # 解析推荐页面,存储album_recommend
    def parse(self, response):
        album_type = self.generateAlbumType(response.url)
        selector = Selector(response)
        for line in selector.xpath('//div[@class="post-thumb"]'):
            album_link = self.code(line.xpath('a[1]/@href').extract()[0])
            # yield Request(album_link, callback=self.parse_detail)
            album_cover = self.code(line.xpath('a[1]/img/@src').extract()[0])
            album_desc = self.code(line.xpath('a[1]/img/@alt').extract()[0])
            recommend_save = {
                'album_link': album_link,
                'album_cover': album_cover,
                'album_desc': album_desc,
                'album_type': album_type,
                'time_stamp': self.time_stamp}
            MongoUtils.updateOrInsert(self.coll_album_recommend, recommend_save)

    # 根据url生成album_type
    def generateAlbumType(self, url):
        if url == self.base_new:
            return 'new'
        elif url == self.base_xinggan:
            return 'xinggan'
        elif url == self.base_shaonv:
            return 'shaonv'
        elif url == self.base_mrxt:
            return 'mrxt'
        elif url == self.base_wmxz:
            return 'wmxz'
        elif url == self.base_wallpaper:
            return 'wallpaper'
        elif url == self.base_swmt:
            return 'swmt'

    @staticmethod
    def code(unicode):
        # replace_reg = re.compile(r'-\d(.*).jpg')
        # url = replace_reg.sub('.jpg', unicode.encode())
        # return url
        return unicode.encode()

    # 检测这个链接是否已经被爬去过了
    def isScrapyIt(self, album_link):
        check = {
            'album_link': album_link
        }
        return MongoUtils.isExistWhole(self.coll_album_whole, check)
