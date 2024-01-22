# 豆瓣爬虫
import json
import time

import pandas as pd
import requests


class DoubanSpider:
    def __init__(self):
        url_base = "https://m.douban.com/rexxar/api/v2/movie/recommend?"
        url = "https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=0&count=20&selected_categories=%7B%7D&uncollect=false&sort=T&tags="
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Referer': 'https://m.douban.com/explore'
        }

    def get_page(url, headers, params):
        res = None
        cnt = 0
        while cnt <= 3:
            req = requests.get(url, headers=headers, params=params)
            if req.status_code == 200:
                res = json.loads(req.text)
                break
            else:
                cnt += 1
                continue

        return res

    def get_data(page_cnt):
        res_list = []
        params = {
            'refresh': ['0'],
            'start': ['0'],
            'count': ['20'],
            'selected_categories': ['{"类型":"喜剧","地区":"华语"}'],
            'uncollect': ['false'],
            'tags': ['喜剧,华语,搞笑'],
            'sort': ['S']
        }
        for i in range(page_cnt):
            start = str(i * 20)
            params['start'] = [start]
            res = get_page(url_base, headers, params)
            res_list.append(res)
            time.sleep(1)

        return res_list


if __name__ == '__main__':
    page_cnt = 50
    data = get_data(page_cnt)
    data_clean = [j for i in range(len(data))
                  for j in data[i]['items']]
    df = pd.DataFrame(data_clean)
    df[['title', 'year', 'card_subtitle']]