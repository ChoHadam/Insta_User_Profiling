
import scrapy
from tqdm import tqdm
import requests, re, json, urllib, datetime
import pandas as pd
from bs4 import BeautifulSoup
import time

# # ----------------------------  현민이의 init ver ---------------------------------
# class FollowerSpider(scrapy.Spider):
#     name = 'follower'
#     headers = {'cookie' : 'ig_did=46DE0419-EFCD-459F-A1C8-543AAD7A837E; mid=XzuGtgALAAFt0YG8Aq3XWbhvJ0gc; csrftoken=gGjx90efuXwVu8CMzPhSjZn2Y20rdiB8; ds_user_id=17901285934; sessionid=17901285934%3ADArEAOlFFJK0gh%3A11; shbid=8668; rur=ASH; shbts=1597999883.7194874; urlgen="{\"2001:e60:9132:b9f9:7929:b07a:6159:a194\": 4766\054 \"222.107.238.125\": 4766}:1kA2FL:56cZuVVM1gYrb9YJTOGL7dAlcyI"',
#                'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
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
#         # start_id = [] 
#         for insta_id in insta_ids[0]:
#             # yield self.follow_crawl(insta_id)
#             self.start_id = insta_id
#             first_url = "https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D".format(insta_id)
#             # res_follow = requests.get(first_url,headers = headers)
#             # res_follow.encoding = 'utf-8'
#             yield scrapy.Request(first_url, callback=self.follower_crawl, headers = InstacrawlSpider.headers, encoding = 'utf-8') # request  첫번째 무조건 url -> d여기 위3줄 다넣기
#             # 이거 request랑 같은거임 



#     def follower_crawl(self, response): # 이거고정임 
#         result_dic = json.loads(response.text)
#         cnt = 0
#         follower = []
#         # while True : # has_next_page가 true인동안 
#         try:
#             if result_dic['data']['user']['edge_followed_by']['page_info']['has_next_page'] == True :
#                 for i in range(len(result_dic['data']['user']['edge_followed_by']['edges'])):
#                     yield { "start_id" : self.start_id,
#                             "id" : result_dic['data']['user']['edge_followed_by']['edges'][i]['node']['reel']['owner']['id'], 
#                             "user_name" : result_dic['data']['user']['edge_followed_by']['edges'][i]['node']['reel']['owner']['username']}
#                 end_cursor = result_dic['data']['user']['edge_followed_by']['page_info']['end_cursor']
#                 after_url = "https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A20%2C%22after%22%3A%22{}%3D%3D%22%7D".format(insta_id, end_cursor[:-2])
#                 yield scrapy.Request(after_url, callback=self.follower_crawl, headers = InstacrawlSpider.headers, encoding = 'utf-8')
#                 cnt += len(result_dic['data']['user']['edge_followed_by']['edges']) # request 여기서 다시 follow로 
#             else:
#                 print(result_dic['data']['user']['edge_followed_by']['page_info'])
#         except : 
#                 result_dic



#---------------------------------------self 그냥 넣기 ver-----------------------------------------------

class FollowerSpider(scrapy.Spider):
    name = 'follower'
    headers = {'cookie' : 'ig_did=46DE0419-EFCD-459F-A1C8-543AAD7A837E; mid=XzuGtgALAAFt0YG8Aq3XWbhvJ0gc; csrftoken=gGjx90efuXwVu8CMzPhSjZn2Y20rdiB8; ds_user_id=17901285934; sessionid=17901285934%3ADArEAOlFFJK0gh%3A11; shbid=8668; rur=ASH; shbts=1597999883.7194874; urlgen="{\"2001:e60:9132:b9f9:7929:b07a:6159:a194\": 4766\054 \"222.107.238.125\": 4766}:1kA2FL:56cZuVVM1gYrb9YJTOGL7dAlcyI"',
               'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    cnt = 0
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
        # start_id = [] 
        for insta_id in insta_ids[0]:
            # yield self.follow_crawl(insta_id)
            # self.start_id = insta_id
            first_url = "https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D".format(insta_id)
            # res_follow = requests.get(first_url,headers = headers)
            # res_follow.encoding = 'utf-8'
            FollowerSpider.cnt += 1
            if FollowerSpider.cnt % 1000 == 0 :
                time.sleep(600)
            yield scrapy.Request(first_url, callback=self.follower_crawl, headers = FollowerSpider.headers, encoding = 'utf-8', meta={'insta_id':insta_id}) # request  첫번째 무조건 url -> d여기 위3줄 다넣기
            # 이거 request랑 같은거임 







    def follower_crawl(self, response): # 이거고정임 
        result_dic = json.loads(response.text)
        # cnt = 0
        insta_id = response.meta['insta_id']
        # follower = []
        # while True : # has_next_page가 true인동안 
        try:
            if result_dic['data']['user']['edge_followed_by']['page_info']['has_next_page'] == True :
                for i in range(len(result_dic['data']['user']['edge_followed_by']['edges'])):
                    FollowerSpider.cnt += 1
                    if FollowerSpider.cnt % 1000 == 0 :
                        time.sleep(600)
                    yield { 
                            "start" : str(insta_id),
                            "end" : result_dic['data']['user']['edge_followed_by']['edges'][i]['node']['reel']['owner']['id'], 
                            "relation_type" : "follow",
                            # "shortcode" : ''
                            #"user_name" : result_dic['data']['user']['edge_followed_by']['edges'][i]['node']['reel']['owner']['username']
                            }
                end_cursor = result_dic['data']['user']['edge_followed_by']['page_info']['end_cursor']
                after_url = "https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A20%2C%22after%22%3A%22{}%3D%3D%22%7D".format(insta_id, end_cursor[:-2])
                yield scrapy.Request(after_url, callback=self.follower_crawl, headers = FollowerSpider.headers, encoding = 'utf-8', meta={'insta_id':insta_id})
                cnt += len(result_dic['data']['user']['edge_followed_by']['edges']) # request 여기서 다시 follow로 
            else:
                print(result_dic['data']['user']['edge_followed_by']['page_info'])
        except : 
                print(result_dic)


