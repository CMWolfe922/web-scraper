import scrapy
from meetings.items import MeetingLinks, aaMeetings


class AaSpider(scrapy.Spider):
    name = 'aa'
    allowed_domains = ['aa-meetings.com']
    start_urls = ['http://aa-meetings.com/']

    def parse(self, response):
        """this will parse the website data and return whatever data
        we specify using either a css selector or xpath  selector.

        the get() method will return one and getall() returns all the
        specified response tags"""
        # creating a logger:
        self.logger.info("A response from %s just arrived!", response.url)
        # retrieving the title using CSS
        # title = response.css('span.title::text').get()

        # retrieving the title using xpath
        # title = response.xpath('//span[@class="title"]/text()').get()

        # get links to each state:
        state_links = response.xpath(
            '//div[@class="col-md-3 col-6 single-item"]//a/@href').getall()

        # create for loop to store items
        for link in state_links:
            yield MeetingLinks(links=link)
