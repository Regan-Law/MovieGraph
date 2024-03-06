# MovieGraph

[基于Neo4j的电影知识图谱的设计与实现](https://github.com/Regan-Law/MovieGraph)

## 项目简介

本项目使用了Neo4j作为知识图谱的存储引擎，使用Python实现对电影的查询和回答。主要使用了flask作为web应用框架,sk-learn作为作为训练模型,jieba库作为中文分词模块,BeautifulSoup4库作为网页爬取模块,py2neo库作为Neo4j的Python接口.


## 项目结构
- flaskr: 项目源码
    - data:
        - Neo4j_import: 爬取的数据和字典和问题模板,使用前请将Neo4j_import中的数据放到Neo4j的import目录下
        - question: 用于存放问题模板
        - cypher.txt: 用于存放Cypher查询语句,请在将Neo4j_import中的数据放到Neo4j的import目录下后在Neo4j中逐一运行导入命令
        - vocabulary: 用于存放训练词典
        - user_dict.txt: 由`generate_dict.py`生成的用户字典

    - spider: 爬虫模块，用于爬取电影信息，保存到Neo4j数据库中
        - data_crawler.py: 爬虫主程序
        - proxy_pool.py: 用于获取代理
        - start.bat: 用于启动爬虫
        - data_deal.py: 数据处理模块,用于将爬取的数据处理成Neo4j数据库所需格式
        - generate_dict.py: 用于生成用户字典
      > 注意:
      > - 使用前提:使用spider时,前提需要克隆[proxy_pool](https://github.com/jhao104/proxy_pool)
          库,同时安装[redis](https://github.com/tporadowski/redis/releases)数据库,并修改`proxy_pool`中的`settings.py`
          中的数据库连接信息,`proxy_pool`库需要安装在**项目的同级目录下**
      > - 使用方法:先打开`redis`服务器,再运行`start.bat`,最后运行`data_crawler.py`,`注意:根据需要修改data_crawler.py中的url地址`
      > - 爬虫由于设置了等待时间防止封IP,需要大量的时间才能爬取到足量的数据,所以该爬虫仅供学习参考,不建议自行爬取数据
      > - 爬虫完成后如果导入报错可以根据需要运行`data_deal.py`文件,注意修改`data_deal.py`中的路径
      > - 爬虫导入成功后需要运行generate_dict.py生成用户字典
      > - 爬虫爬取的数据仅用于学习,请勿用于商业用途 

    - static: 用于存放静态文件,如html,css,js等,其中使用了bootstrap和jquery,可自行添加.
    - templates: 用于存放html模板,其中`index.html`为欢迎界面,`QA.html`为主要界面
    - utils: 用于存放一些工具函数,如Neo4j数据库连接和查询工具,数据处理,问题分类和问题模板等
        - preprocess_data.py: 用于数据的处理,读取问题模板,对接受的问题进行词性划分等,主要使用了jieba库
        - question_classification.py: 使用了sk-learn朴素贝叶斯进行训练并使用TF-IDF进行特征提取和jieba库进行切割以完成对问题的分类
        - question_template.py: 定义了问题模板,用于对问题进行匹配,返回对应问题模板
        - query.py: 用于连接数据库并执行查询,返回查询结果
    - \_\_init\_\_.py: 应用工厂文件,用于创建应用
    - app.py: 应用文件,运行可启动本项目,**注意:运行前确保Neo4j数据库已连接且地址端口`localhost:5000`未被占用**
    - test: 测试用文件夹,用于测试
    - README.md: 项目说明文件