import requests


def get_proxy():
    return requests.get("http://localhost:5010/get/").json()


def delete_proxy(proxy):
    requests.get("http://localhost:5010/delete/?proxy={}".format(proxy))


def getHtml(url, headers):
    retry_count = 7
    # 获得一个随机ip
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            # 尝试用获得的ip去访问测试网址
            requests.packages.urllib3.disable_warnings()
            html = requests.get(
                url,
                proxies={
                    "http": "http://{}".format(proxy),
                },
                headers=headers,
                verify=False,
            )
            # print("获取到的html是：{}".format(html.text))
            # print("代理ip：{}".format(proxy))
            return html
        # 如果报错，则尝试次数-1，五次后停止访问
        except Exception:
            retry_count -= 1
            # 用完一次就删除代理池中这条代理ip
            delete_proxy(proxy)
    return None
