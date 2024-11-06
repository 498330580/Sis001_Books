# 临时数据库（转移数据库）
from exts import db_sql
from datetime import datetime


# 临时数据
class TmpData(db_sql.Model):
    __tablename__ = 'tmpdata'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(300), nullable=False)
    url = db_sql.Column(db_sql.String(500), nullable=False)
    is_crawled = db_sql.Column(db_sql.Boolean, nullable=False, default=False)   # 是否爬取数据
    is_sorted = db_sql.Column(db_sql.Boolean, nullable=False, default=False)    # 是否整理
    content = db_sql.Column(db_sql.Text, nullable=True)
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# 浏览记录
class History(db_sql.Model):
    __tablename__ = 'history'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    url = db_sql.Column(db_sql.String(500), nullable=False)
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
