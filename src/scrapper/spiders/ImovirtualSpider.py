import scrapy
import re

class ImovirtualSpider(scrapy.Spider):
    
    name = 'ImovirtualSpider'
    allowed_domains = ['imovirtual.com']
    start_urls = ['https://www.imovirtual.com/en/comprar/apartamento/lisboa/?search%5Bregion_id%5D=11&search%5Bsubregion_id%5D=153&page={page}']

    def start_requests(self):
        
        #each start_url has pagination, so is a double for-loop
        for url in self.start_urls:
            page = 1
            while(page<2):
                parsed_url = url.format(page=page)
                page += 1
                try:
                    yield scrapy.Request(parsed_url, self.parse)
                except ValueError:
                    break
    
    def getFromIndex(self, src, idx, callback=None):
        if(callback is None):
            return None if (len(src) <= idx) else src[idx]
        else:
            return None if (len(src) <= idx) else callback(src[idx])
        


    def parse(self, response):

        # Regex callbacks
        get_extracting_lambda = lambda pattern: lambda x: pattern.findall(x)[0]
        get_join_extracting_lambda = lambda pattern: lambda x: ''.join(pattern.findall(x))

        # Regex lambdas
        pattern_start_with_numbers = get_extracting_lambda(re.compile('^\d+'))
        pattern_get_numbers = get_extracting_lambda(re.compile('\d+'))
        pattern_get_price = get_join_extracting_lambda(re.compile('(\d+){1,3}'))

        articles = response.xpath("//article")
        for article in articles:
            id = self.getFromIndex(article.xpath("./@data-item-id").extract(), 0)
            title = self.getFromIndex(article.xpath(".//span[@class = 'offer-item-title']/text()").extract(), 0)
            tipology = self.getFromIndex(article.xpath(".//li[contains(@class, 'offer-item-rooms')]/text()").extract(),0, pattern_get_numbers)
            area = self.getFromIndex(article.xpath(".//li[contains(@class, 'offer-item-area')]/text()").extract(),0, pattern_start_with_numbers)
            price = self.getFromIndex(article.xpath(".//li[contains(@class, 'offer-item-price')]/text()").extract(),0, pattern_get_price)
            bathroom = self.getFromIndex(article.xpath(".//ul[contains(@class, 'parameters-view')]/li[contains(text(),'Bath')]/text()").extract(),0, pattern_get_numbers)

            yield {
                'srcID': id,
                'title': title,
                'tipology': tipology,
                'area': area,
                'area_unit': 'sqm',
                'price': price,
                'bathroom': bathroom,
            }