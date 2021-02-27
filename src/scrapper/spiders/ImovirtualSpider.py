import scrapy

class ImovirtualSpider(scrapy.Spider):
    
    name = 'ImovirtualSpider'
    allowed_domains = ['imovirtual.com']
    start_urls = ['https://www.imovirtual.com/en/comprar/apartamento/lisboa/?search%5Bregion_id%5D=11&search%5Bsubregion_id%5D=153']

    def start_requests(self):
        
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse)
    

    def parse(self, response):

        for itemTitle in response.xpath("//span[@class = 'offer-item-title']/text()").getall():
            yield {'title': itemTitle}