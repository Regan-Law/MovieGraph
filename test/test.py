import sys

from flaskr.util.preprocess_data import Question

# 创建问题处理对象，这样模型就可以常驻内存
que = Question()


# Restore
def enablePrint():
	sys.stdout = sys.__stdout__


enablePrint()
result = que.question_process("怪物是由谁出演的")
print(result)