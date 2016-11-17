import scrapy

from spiders.FunnyImageSpider import FunnyImageSpider
from spiders.VideoSpider import VideoSpider
from spiders.OrgSpider import DmozSpider
from spiders.BeautyImageSpider import BeautyImageSpider
from spiders.MeiZhiTuSpider import MeiZhiTuSpider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(VideoSpider)
# process.crawl(MeiZhiTuSpider)
# process.crawl(FunnyImageSpider)
# process.crawl(BeautyImageSpider)
# process.crawl(DmozSpider)
process.start()