import os
import time

import pandas as pd
from bs4 import BeautifulSoup

from proxy_pool import getHtml

# 请求热门电影的URL
url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E6%9C%80%E6%96%B0&page_limit=1&page_start=0"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}
movie_header = ["mid", "title", "introduction", "rating", "releasedate", "url"]
person_header = ["pid", "name", "bio", "url"]
genre_header = ["gid", "name"]
movie_to_genre_header = ["mid", "gid"]
person_to_movie_header = ["pid", "mid"]
# 创建csv文件
if not os.path.exists("./data/Neo4j_import/movie.csv"):
    headers = pd.DataFrame(columns=movie_header)
    headers.to_csv("./data/Neo4j_import/movie.csv", index=False)
if not os.path.exists("./data/Neo4j_import/person.csv"):
    headers = pd.DataFrame(columns=person_header)
    headers.to_csv("./data/Neo4j_import/person.csv", index=False)

if not os.path.exists("./data/Neo4j_import/genre.csv"):
    headers = pd.DataFrame(columns=genre_header)
    headers.to_csv("./data/Neo4j_import/genre.csv", index=False)

if not os.path.exists("./data/Neo4j_import/movie_to_genre.csv"):
    headers = pd.DataFrame(columns=movie_to_genre_header)
    headers.to_csv("./data/Neo4j_import/movie_to_genre.csv", index=False)

if not os.path.exists("./data/Neo4j_import/person_to_movie.csv"):
    headers = pd.DataFrame(columns=person_to_movie_header)
    headers.to_csv("./data/Neo4j_import/person_to_movie.csv", index=False)

# 获取请求数据
response = getHtml(url, headers)
data = response.json()

# 初始化类型字典和演员字典
genre_dict = {}
person_dict = {}

