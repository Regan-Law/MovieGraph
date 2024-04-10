import io
import sys

from flask import render_template, redirect, url_for, request

from flaskr import create_app
from flaskr.util.preprocess_data import Question

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
app = create_app()
qs = Question()


@app.route(
    "/",
    methods=["GET", "POST"],
)
def index():
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    return render_template("search.html")


@app.route("/start", methods=["GET", "POST"])
def start():
    if request.method == "POST":
        text = request.form
        print(text)
        return redirect(url_for("start"))
    return render_template("QA.html")


@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "POST":
        text = request.form
        if text["id"] == "bei":
            question = text["q"]
            print("received question:", question)
            print("now get answer!")
            answer = qs.question_process(question)
            print("得到的答案是：", answer)
            if len(str(answer).strip()) == 0:
                answer = "我也还不知道呢！"
            print("return answer!")
            return answer
    # 如果是GET请求或者POST请求不符合条件，则可以重定向或者返回特定信息
    return "Invalid request or condition not met", 400


if __name__ == "__main__":
    app.run()
