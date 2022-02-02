#!/.venv/bin/activate python3

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from webbot.items import Articles

class MarketnewsSpider(CrawlSpider):
    name = 'marketNews'
    allowed_domains = ['cnbc.com']
    start_urls = ['http://cnbc.com/']

    # ------------ Create regex pattern to follow correct urls ------------ #
    url_pattern = ''

    # --------------- Create custom settings for this spider -------------- #
    custom_settings = {
        'FEED_URI': 'articles.csv',  # This can be json, or xml
        'FEED_FORMAT': 'csv',  # json or xml
        'CLOSESPIDER_PAGECOUNT': 100
    }

    # ---------- I need to create rules for the spider to follow ---------- #
    rules = [Rule(LinkExtractor(), callback='parse_info', follow=True)]

    def parse_info(self, response):
        """Create the items to scrape from each url using xpath"""
        articles = Articles()

        articles['title'] = response.xpath('//h1[@class="ArticleHeader-headline"]/text()')
        articles['url'] = response.url
        articles['author'] = response.xpath('//*[@class="Author-authorName"]/text()')
        articles['body'] = response.xpath('//*[@id="RegularArticle-ArticleBody-5"]/div//p/text()')
        # articles['publishDate'] = response.xpath()
        # articles['lastUpdated'] = response.xpath()

