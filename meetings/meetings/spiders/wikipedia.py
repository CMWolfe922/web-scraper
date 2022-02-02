#!/.venv/bin/activate python3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class WikipediaSpider(CrawlSpider):
    name = 'wikipedia'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Kevin_Bacon']

    # -------------------- Create regex pattern to follow correct urls -------------------- #
    url_pattern = 'wiki/((?!:).)*$'

    # ------------------ I need to create rules for the spider to follow ------------------ #
    rules = [Rule(LinkExtractor(allow=url_pattern),
                  callback='parse_info', follow=True)]

    # --------------- Create parse_info method to extract specific web data --------------- #
    def parse_info(self, response):
        return {
            # The i is for italicized because movie and article titles are italicized
            'title': response.xpath('//h1/text()').get() or response.xpath('//h1/i/text()').get(),
            'url': response.url,
            'last_edited': response.xpath('//li[@id="footer-info-lastmod"]/text()').get()
        }
