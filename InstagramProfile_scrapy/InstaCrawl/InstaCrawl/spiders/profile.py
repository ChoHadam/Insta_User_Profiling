import re, requests, json, urllib, datetime, scrapy, time
import pandas as pd
from InstaCrawl.items import InstacrawlItem
# from InstaCrawl.middlewares import TooManyRequestsRetryMiddleware

class InstaProfileSpider(scrapy.Spider):
    name = 'profile'
    headers = { 'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
                }

    headers = { "x-instagram-gis": "ad034c3799ec2a9b083be2bbb257ffec",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",}
             

    cookies = {'ig_did':'6A142BE8-A4FA-4BCB-A15F-C41E2F7CF2BA',
    'mid': 'Xz9q9wALAAHsdxymIjepqNOBeS-k', 
    'fbm_124024574287414':'base_domain=.instagram.com',
    'shbid':'8668\0546769785738\0541630507157:01f74fd177d1c380175ef3524de37ad2fa9b454e45db764f6d83432dbd55664cde4285dc',
    'shbts':'1598971157\0546769785738\0541630507157:01f7a3b0b0ebae54cbee5f000f895f0ca63c685fa75f0b4b1562192068a2aa58ad794b30', 
    'csrftoken':'F7NFJ4LI2PfrKsuoZ7r50sfuJYTh7UEC', 
    'ds_user_id': '40522214037; sessionid=40522214037%3AX7mewGdkcbhJdg%3A6',
    'rur':'VLL\05440522214037\0541630547219:01f73e9a04ab794a0aadf6dc1a3489b97c65db51dec5338cee6278821057322646fc586e',
    'urlgen':'{\"211.201.31.104\": 9318}:1kDHrX:OlPxhUGurPPaaZbyp0fhkyj-wjQ'}

    # headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

    # cookies = {'ig_did' : '163B7911-4E71-4B66-8D0F-667BBC63BE31', 
    # 'mid' : 'X00kegALAAGzZJLgu2_D7CBeq6gS',
    # 'csrftoken' : '9FuY9Z957HjM8iSzkxSFzUY0pCgh9ZnL',
    # 'ds_user_id' : '6769785738', 
    # 'sessionid' : '6769785738%3Aewkugly0ohNTr9%3A18',
    # 'shbid':'8668\0546769785738\0541630676199:01f7175d122ea7166af19803815e916273c54b861d8f8c4bfd5430faf679517e8fb36a7a',
    # 'shbts':'1599140199\0546769785738\0541630676199:01f79cccee006b8a124538894fc5d66fe3c8360e65590ec7802e81ae52f37d610b7b73d5',
    # 'urlgen' : '{\"211.201.31.104\": 9318}:1kDpQ1:dcO6d47WuGr8j8o3Y5uXUtYAhX8',
    # 'rur' : 'VLL\0546769785738\0541630676209:01f7ec2699b3cd8963e7b24bb7e5ea02d4f1c04158533142096cd11685335062a658e566'}

    # allowed_domains = ['instagram.com']
    # start_urls = ['http://instagram.com/']
    # url_format = 'https://www.instagram.com/{0}/?__a=1'
    crawling_count = 0
    def __init__(self,file):
        # insta_ids = list(pd.read_csv(file, header=None)[0])
        insta_ids = list(pd.read_json(file)['username'])
        first_url = 'https://www.instagram.com/{0}/?__a=1'
        self.urls = []
        for insta_id in insta_ids:
            self.urls.append(first_url.format(insta_id))


    def start_requests(self) :
        for url in self.urls :
            yield scrapy.Request(url=url, headers=InstaProfileSpider.headers, callback=self.parse)


    def parse(self, response):
        #print(response.text)
        result_dic = json.loads(response.text)
        item = InstacrawlItem()
        self.crawling_count  += 1
        if self.crawling_count % 200 == 0:
            time.sleep(700)

        #print("*"*50)
        #print(result_dic['graphql']['user']['username'])
        #print(result_dic['graphql']['user']['biography'])
        item['username'] = result_dic['graphql']['user']['username']
        item['profile'] = result_dic['graphql']['user']['biography']
        item['follower_cnt'] = result_dic['graphql']['user']['edge_followed_by']['count']
        item['following_cnt'] = result_dic['graphql']['user']['edge_follow']['count']

        yield item