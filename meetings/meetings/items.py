# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Articles(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    publishDate = scrapy.Field()
    lastUpdated = scrapy.Field()


class Meetings(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    start_time = scrapy.Field()
    day_available = scrapy.Field()


class MeetingLinks(scrapy.Item):
    links = scrapy.Field()
