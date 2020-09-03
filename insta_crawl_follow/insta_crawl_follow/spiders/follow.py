# 사용한것 -> settting : ROBOTSTXT_OBEY = False (기본세팅은 true였음) , setting 아래것도 건드림 (timesleep 대신 자동으로 스크래피가 활성화)
"""
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 600
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 32.0
"""
# -------------------------item 안쓴 ver -------------------------------------

import time
import scrapy
from tqdm import tqdm
import requests, re, json, urllib, datetime
import pandas as pd
from bs4 import BeautifulSoup



class FollowSpider(scrapy.Spider):
    name = 'follow'
    cnt = 0
    tmp = 0
    headers = {'cookie' : 'ig_did=46DE0419-EFCD-459F-A1C8-543AAD7A837E; mid=XzuGtgALAAFt0YG8Aq3XWbhvJ0gc; csrftoken=gGjx90efuXwVu8CMzPhSjZn2Y20rdiB8; ds_user_id=17901285934; sessionid=17901285934%3ADArEAOlFFJK0gh%3A11; shbid=8668; rur=ASH; shbts=1597999883.7194874; urlgen="{\"2001:e60:9132:b9f9:7929:b07a:6159:a194\": 4766\054 \"222.107.238.125\": 4766}:1kA2FL:56cZuVVM1gYrb9YJTOGL7dAlcyI"',
               'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    # allowed_domains = ['instagram.com']
    # start_urls = ['https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D'.format(insta_id)] # 얘가 파스를 부름~ 이건 스크래피가 만들어놈 
    
    # # extract  
    # def parse(self, response):
        
        
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall(),
    #         }
    
    def start_requests(self):
        insta_ids = pd.read_csv("C:\\Users\\dhsmi\\workspace\\insta\\Insta_User_Profiling\\Insta_Crawling\\User Crawling Data\\20대\\20dae.csv", header=None)
        
        for insta_id in insta_ids[0]:
            # start_id = insta_id
            # yield self.follow_crawl(insta_id)
            first_url = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D".format(insta_id)
            # FollowSpider.cnt += 1
            # if FollowSpider.cnt % 700 == 0 :
            #     time.sleep(500)
            yield scrapy.Request(first_url, callback=self.follow_crawl, headers = FollowSpider.headers, encoding = 'utf-8', meta={'insta_id':insta_id}) # request  첫번째 무조건 url -> d여기 위3줄 다넣기
            # 이거 request랑 같은거임 

    def follow_crawl(self, response): # 이거고정임 
        result_dic = json.loads(response.text)
        insta_id = response.meta['insta_id']
        # follow = []
        # try:
        if result_dic['data']['user']['edge_follow']['page_info']['has_next_page'] == True :
            for i in tqdm(range(len(result_dic['data']['user']['edge_follow']['edges']))):
                # FollowSpider.cnt += 1
                # if FollowSpider.cnt % 700 == 0 :
                #     time.sleep(500)
                yield { "start" : str(insta_id),
                        "end" : result_dic['data']['user']['edge_follow']['edges'][i]['node']['reel']['owner']['id'],
                        'shortcode' : ' ',
                        'relation_type' : 'follow'
                        #"user_name" : result_dic['data']['user']['edge_follow']['edges'][i]['node']['reel']['owner']['username']
                        }                    
            # if cnt % 700 == 0 :
            #     time.sleep(600)
            end_cursor = result_dic['data']['user']['edge_follow']['page_info']['end_cursor']
            after_url = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A13%2C%22after%22%3A%22{}%3D%3D%22%7D".format(insta_id, end_cursor[:-2])
            yield scrapy.Request(after_url, callback=self.follow_crawl, headers = FollowSpider.headers, encoding = 'utf-8', meta={'insta_id':insta_id})
            #cnt += len(result_dic['data']['user']['edge_follow']['edges']) # request 여기서 다시 follow로 
        else:
            print(result_dic['data']['user']['edge_follow']['page_info'])
        # except : 
                # result_dic
        # print(cnt)




#----------------------------------item 쓴 ver------------------------------------
# import scrapy


# import scrapy
# from tqdm import tqdm
# import requests, re, json, urllib, datetime
# import pandas as pd
# from bs4 import BeautifulSoup
# # from instagram.items import InstagramItem


# class InstacrawlSpider(scrapy.Spider):
#     name = 'followcrawl'
#     headers = {'cookie' : 'ig_did=46DE0419-EFCD-459F-A1C8-543AAD7A837E; mid=XzuGtgALAAFt0YG8Aq3XWbhvJ0gc; csrftoken=gGjx90efuXwVu8CMzPhSjZn2Y20rdiB8; ds_user_id=17901285934; sessionid=17901285934%3ADArEAOlFFJK0gh%3A11; shbid=8668; rur=ASH; shbts=1597999883.7194874; urlgen="{\"2001:e60:9132:b9f9:7929:b07a:6159:a194\": 4766\054 \"222.107.238.125\": 4766}:1kA2FL:56cZuVVM1gYrb9YJTOGL7dAlcyI"',
#                         'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
#     # allowed_domains = ['instagram.com']
#     # start_urls = ['https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D'.format(insta_id)] # 얘가 파스를 부름~ 이건 스크래피가 만들어놈 
    
#     # # extract  
#     # def parse(self, response):
        
        
#     #     for quote in response.css('div.quote'):
#     #         yield {
#     #             'text': quote.css('span.text::text').get(),
#     #             'author': quote.css('small.author::text').get(),
#     #             'tags': quote.css('div.tags a.tag::text').getall(),
#     #         }
    
#     def start_requests(self):
#         insta_ids = pd.read_csv("C:\\Users\\dhsmi\\workspace\\insta\\Insta_User_Profiling\\Insta_Crawl\\User Crawling Data\\20대\\20dae.csv", header=None)
        
#         for insta_id in insta_ids[0]:
#             # yield self.follow_crawl(insta_id)
#             first_url = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D".format(insta_id)
#             # res_follow = requests.get(first_url,headers = headers)
#             # res_follow.encoding = 'utf-8'
#             yield scrapy.Request(first_url, callback=self.follow_crawl, headers = InstacrawlSpider.headers, encoding = 'utf-8') # request  첫번째 무조건 url -> d여기 위3줄 다넣기
#             # 이거 request랑 같은거임 






#     def follow_crawl(self, response): # 이거고정임 

#         item = InstagramItem()
#         # headers = {
#         #             'cookie' : 'ig_did=46DE0419-EFCD-459F-A1C8-543AAD7A837E; mid=XzuGtgALAAFt0YG8Aq3XWbhvJ0gc; csrftoken=gGjx90efuXwVu8CMzPhSjZn2Y20rdiB8; ds_user_id=17901285934; sessionid=17901285934%3ADArEAOlFFJK0gh%3A11; shbid=8668; rur=ASH; shbts=1597999883.7194874; urlgen="{\"2001:e60:9132:b9f9:7929:b07a:6159:a194\": 4766\054 \"222.107.238.125\": 4766}:1kA2FL:56cZuVVM1gYrb9YJTOGL7dAlcyI"',
#         #             'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
#         #             }
#         # first_url = "https://www.\instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D".format(insta_id)
#         # res_follow = requests.get(first_url,headers = headers)
#         # res_follow.encoding = 'utf-8'
#         # result_dic = json.loads(res_follow.text)
#         # #follow count
#         # result_dic['data']['user']['edge_follow']['count']
#         result_dic = json.loads(response.text) #★★★★★★★★★★★★여기 res_follow.text였음 
#         cnt = 0
#         follow = []
#         # while True : # has_next_page가 true인동안 
#         try:
#             if result_dic['data']['user']['edge_follow']['page_info']['has_next_page'] == True :
#                 for i in tqdm(range(len(result_dic['data']['user']['edge_follow']['edges']))):
#                     item['id'] = result_dic['data']['user']['edge_follow']['edges'][i]['node']['reel']['owner']['id']
#                     item['user_name'] = result_dic['data']['user']['edge_follow']['edges'][i]['node']['reel']['owner']['username']
#                     yield item
#                 end_cursor = result_dic['data']['user']['edge_follow']['page_info']['end_cursor']
#                 after_url = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A13%2C%22after%22%3A%22{}%3D%3D%22%7D".format(insta_id, end_cursor[:-2])
#                 yield scrapy.Request(after_url, callback=self.follow_crawl, headers = InstacrawlSpider.headers, encoding = 'utf-8')
#                 cnt += len(result_dic['data']['user']['edge_follow']['edges']) # request 여기서 다시 follow로 
#             else:
#                 print(result_dic['data']['user']['edge_follow']['page_info'])
#         except : 
#                 result_dic

