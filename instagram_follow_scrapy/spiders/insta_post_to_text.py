import scrapy
from tqdm import tqdm
import requests, re, json, urllib, datetime
import pandas as pd
from bs4 import BeautifulSoup


class InstaPostToTextSpider(scrapy.Spider):
    name = 'textcrawl'
    headers = {'cookie' : 'ig_did=46DE0419-EFCD-459F-A1C8-543AAD7A837E; mid=XzuGtgALAAFt0YG8Aq3XWbhvJ0gc; csrftoken=gGjx90efuXwVu8CMzPhSjZn2Y20rdiB8; ds_user_id=17901285934; sessionid=17901285934%3ADArEAOlFFJK0gh%3A11; shbid=8668; rur=ASH; shbts=1597999883.7194874; urlgen="{\"2001:e60:9132:b9f9:7929:b07a:6159:a194\": 4766\054 \"222.107.238.125\": 4766}:1kA2FL:56cZuVVM1gYrb9YJTOGL7dAlcyI"',
                        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
    

    # id -> post 
    def start_requests(self):
        insta_ids = pd.read_csv("C:\\Users\\dhsmi\\workspace\\insta\\Insta_User_Profiling\\Insta_Crawl\\User Crawling Data\\20대\\20dae.csv", header=None)
        # start_id = [] 
        for insta_id in insta_ids[0]:
            # yield self.follow_crawl(insta_id)
            # self.start_id = insta_id
            first_url = "https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A12%7D".format(insta_id)
            # res_follow = requests.get(first_url,headers = headers)
            # res_follow.encoding = 'utf-8'
            yield scrapy.Request(first_url, callback=self.post_crawl, headers = InstacrawlSpider.headers, encoding = 'utf-8') # request  첫번째 무조건 url -> d여기 위3줄 다넣기
            # 이거 request랑 같은거임 
    
    def post_crawl(self, response): # 이거고정임 
        result_dic = json.loads(response.text)
        post_cnt = 0
        short_code_list = []
        # while True : # has_next_page가 true인동안 
        try:
            if result_dic['data']['user']["edge_owner_to_timeline_media"]["page_info"]["has_next_page"] == True :
                for i in tqdm(range(len(result_dic['data']['user']["edge_owner_to_timeline_media"]["edges"]))):
                    yield {
                            "short_code" : result_dic['data']['user']["edge_owner_to_timeline_media"]["edges"][i]['node']['shortcode']
                            }    

                 #이거 for문 안의 yield 아래 넣어야할것같은데 .. 같이돌면 바뀔듯 하기도 ..    
                to_comment_url = "https://www.instagram.com/graphql/query/?query_hash=2418469a2b4d9b47ae7bec08e3ec53ad&variables=%7B%22shortcode%22%3A%22{}%22%2C%22child_comment_count%22%3A3%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22has_threaded_comments%22%3Atrue%7D".format(short_code)
                yield scarpy.Request(to_commnet_url, callback = self.commnet_crawl, headers = InstacrawlSpider.headers, encoding = 'utf-8')
                end_cursor = result_dic['data']['user']["edge_owner_to_timeline_media"]["page_info"]['end_cursor']
                # has_next_page = result_dic['data']['user']['edge_follow']['page_info']['has_next_page']
                after_url = "https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B%22id%22%3A%22{}%22%2C%22first%22%3A12%2C%22after%22%3A%22{}%3D%3D%22%7D".format(insta_id, end_cursor[:-2])
                yield scrapy.Request(after_url, callback=self.post_crawl, headers = InstacrawlSpider.headers, encoding = 'utf-8')
                post_cnt += len(result_dic['data']['user']["edge_owner_to_timeline_media"]["edges"])
            else:
                print(result_dic['data']['user']["edge_owner_to_timeline_media"]["page_info"]["has_next_page"])
                break
        except : 
                # result_dic['data']['user']['edge_follow']['page_info']['has_next_page']
                result_dic
        
        # #이거 for문 안의 yield 아래 넣어야할것같은데 .. 같이돌면 바뀔듯 하기도 .. 
        # to_comment_url = "https://www.instagram.com/graphql/query/?query_hash=2418469a2b4d9b47ae7bec08e3ec53ad&variables=%7B%22shortcode%22%3A%22{}%22%2C%22child_comment_count%22%3A3%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22has_threaded_comments%22%3Atrue%7D".format(short_code)
        # yield scarpy.Request(to_commnet_url, callback = self.commnet_crawl, headers = InstacrawlSpider.headers, encoding = 'utf-8')
        

    def comment_crawl(self, response):
        result_dic = json.loads(response.text)
        comment_cnt = 0
        
        for k in range(len(short_code)):
            short_code = short_code_list[k]['short_code']
            start_url = "https://www.instagram.com/graphql/query/?query_hash=2418469a2b4d9b47ae7bec08e3ec53ad&variables=%7B%22shortcode%22%3A%22{}%22%2C%22child_comment_count%22%3A3%2C%22fetch_comment_count%22%3A40%2C%22parent_comment_count%22%3A24%2C%22has_threaded_comments%22%3Atrue%7D".format(short_code)
            res = requests.get(start_url,headers = headers)
            res.encoding = 'utf-8'
            result_dic = json.loads(res.text)
            print(result_dic['data']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']) # 자기글
            for i in range(len(result_dic['data']['shortcode_media']["edge_media_to_parent_comment"]['edges'])):
                print(result_dic['data']['shortcode_media']["edge_media_to_parent_comment"]['edges'][i]['node']['text']) #댓글
                for j in range(len(result_dic['data']['shortcode_media']["edge_media_to_parent_comment"]['edges'][i]['node']['edge_threaded_comments']['edges'])):
                    print(result_dic['data']['shortcode_media']["edge_media_to_parent_comment"]['edges'][i]['node']['edge_threaded_comments']['edges'][j]['node']['text'])


