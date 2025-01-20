# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SkiscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    country = scrapy.Field()
    description = scrapy.Field()
    elevation = scrapy.Field()
    slopes = scrapy.Field()
    ski-lift = scrapy.Field()
    prices = scrapy.Field()
    pass
