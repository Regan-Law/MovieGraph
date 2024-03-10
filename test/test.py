from preprocess_data import Question

# 创建问题处理对象，这样模型就可以常驻内存
que = Question()
result = que.question_process("花泽香菜参演的评分小于8.5的电影有哪些")
print(result)