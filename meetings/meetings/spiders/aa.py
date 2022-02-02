import scrapy


class AaSpider(scrapy.Spider):
    name = 'aa'
    allowed_domains = ['aa-meetings.com']
    start_urls = ['http://aa-meetings.com/']

    def parse(self, response):
        """this will parse the website data and return whatever data
        we specify using either a css selector or xpath  selector.

        the get() method will return one and getall() returns all the
        specified response tags"""
        # retrieving the title using CSS
        # title = response.css('span.title::text').get()

        # retrieving the title using xpath
        title = response.xpath('//span[@class="title"]/text()').get()

        title = response.xpath()
        return {"title": title}
