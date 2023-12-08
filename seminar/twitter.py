import requests
import json
 
# 認証用トークン
BEARER_TOKEN =  r"ユーザiD" # ← ここに認証用のトークンが入ります
headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}
 
# created_at(投稿時刻), author_id(アカウントID)などの情報が欲しい場合はtweet_fieldsに書く
# 空の場合は ツイートのid, text のみ取得する。
tweet_fields = ["created_at", "author_id", "public_metrics"]
user_fields = ["id", "name", "username"]
 
#自分の設定にあった endpointを取得
url = 'https://api.twitter.com/2/tweets/search/recent'

#取得できるのは直近1週間まで
# クエリ(検索語)の設定
query0 = {
    # 検索ワード  e.g. query = "テスト" / query = "テスト OR test"
    # OR 検索　AND検索　-検索　などしたい場合はそのように書く
    # ある特定 ID のツイートに対するリツイートを取得する場合は以下のように書く
    #    query={Tweet Id} -is:retweet
    'query': "(パッケージ 破れない) Lang:ja",
    #'query': '(自閉症 OR 自閉スペクトラム症)', # 
    'max_results': 10,
    #'start_time': '2020-04-01T00:00:00+09:00',
    'start_time': '2023-03-25T00:00:00+09:00',
    #'end_time': '2020-05-31T23:59:59+09:00', # +09:00 を入れると日本時間でかける
    'end_time': '2023-03-25T10:00:00+09:00',
    'tweet.fields': ",".join(tweet_fields),
    'user.fields': ",".join(user_fields),
}

query1 = {
    'query': "(パッケージ 破れない) Lang:ja",
    'max_results': 100,
    'start_time': '2023-03-28T00:00:00+09:00',
    'end_time': '2023-03-29T00:00:00+09:00',
    'tweet.fields': ",".join(tweet_fields),
    'user.fields': ",".join(user_fields),
}

query_list=[query0, query1]
text_number=-1
request_count=0

for query in query_list:
    total_tweet=0
    text_number+=1
    text="twapi{}.txt".format(text_number)
        
    #txtファイルを白紙にする
    with open(text, 'w', encoding='utf-8') as f:
        pass
    
    while True:
        #一定の件数以上リクエストしていたら停止させる
        if request_count >= 180:
            with open(text, 'a', encoding='utf-8') as f:
                f.writelines(str(total_tweet))
            print(total_tweet)
            print('too much request')
            break
        
        response = requests.request("GET", url, headers=headers, params=query)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        
        total_tweet += response.json()['meta']['result_count']
        
        # JSON という形式のデータを見易くする
        result_text = json.dumps(response.text, indent=4, sort_keys=True, ensure_ascii=False)
        # wは新規書き込み　aは追加書き込み
        with open(text, 'a', encoding='utf-8') as f:
            f.writelines(result_text+'\n')
        print(result_text)
        
        request_count += 1
        
        #pagination token を更新
        try:
            query['pagination_token']=response.json()['meta']['next_token']
        #next_tokenがなければ終了
        except KeyError:
            with open(text, 'a', encoding='utf-8') as f:
                f.writelines(str(total_tweet)+'\n')
            print(total_tweet)
            break