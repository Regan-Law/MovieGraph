from py2neo import Graph


class Query:  # 查询类
	def __init__(self):  # 初始化
		self.graph = Graph("http://localhost:7474", auth=("neo4j", "yan011017"), name="neo4j")  # 连接数据库

	def run(self, cql):  # 执行查询
		# find_rela  = test_graph.run("match (n:Person{name:'张学友'})-[actedin]-(m:Movie) return m.title")
		result = []  # 定义一个空列表，用于存储查询结果
		find_rela = self.graph.run(cql)  # 执行cql语句
		for i in find_rela:  # 遍历查询结果
			result.append(i.items()[0][1])
		return result

# if __name__ == '__main__':
#     SQL=Query()
#     result=SQL.run("match (m:Movie)-[]->() where m.title='卧虎藏龙' return m.rating")
#     print(result)