import scrapy, re, time, datetime, urllib, json
import pandas as pd
from Crawling.items import InstaCrawlingUserPost

class InstaCralwingSpider(scrapy.Spider):
    name = 'insta_post'
    # allowed_domains = ['instagram.com']
    # start_urls = ['http://instagram.com/']
    url_format = 'https://www.instagram.com/graphql/query/?query_hash=bfa387b2992c3a52dcbe447467b4b771&variables=%7B"id"%3A"{0}"%2C"first"%3A12'
    next_page = '%2C"after"%3A"{0}"'
    url_end = '%7D'
    crawling_count = 0

    def __init__(self, file):
        user_id = list(pd.read_csv(file, header=None)[0])
        
        self.start_urls = []
        for user in user_id:
            self.start_urls.append(InstaCralwingSpider.url_format.format(user) + InstaCralwingSpider.url_end)

    def parse(self, response):
        jason = response.json()
        item = InstaCrawlingUserPost()
        for i in range(len(jason['data']['user']['edge_owner_to_timeline_media']['edges'])):
            # 크롤링 횟수 카운트
            self.crawling_count  += 1
            if self.crawling_count % 500 == 0:
                time.sleep(300)
            # 유저 넘버
            item['inner_id'] = jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['owner']['id']
            insta_id = item['inner_id']
            # 게시물 게시 시간
            item['post_date'] = (datetime.datetime.fromtimestamp(int(jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['taken_at_timestamp']))).strftime('%Y-%m-%d %H:%M:%S')
            # 동영상 조회수
            if jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['is_video'] == True:
                item['view_count'] = jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['video_view_count']
            else:
                item['view_count'] = None
            # 게시물 좋아요 개수        
            item['like_count'] = jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['edge_media_preview_like']['count']
            # 크롤링 시간
            item['crawling_time'] = time.strftime('%Y-%m-%d-%c', time.localtime(time.time()))
            # 사진 URL
            item['media_url'] = jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['display_url']
            # 게시물 텍스트
            if jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['edge_media_to_caption']['edges'] != []:
                item['content'] = jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['edge_media_to_caption']['edges'][0]['node']['text']
            else:
                item['content'] = None
            # 게시물 고유 코드
            item['post_id'] = jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['shortcode']
            # 게시물 URL
            item['url'] = 'https://www.instagram.com/p/' + item['post_id']
            # 게시물 텍스트 해시태그
            if re.findall('#[\w가-힣a-zA-Z0-9]*', str(item['content'])) != None:
                find_hashtag = re.findall('(?<=\#)[\w가-힣a-zA-Z0-9]*', str(item['content']))
                item['hashtag'] = ', '.join(find_hashtag)
            else:
                item['hashtag'] = None
            # 게시자명
            item['insta_id'] = jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['owner']['username']
            # 게시물 장소
            if jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['location'] != None:
                item['location'] = jason['data']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['location']['name']
            else:
                item['location'] = None
            yield item

        end_cursor = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        
        if end_cursor != None:
            yield scrapy.Request(InstaCralwingSpider.url_format.format(insta_id) + InstaCralwingSpider.next_page.format(end_cursor) + InstaCralwingSpider.url_end, callback=self.parse)