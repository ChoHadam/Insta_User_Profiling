# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstacrawlItem(scrapy.Item):
    username = scrapy.Field()
    inner_id = scrapy.Field()
    profile = scrapy.Field()
    follower_cnt = scrapy.Field()
    following_cnt = scrapy.Field()