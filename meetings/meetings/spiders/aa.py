import scrapy
from meetings.items import Links, Meetings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlRespone
# retrieving the title using CSS
# title = response.css('span.title::text').get()

# retrieving the title using xpath
# title = response.xpath('//span[@class="title"]/text()').get()
# the get() method will return one and getall() returns all the
# specified response tags


class AaSpider(CrawlSpider):
    name = 'aa'
    allowed_domains = ['aa-meetings.com']
    start_urls = ['https://www.aa-meetings.com/aa-meeting/']
    # Create regex pattern to follow correct urls
    url_patterns = 'a{2}\-\w+\/((page\/\d*\/$)|(\w*.\w*)*)'
    custom_settings = {
        'FEED_URI': 'meetings.csv',  # This can be json, or xml
        'FEED_FORMAT': 'csv'
    }
    # create rules for the spider to follow
    rules = [Rule(LinkExtractor(allow=url_patterns),
                  callback='parse_info', follow=True)]

    # def start_requests(self, start_urls):
    #     yield self.make_requests_from_url(start_urls)

    def parse_info(self, response):
        # creating a logger:
        self.logger.info("A response from %s was received: ", response.url)
        # --------------------------- Create an Meetngs object ---------------------------- #
        meeting = Meetings()
        meeting['name'] = response.xpath("//div[@class='fui-card-body']//h4//a/text()").getall()
        meeting['address'] = response.xpath("//div[@class='fui-card-body']//address[@class='weight-300']/text()").getall()
        meeting['city'] = response.xpath("//p[@class='weight-300']//a/text()").getall()
        meeting['cityStateZip'] = response.xpath("//div[@class='fui-card-body']/h4/p/text()").getall()
        meeting['locationName'] = response.xpath("//div[@class='fui-card-body']//p/text()").getall()
        meeting['time'] = response.xpath("//table[@class='table fui-table']/td/text()").getall()
        meeting['days'] = response.xpath("//table[@class='table fui-table']/td/text()").getall()
        meeting['type'] = response.xpath("//table[@class='table fui-table']/td/text()").getall()
        meeting['rules'] = response.xpath("//table[@class='table fui-table']/td/text()").getall()

        # get each meetings url
        meeting['url'] = response.url
