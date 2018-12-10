# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class File(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    info = scrapy.Field()
    _bytes = scrapy.Field()
    lines = scrapy.Field()
    filename = scrapy.Field()
    file_extension = scrapy.Field()
    path = scrapy.Field()
    repository = scrapy.Field()
    full_path = scrapy.Field()