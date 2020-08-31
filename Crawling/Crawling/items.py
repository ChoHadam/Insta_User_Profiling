# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaCrawlingUserPost(scrapy.Item):
    inner_id = scrapy.Field()
    team_idx = 1
    post_date = scrapy.Field()
    view_count = scrapy.Field()
    like_count = scrapy.Field()
    crawling_time = scrapy.Field()
    media_url = scrapy.Field()
    content = scrapy.Field()
    post_id = scrapy.Field()
    url = scrapy.Field()
    hashtag = scrapy.Field()
    insta_id = scrapy.Field()
    location = scrapy.Field()
