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
    url_cnt = 0
    cnt = 0
    tmp = 0
    headers = {'cookie' : 'ig_did=46DE0419-EFCD-459F-A1C8-543AAD7A837E; mid=XzuGtgALAAFt0YG8Aq3XWbhvJ0gc; ds_user_id=17901285934; sessionid=17901285934%3AUofQA5vp9nIicG%3A6; csrftoken=gGjx90efuXwVu8CMzPhSjZn2Y20rdiB8; shbid="8668\05417901285934\0541630992652:01f7252b8131a7e61dc5808de90c4907001efd25d95792a0c6b75abf1221811863147d7a"; shbts="1599456652\05417901285934\0541630992652:01f70b2fec7b9d00ff9e6eabd9700f1c5bb464c6e66b6c87dd1f2001db5b2d8fee09a4ba"; urlgen="{\"2001:e60:9222:dc8:c0e1:488:c19:4d38\": 4766\054 \"2001:e60:8734:7198:35c3:105d:76d7:7a66\": 4766\054 \"222.111.18.10\": 4766}:1kFwfS:mSZedRO0bGagCdzc7RKlh7zONGs"; rur="FTW\05417901285934\0541631180730:01f767b99037dc97511d3356a96b6d8fc3d7a1a09ec96efbd05781077e7641b6f25b3259"',
               'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    
    def start_requests(self):
        insta_ids = pd.read_csv("C:\\Users\\dhsmi\\Downloads\\40_50_total.csv", header=None)
        # insta_ids = [1743531606]
        # 인용 파일 받아올떄 insta_ids = pd.read_csv("C:\\Users\\dhsmi\\Downloads\\sipdae_profile.csv") + for insta_id in insta_ids['inner_id'] :

        for insta_id in insta_ids[0]:
            first_url = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A24%7D".format(insta_id)
            yield scrapy.Request(first_url, callback=self.follow_crawl, headers = FollowSpider.headers, encoding = 'utf-8', meta={'insta_id':insta_id}) # request  첫번째 무조건 url -> d여기 위3줄 다넣기
            FollowSpider.url_cnt += 1
            if FollowSpider.url_cnt % 100 == 0 :
                time.sleep(300)
                print("■■■■■■■■■■■■■■■■■■■url 카운팅■■■■■■■■■■■■■■■■■■■■■■")

    def follow_crawl(self, response): # 이거고정임 
        result_dic = json.loads(response.text)
        insta_id = response.meta['insta_id']
        # try:
        FollowSpider.cnt += 1
        if FollowSpider.cnt % 1500 == 0 :
            time.sleep(300)
        if result_dic['status'] == "ok":
            print("■■■■■■■■■■■■■■■■■■■status ok 카운팅■■■■■■■■■■■■■■■■■■■■■■")
            if result_dic['data']['user']['edge_follow']['page_info']['has_next_page'] == False :
                for i in tqdm(range(len(result_dic['data']['user']['edge_follow']['edges']))):
                    FollowSpider.cnt += 1
                    print("■■■■■■■■■■■■■■■■■■■False 카운팅■■■■■■■■■■■■■■■■■■■■■■")
                    if FollowSpider.cnt % 1500 == 0 :
                        time.sleep(300)
                    
                    yield { "start" : str(insta_id),
                            "end" : result_dic['data']['user']['edge_follow']['edges'][i]['node']['reel']['owner']['id'],
                            'relation_type' : 'follow',
                            'shortcode' : ' ' 
                            #"user_name" : result_dic['data']['user']['edge_follow']['edges'][i]['node']['reel']['owner']['username']
                            }
                            
            
            elif result_dic['data']['user']['edge_follow']['page_info']['has_next_page'] == True :
                for i in tqdm(range(len(result_dic['data']['user']['edge_follow']['edges']))):
                    FollowSpider.cnt += 1
                    print("■■■■■■■■■■■■■■■■■■■True 카운팅■■■■■■■■■■■■■■■■■■■■■■")
                    if FollowSpider.cnt % 1500 == 0 :
                        time.sleep(300)
                    yield { "start" : str(insta_id),
                            "end" : result_dic['data']['user']['edge_follow']['edges'][i]['node']['reel']['owner']['id'],
                            'relation_type' : 'follow',
                            'shortcode' : ' ' 
                            #"user_name" : result_dic['data']['user']['edge_follow']['edges'][i]['node']['reel']['owner']['username']
                            }                               
                end_cursor = result_dic['data']['user']['edge_follow']['page_info']['end_cursor']
                # FollowSpider.cnt += 1
                # if FollowSpider.cnt % 1000 == 0 :
                #     time.sleep(300)
                
                after_url = "https://www.instagram.com/graphql/query/?query_hash=d04b0a864b4b54837c0d870b0e77e076&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Afalse%2C%22first%22%3A13%2C%22after%22%3A%22{}%3D%3D%22%7D".format(insta_id, end_cursor[:-2])
                yield scrapy.Request(after_url, callback=self.follow_crawl, headers = FollowSpider.headers, encoding = 'utf-8', meta={'insta_id':insta_id})
                
            else:
                print("뭔가 이상합니다")    
                # print(result_dic['data']['user']['edge_follow']['page_info'])
        else :   
            print("■■■■■■■■■■■■■■■■■■■Status fail 카운팅■■■■■■■■■■■■■■■■■■■■■■")         
            time.sleep(300)
            # 그다음 뭔가 처리해줘야할것가튼데... 





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

