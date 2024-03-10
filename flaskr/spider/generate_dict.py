# 读取数据
import pandas as pd

# 读取数据
movies_df = pd.read_csv("../data/Neo4j_import/movie.csv")
person = pd.read_csv("../data/Neo4j_import/person.csv")["name"]
genre = pd.read_csv("../data/Neo4j_import/genre.csv")["name"]

output_folder = "../data/"

with open(f"{output_folder}user_dict.txt", "w", encoding="utf-8") as f:
	for _, row in movies_df.iterrows():
		# 分割中外文名，假设中文名和外文名之间至少有一个空格
		parts = row["title"].split(' ', 1)  # 最多分割一次，确保只分割中文名和外文名
		if len(parts) == 2:
			chinese_title, foreign_title = parts
			# 检查并移除句号
			chinese_title = chinese_title.replace('。', '')
			foreign_title = foreign_title.replace('。', '')
			f.write(f'{chinese_title} 15 nm\n')  # 中文名，词频设置为15
			f.write(f'{foreign_title} 15 nm\n')  # 外文名，词频设置为15
		else:
			# 如果没有外文名，或者格式不符合预期，直接写入整个标题
			title = row["title"].replace('。', '')  # 移除句号
			f.write(f'{row["title"]} 15 nm\n')  # 整个标题，词频设置为15
	for person in person:
		f.write(f'{person} 15 nr\n')  # 人名，词频设置为15

	for genre in genre:
		f.write(f'{genre} 15 ng\n')  # 类型名，词频设置为15