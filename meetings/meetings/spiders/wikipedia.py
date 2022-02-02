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