# 遍历每部电影
for movie in data["subjects"]:
    movie_url = movie["url"]
    # 去重判断
    movie_csv = pd.read_csv("./data/Neo4j_import/movie.csv")
    if movie_csv["url"].isin([movie_url]).any():
        continue
    else:
        if movie_csv["mid"].isnull().all():
            mid = 0
        else:
            mid = movie_csv["mid"].iloc[-1] + 1
        # 初始化数据列表
        movies = []
        # 添加随机时间延迟
        time.sleep(5)  # 随机等待5秒
        # 解析电影详细数据
        movie_response = getHtml(movie_url, headers)
        movie_soup = BeautifulSoup(movie_response.text, "html.parser")

        # 提取电影标题
        movie_title_element = movie_soup.find("span", {"property": "v:itemreviewed"})
        if movie_title_element:
            movie_title = movie_title_element.text
        else:
            # 如果没有找到电影标题，可以选择跳过这部电影或记录错误
            print(f"Title not found for movie at URL: {movie_url}")
            print(movie_soup)
            continue  # 跳过当前电影的剩余处理
        # 提取电影简介
        movie_introduction = movie_soup.find(
            "span", {"property": "v:summary"}
        ).get_text(strip=True)
        # 提取电影评分
        movie_rating = movie_soup.find("strong", {"property": "v:average"}).text
        # 提取上映时间
        movie_releasedate = movie_soup.find(
            "span", {"property": "v:initialReleaseDate"}
        ).text
        # 创建DataFrame
        movies = pd.DataFrame(
            {
                "mid": [mid],
                "title": [movie_title],
                "introduction": [movie_introduction],
                "rating": [movie_rating],
                "releasedate": [movie_releasedate],
                "url": [movie_url],
            },
            columns=movie_header,  # 确保列名与之前一致
        )
        # 存入csv文件
        movies.to_csv(
            "./data/Neo4j_import/movie.csv",
            index=False,
            mode="a",
            header=False,
        )

        # 提取演员信息
        actors = movie_soup.find_all("a", rel="v:starring")
        for actor in actors:  # 遍历演员信息
            actor_name = actor.text
            actor_url = "https://movie.douban.com" + actor["href"]  # 获取演员的URL

            # 添加随机时间延迟
            time.sleep(5)  # 随机等待5秒
            # 读取演员csv文件
            person_csv = pd.read_csv("./data/Neo4j_import/person.csv")
            # 如果演员未出现过，获取演员信息
            if (
                not person_csv["url"].isin([actor_url]).any()
                and "celebrity" in actor_url
            ):
                # 请求演员页面
                actor_response = getHtml(actor_url, headers)
                actor_soup = BeautifulSoup(actor_response.text, "html.parser")

                # 提取演员简介
                actor_bio_locate = actor_soup.select_one("#intro > div.bd")
                if actor_bio_locate:
                    actor_bio_hidden = actor_bio_locate.select_one("span.all.hidden")
                    if actor_bio_hidden:
                        actor_bio_element = actor_bio_hidden
                    else:
                        actor_bio_element = actor_bio_locate
                    actor_bio = actor_bio_element.get_text(strip=True)
                    if not actor_bio:
                        actor_bio = (
                            "No biography available"  # 导入Neo4j时不能使用空值,踩坑
                        )
                else:
                    actor_bio = "No biography available"  # 导入Neo4j时不能使用空值
                # 分配新的pid
                if person_csv["pid"].isnull().all():
                    pid = 0
                else:
                    pid = person_csv["pid"].iloc[-1] + 1
                # 创建DataFrame
                persons = pd.DataFrame(
                    {
                        "pid": [pid],
                        "name": [actor_name],
                        "bio": [actor_bio],
                        "url": [actor_url],
                    },
                    columns=person_header,  # 确保列名与之前一致
                )
                # 存入csv文件中
                pd.DataFrame(persons).to_csv(
                    "./data/Neo4j_import/person.csv",
                    index=False,
                    mode="a",
                    header=False,
                )
            elif (
                not person_csv["url"].isin([actor_url]).any()
                and "celebrity" not in actor_url
            ):
                continue
            else:
                pid = person_csv.loc[person_csv["url"] == actor_url, "pid"].values[0]
            # 创建DataFrame
            person_to_movie = pd.DataFrame(
                {
                    "pid": [pid],
                    "mid": [mid],
                },
                columns=person_to_movie_header,  # 确保列名与之前一致
            )
            # 存入csv文件中
            pd.DataFrame(person_to_movie).to_csv(
                "./data/Neo4j_import/person_to_movie.csv",
                index=False,
                mode="a",
                header=False,
            )

        # 提取电影类型
        movie_genres = movie_soup.find_all("span", property="v:genre")
        # 遍历电影类型
        for genre in movie_genres:
            genre_name = genre.text
            # 读取类型csv文件
            genre_csv = pd.read_csv("./data/Neo4j_import/genre.csv")
            # 如果类型未出现过
            if not genre_csv["name"].isin([genre_name]).any():
                # 分配新的gid
                if genre_csv["gid"].isnull().all():
                    gid = 0
                else:
                    gid = genre_csv["gid"].iloc[-1] + 1
                # 创建DataFrame
                genres = pd.DataFrame(
                    {
                        "gid": [gid],
                        "name": [genre_name],
                    },
                    columns=genre_header,  # 确保列名与之前一致
                )
                # 存入csv文件中
                pd.DataFrame(genres).to_csv(
                    "./data/Neo4j_import/genre.csv", mode="a", index=False, header=False
                )
            else:
                gid = genre_csv.loc[genre_csv["name"] == genre_name, "gid"].values[0]
            # 创建DataFrame
            movie_to_genre = pd.DataFrame(
                {
                    "mid": [mid],
                    "gid": [gid],
                },
                columns=movie_to_genre_header,  # 确保列名与之前一致
            )
            # 存入csv文件中
            pd.DataFrame(movie_to_genre).to_csv(
                "./data/Neo4j_import/movie_to_genre.csv",
                mode="a",
                index=False,
                header=False,
            )
