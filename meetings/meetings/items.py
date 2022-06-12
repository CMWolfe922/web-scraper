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
    # cityStateZip = scrapy.Field()
    # locationName = scrapy.Field()
    # meeting_info = scrapy.Field()
    # I don't think I need the same exact xpath for all these
    # items because each one just returns the same thing
    # days = scrapy.Field()
    # type = scrapy.Field()
    # rules = scrapy.Field()
    url = scrapy.Field()


class Links(scrapy.Item):
    links = scrapy.Field()
