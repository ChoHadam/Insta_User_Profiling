import csv
import requests
import json
import urllib.request
import time

def limit_follower(folder_path, file_name, n ):    
  headers = {
    }

  # csv 파일 불러와서 리스트에 저장
  file = open('{}/{}'.format(folder_path, file_name), 'r')
  csvfile = csv.reader(file)
  user_list = []
  for i in csvfile:
    user_list.extend(i)
  print(len(user_list), user_list)

  new_user_list = []
  req_count = 0
  
  # inner_id에 해당하는 follower수 가져오기 
  for inner_id in user_list:
    req_count += 1

    if req_count % 100 == 0:
      print()
      print('req_count : {}'.format(req_count))
      print()
      time.sleep(300) # 아이디 100개씩 request 할 때마다 5분씩 쉬면서 동작

    first_url = 'https://www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=%7B%22id%22%3A%22{}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A24%7D'.format(inner_id)
    #print(first_url)
    res = requests.get(first_url, headers = headers)
    res_dic = json.loads(res.text)
    if res_dic['data']['user'] != None:
      count = res_dic['data']['user']['edge_followed_by']['count']

      # 팔로워수가 n명 이하인 inner_id 추려내기
      if count <= n:
        print(inner_id, count)
        new_user_list.append(inner_id)
      
  print(len(new_user_list), new_user_list)

  # new_user_list csv파일로 저장
  unique_user_list = list(set(new_user_list)) #중복된 아이디 제거
  dataframe = pd.DataFrame(unique_user_list)
  dataframe.to_csv("{}/new_{}".format(folder_path, file_name), header=False, index = False)
  
  
  
# limit_follower 함수 호출
# 파라미터 : 파일경로, 파일명, 팔로워수 상한선(예 : 팔로워 1000명 이하인 id만 추려내고자하면 -> 1000 입력)
limit_follower('/content/drive/My Drive/insta_users', '20대.csv', 1000)