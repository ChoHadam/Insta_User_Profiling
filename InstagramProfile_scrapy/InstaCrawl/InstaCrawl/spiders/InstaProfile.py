import re, requests, json, urllib, datetime, scrapy
import pandas as pd
from InstaCrawl.items import InstacrawlItem

class InstaProfileSpider(scrapy.Spider):
    name = 'insta_profile'
    # allowed_domains = ['instagram.com']
    # start_urls = ['http://instagram.com/']
    url_format = 'https://www.instagram.com/graphql/query/?query_hash=d4d88dc1500312af6f937f7b804c68c3&variables=%7B%22user_id%22%3A%22{0}%22%2C%22include_chaining%22%3Afalse%2C%22include_reel%22%3Atrue%2C%22include_suggested_users%22%3Atrue%2C%22include_logged_out_extras%22%3Afalse%2C%22include_highlight_reels%22%3Afalse%2C%22include_live_status%22%3Atrue%7D'
    # crawling_count = 0
    def __init__(self, file):
        user_id = list(pd.read_csv(file, header=None)[0])
        self.start_urls = []
        for user in user_id:
            self.start_urls.append(InstaProfileSpider.url_format.format(user))

    def parse(self, response):
        result_dic = json.loads(response.text)
        item = InstacrawlItem()
        # for i in range(len(result_dic['data']['user']['reel']['user']['username'])):
        #     # 크롤링 횟수 카운트
        #     # self.crawling_count  += 1
        #     # if self.crawling_count > 200:
        #     #     time.sleep(300)

        print("*"*50)
        print(result_dic['data']['user']['reel']['user']['username'])
        print(type(result_dic['data']['user']['reel']['user']['username']))
        item['login_id'] = result_dic['data']['user']['reel']['user']['username']

        response_profile = requests.get('https://www.instagram.com/{}/?__a=1'.format(result_dic['data']['user']['reel']['user']['username']))
        json2 = json.loads(response_profile.text)

        item['profile'] = json2['graphql']['user']['biography']
        item['follower_cnt'] = json2['graphql']['user']['edge_followed_by']['count']
        item['following_cnt'] = json2['graphql']['user']['edge_follow']['count']

        yield item
