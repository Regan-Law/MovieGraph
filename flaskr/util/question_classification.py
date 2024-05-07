import os
import re

import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


# 获取所有的文件
def getfilelist(root_path):
	file_path_list = []
	file_name = []
	walk = os.walk(root_path)
	for root, dirs, files in walk:
		for name in files:
			filepath = os.path.join(root, name)
			file_name.append(name)
			file_path_list.append(filepath)
	return file_path_list


def read_train_data():
	train_x = []  # 特征
	train_y = []  # 标签
	file_list = getfilelist("flaskr/data/question/")
	# 遍历所有文件
	for one_file in file_list:
		# 获取文件名中的数字
		num = re.sub(r"\D", "", one_file)
		# 如果该文件名有数字，则读取该文件
		if str(num).strip() != "":
			# 设置当前文件下的数据标签
			label_num = int(num)
			# 读取文件内容
			with open(one_file, "r", encoding="utf-8") as fr:
				data_list = fr.readlines()
				for one_line in data_list:
					# 使用jieba分词进行分词
					word_list = list(jieba.cut(str(one_line).strip()))
					# 将这一行加入结果集
					train_x.append(" ".join(word_list))
					train_y.append(label_num)
	return train_x, train_y


class Question_classify:
	def __init__(self):
		# 读取训练数据
		self.train_x, self.train_y = read_train_data()
		# 训练模型
		self.model = self.train_model_NB()

	# 训练并测试模型-NB
	def train_model_NB(self):
		x_train, y_train = self.train_x, self.train_y
		self.tv = TfidfVectorizer()  # 向量化处理
		train_data = self.tv.fit_transform(x_train).toarray()  # 计算TF-IDF值，转换为稠密数组
		clf = MultinomialNB(alpha=0.01)  # 创建朴素贝叶斯分类器对象，将拉普拉斯平滑程度alpha置为0.01（用于处理零概率问题）
		clf.fit(train_data, y_train)  # 训练模型
		return clf

	# 预测
	def predict(self, question):
		question = [" ".join(list(jieba.cut(question)))]
		test_data = self.tv.transform(question).toarray()  # 转换为特征向量并将其转化为稠密数组
		y_predict = self.model.predict(test_data)[0]  # 预测，取第一个预测结果
		return y_predict