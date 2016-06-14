# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StoppedCategoryItem(scrapy.Item):
    at = scrapy.Field()
    industry = scrapy.Field()
    pageno = scrapy.Field()


class CandidateItem(scrapy.Item):
    name = scrapy.Field()
    email = scrapy.Field()


class LastProcessedItem(scrapy.Item):
    cookiejar = scrapy.Field()
    pageno = scrapy.Field()
    industry = scrapy.Field()