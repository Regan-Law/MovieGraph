import pandas as pd

# 读取CSV文件
df = pd.read_csv("./data/Neo4j_import/person.csv")

# 预处理bio列，确保引号和换行符被正确处理
# 这里使用了Python的字符串replace方法来替换双引号为单引号
# 并且确保换行符也被正确处理
df["bio"] = df["bio"].apply(
    lambda x: (
        x.replace('""', '\\"').replace('"', "'").replace("\n", "\\n").replace("\r", "")
        if isinstance(x, str)
        else x
    )
)

# 将处理后的DataFrame保存到新的CSV文件中，确保不生成索引
df.to_csv("./data/Neo4j_import/person.csv", index=False)
