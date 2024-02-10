# MovieGraph

基于Neo4j的电影知识图谱的设计与实现

## 项目简介

- data: 爬取的数据和字典和问题模板,使用前请将Neo4j_import中的数据放到Neo4j的import目录下并在Neo4j中运行导入命令
- spider: 爬虫模块，用于爬取电影信息，保存到Neo4j数据库中
  > 注意:
  > - 使用前提:使用spider时,前提需要克隆[proxy_pool](https://github.com/jhao104/proxy_pool)
      库,同时安装[redis](https://github.com/tporadowski/redis/releases)数据库,并修改`proxy_pool`中的`settings.py`
      中的数据库连接信息,`proxy_pool`库需要安装在**项目的同级目录下**
  > - 使用方法:先打开`redis`服务器,再运行`start.bat`,最后运行`crawler.py`,`注意:根据需要修改crawler.py中的url地址`
  > - 爬虫由于设置了等待时间防止封IP,需要大量的时间才能爬取到足量的数据,所以该爬虫仅供学习参考,不建议自行爬取数据

- static: 用于存放静态文件,如html,css,js等
- templates: 用于存放html模板
- utils: 用于存放一些工具函数,如Neo4j数据库连接和查询工具,数据处理,问题分类和问题模板等