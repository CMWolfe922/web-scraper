import scrapy


class AaSpider(scrapy.Spider):
    name = 'aa'
    allowed_domains = ['aa-meetings.com']
    start_urls = ['http://aa-meetings.com/']

    def parse(self, response):
        pass
