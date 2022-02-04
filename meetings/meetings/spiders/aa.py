import scrapy
from meetings.items import MeetingLinks, Meetings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from meetings.items import Meetings

class AaSpider(CrawlSpider):
    name = 'aa'
    allowed_domains = ['aa-meetings.com']
    start_urls = ['https://www.aa-meetings.com/aa-meeting/']

    url_patterns = 'aa-meetings/'

    def start_requests(self):
        yield self.make_requests_from_url("https://www.aa-meetings.com/aa-meeting/")

    hxs = HtmlXPathSelector(response)
    def parse_info(self, response):
        """this will parse the website data and return whatever data
        we specify using either a css selector or xpath  selector.

        the get() method will return one and getall() returns all the
        specified response tags"""

        # creating a logger:
        self.logger.info("A response from %s was received: ", response.url)
    # ---------------------- Create custom settings for this spider ----------------------- #
        custom_settings = {
            'FEED_URI': 'meetings.csv',  # This can be json, or xml
            'FEED_FORMAT': 'csv',  # json or xml
            'CLOSESPIDER_PAGECOUNT': 10
        }
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
