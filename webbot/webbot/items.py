# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Articles(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    publishDate = scrapy.Field()
    lastUpdated = scrapy.Field()

class LinkedinItem(scrapy.Item):
    username = scrapy.Field()
    post_url = scrapy.Field()
    post_likes = scrapy.Field()
