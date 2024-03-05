import sys

from flask import Flask, redirect, render_template, url_for, request

from util.preprocess_data import Question

app = Flask(__name__)
qs = Question()


@app.route(
	"/",
	methods=["GET", "POST"],
)
@app.route("/index", methods=["GET", "POST"])
def index():
	return render_template("templates/index.html")


@app.route("/start", methods=["GET", "POST"])
def start():
	if request.method == "POST":
		text = request.form
		print(text)
		return redirect(url_for("start"))
	return render_template("templates/QA.html")


@app.route("/query", methods=["GET", "POST"])
def query():
	if request.method == "POST":
		enablePrint()
		text = request.form
		if text["id"] == "bei":
			question = text["q"]
			print("received question:", question)
			print("now get answer!")
			answer = get_answer(question)
			print("得到的答案是：", answer)
			if len(str(answer).strip()) == 0:
				answer = "我也还不知道呢！"
			print("return answer!")
			return answer
	# 如果是GET请求或者POST请求不符合条件，则可以重定向或者返回特定信息
	return "Invalid request or condition not met", 400


def enablePrint():
	sys.stdout = sys.__stdout__


def get_answer(question):
	# 查询
	answer = qs.question_process(question)
	return answer


if __name__ == "__main__":
	app.run()