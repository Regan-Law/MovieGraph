# 应用工厂

from flask import Flask


def create_app():
	app = Flask(__name__)  # 创建flask实例
	return app