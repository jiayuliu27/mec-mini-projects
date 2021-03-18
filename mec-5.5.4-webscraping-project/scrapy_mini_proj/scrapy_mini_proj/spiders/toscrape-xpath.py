import scrapy

class ScraperXpath(scrapy.Spider):
    name = 'toscrape-xpath'

    start_urls = [
        'http://quotes.toscrape.com',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class = "quote"]'):
            yield {
                'text': quote.xpath('//span/text()').get(),
                'author': quote.xpath('//small[@class = "author"]/text()').get(),
                'tags': quote.xpath('//div[@class = "tags"]/a[@class = "tag"]/text()').getall(),
            }
    