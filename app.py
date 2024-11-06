import os
from flask import Flask, render_template
from exts import db_sql
from flask_migrate import Migrate
from config import DevelopmentConfig

# 导入蓝图
from biueprint.crawl import crawl_bp_v1
from biueprint.book import book_bp_v1
from biueprint.data import data_bp_v1

# 导入sql表
from models import book

app = Flask(__name__)


# 获取项目目录
APP_PATH = os.path.dirname(__file__)


# 配置
app.config.from_object(DevelopmentConfig)


# 创建数据库连接，管理项目
db_sql.init_app(app)
migrate = Migrate(app, db_sql)


@app.route('/')
def hello_world():  # put application's code here
    return f'欢迎来到SIS001小说数据库！'


@app.errorhandler(404)  # 注册404错误处理函数
def page_not_found(e):  # 定义函数名和参数
    return render_template('404.html'), 404  # 返回404页面


# 注册蓝图
# v1
app.register_blueprint(crawl_bp_v1)     # 注册v1爬取蓝图
app.register_blueprint(data_bp_v1)     # 注册v1临时数据蓝图
app.register_blueprint(book_bp_v1)     # 注册书籍蓝图


if __name__ == '__main__':
    # 创建数据库
    # sql.create_all()
    # 运行服务
    app.run(debug=True, host='0.0.0.0', port=8100)
