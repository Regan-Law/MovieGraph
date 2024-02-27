from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/static/")
def index():
    return render_template.index()


if __name__ == "__main__":
    app.run(debug=True)
