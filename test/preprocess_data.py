import os
import re
import sys

import jieba.posseg

from question_classification import Question_classify
from question_template import QuestionTemplate


# Disable
# 用于阻止命令行输出，使得程序运行时不会在控制台打印任何内容。
# 通过将sys.stdout重新赋值为打开os.devnull文件的写入模式，将输出重定向到黑洞文件，实现阻止输出的效果。
def blockPrint():
	sys.stdout = open(os.devnull, "w")


# Restore
# 可以将stdout恢复到程序启动时的默认状态
# 将sys.stdout重新赋值为sys.stdout
def enablePrint():
	sys.stdout = sys.__stdout__


# blockPrint()

# enablePrint()


class Question:
	def __init__(self):
		# 初始化相关设置：读取词汇表，训练分类器，连接数据库
		self.init_config()

	def init_config(self):
		# # 读取词汇表
		# with(open("../flaskr/data/vocabulary.txt", "r", encoding="utf-8")) as fr:
		# 	vocab_list = fr.readlines()
		# vocab_dict = {}
		# vocablist = []
		# for one in vocab_list:
		# 	word_id, word = str(one).strip().split(":")
		# 	vocab_dict[str(word).strip()] = int(word_id)
		# 	vocablist.append(str(word).strip())
		# # print(vocab_dict)
		# self.vocab = vocab_dict

		# 训练分类器
		self.classify_model = Question_classify()
		# 读取问题模板
		with open(
				"./flaskr/data/question/question_classification.txt", "r", encoding="utf-8"
		) as f:
			question_mode_list = f.readlines()
		self.question_mode_dict = {}
		for one_mode in question_mode_list:
			# 读取一行
			mode_id, mode_str = str(one_mode).strip().split(":")
			# 处理一行，并存入
			self.question_mode_dict[int(mode_id)] = str(mode_str).strip()
		# print(self.question_mode_dict)

		# 创建问题模板对象
		self.questiontemplate = QuestionTemplate()

	def question_process(self, question):
		# 接收问题
		self.raw_question = str(question).strip()
		# 对问题进行词性标注
		self.pos_quesiton = self.question_posseg()
		# 得到问题的模板
		self.question_template_id_str = self.get_question_template()
		# 查询图数据库,得到答案
		self.answer = self.query_template()
		return self.answer

	def question_posseg(self):
		jieba.load_userdict("./flaskr/data/user_dict.txt")
		clean_question = re.sub(
			"[\s+\!\/_,$%^*(+\"')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+",
			"",
			self.raw_question,
		)
		self.clean_question = clean_question
		question_seged = jieba.posseg.cut(str(clean_question))
		result = []
		question_word, question_flag = [], []
		for w in question_seged:
			temp_word = f"{w.word}/{w.flag}"
			result.append(temp_word)
			# 预处理问题
			word, flag = w.word, w.flag
			question_word.append(str(word).strip())
			question_flag.append(str(flag).strip())
		assert len(question_flag) == len(question_word)
		self.question_word = question_word
		self.question_flag = question_flag
		print(result)
		return result

	def get_question_template(self):
		# 抽象问题
		for item in ["nr", "nm", "ng"]:
			while item in self.question_flag:
				ix = self.question_flag.index(item)
				self.question_word[ix] = item
				self.question_flag[ix] = item + "ed"
		# 将问题转化字符串
		str_question = "".join(self.question_word)
		print("抽象问题为：", str_question)
		# 通过分类器获取问题模板编号
		question_template_num = self.classify_model.predict(str_question)
		print("使用模板编号：", question_template_num)
		question_template = self.question_mode_dict[question_template_num]
		print("问题模板：", question_template)
		question_template_id_str = str(question_template_num) + "\t" + question_template
		print("转化结果为：", question_template_id_str)
		return question_template_id_str

	# 根据问题模板的具体类容，构造cql语句，并查询
	def query_template(self):
		# 调用问题模板类中的获取答案的方法
		try:
			answer = self.questiontemplate.get_question_answer(
				self.pos_quesiton, self.question_template_id_str
			)
		except:
			answer = "我也还不知道！"
		return answer