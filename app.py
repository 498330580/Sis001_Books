import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# 获取项目目录
APP_PATH = os.path.dirname(__file__)


# 配置
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "123456789abcdefghijklmn"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(APP_PATH, 'data')}/test.db"


# 创建数据库连接，管理项目
db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return f'Hello World!  '


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8100)
