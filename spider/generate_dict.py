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
			f.write(f'{chinese_title} nm\n')  # 中文名
			f.write(f'{foreign_title} nm\n')  # 外文名
		else:
			# 如果没有外文名，或者格式不符合预期，直接写入整个标题
			f.write(f'{row["title"]} nm\n')
	for person in person:
		f.write(f'{person} nr\n')

	for genre in genre:
		f.write(f'{genre} ng\n')