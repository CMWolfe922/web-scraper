#!/.venv/bin/activate python3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from meetings.items import Articles


class WikipediaSpider(CrawlSpider):
    name = 'wikipedia'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Kevin_Bacon']

    # -------------------- Create regex pattern to follow correct urls -------------------- #
    url_pattern = 'wiki/((?!:).)*$'

    # ---------------------- Create custom settings for this spider ----------------------- #
    custom_settings = {
        'FEED_URI': 'articles.csv',  # This can be json, or xml
        'FEED_FORMAT': 'csv',  # json or xml
        'CLOSESPIDER_PAGECOUNT': 10
    }
    # ------------------ I need to create rules for the spider to follow ------------------ #
    rules = [Rule(LinkExtractor(allow=url_pattern),
                  callback='parse_info', follow=True)]

    # --------------- Create parse_info method to extract specific web data --------------- #
    def parse_info(self, response):
        # --------------------------- Create an Article object ---------------------------- #
        article = Articles()

        # The i is for italicized because movie and article titles are italicized
        article['title'] = response.xpath(
            '//h1/text()').get() or response.xpath('//h1/i/text()').get()

        article['url'] = response.url

        article['lastUpdated'] = response.xpath(
            '//li[@id="footer-info-lastmod"]/text()').get()



import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        item = scrapy.Item()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').get()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').get()
        item['link_text'] = response.meta['link_text']
        url = response.xpath('//td[@id="additional_data"]/@href').get()
        return response.follow(url, self.parse_additional_page, cb_kwargs=dict(item=item))

    def parse_additional_page(self, response, item):
        item['additional_data'] = response.xpath('//p[@id="additional_data"]/text()').get()
        return item