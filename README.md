# MovieGraph

基于Neo4j的电影知识图谱的设计与实现

## 项目简介
- spider: 爬虫模块，用于爬取电影信息，保存到Neo4j数据库中
	> 注意:
	> - 使用前提:使用spider时,前提需要克隆[proxy_pool](https://github.com/jhao104/proxy_pool)库,同时安装[redis](https://github.com/tporadowski/redis/releases)数据库,并修改`proxy_pool`中的`settings.py`中的数据库连接信息,`proxy_pool`库需要安装在**项目的同级目录下**
	> - 使用方法:先打开`redis`服务器,再运行`start.bat`,最后运行`crawler.py`,`注意:根据需要修改crawler.py中的url地址`