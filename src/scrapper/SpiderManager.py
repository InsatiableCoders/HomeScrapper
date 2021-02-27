#local dependencies
from .spiders import ImovirtualSpider

#external dependencies
import scrapy
from scrapy import signals
from scrapy.crawler import Crawler, CrawlerProcess


class SpiderManager():

    crawlerProcess = None

    #spiders
    spiders_to_execute = []
    spiders = {
        "Imovirtual": ImovirtualSpider.ImovirtualSpider
    }


    def __init__(self, args):
        
        #Instanciate Scrapy's Crawler
        self.crawlerProcess = CrawlerProcess()

        #import spiders 
        for arg in args:
            self.getSpider(arg)


    #Function responsible to read argument and import instance of correspondent Spider
    def getSpider(self, arg):

        spider = self.spiders.get(arg, None)

        if(spider is not None):
            self.spiders_to_execute.append(spider)

    #Function to be called after __init__ is completed
    def execute(self, consumer):
        
        for spider in self.spiders_to_execute:

            def collect_items(item, response, spider):
                consumer.collect(spider.name, item)

            crawler = Crawler(spider)
            crawler.signals.connect(collect_items, signals.item_scraped)

            process = CrawlerProcess()
            process.crawl(crawler)
            process.start()  ## <-- LOCKING

            consumer.inbox_status() ## <-- LOCKING
            consumer.output_inbox() ## <-- LOCKING
