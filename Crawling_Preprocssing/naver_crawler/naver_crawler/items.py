# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NaverCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    media = scrapy.Field()
    body = scrapy.Field()
    time = scrapy.Field()
    pass
