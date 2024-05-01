from preprocess_data import Question

# 创建问题处理对象，这样模型就可以常驻内存
que = Question()
result = que.question_process("三大队的演员都有谁")
print(result)
