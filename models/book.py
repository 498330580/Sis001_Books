# 小说数据库
from datetime import datetime
from exts import db_sql


# 小说作者（一对多），作者有多个小说
class Author(db_sql.Model):
    __tablename__ = 'author'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(100), nullable=False)
    book = db_sql.relationship('Book', backref='author')
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# 小说类型（一对多），类型有多个小说
class BookType(db_sql.Model):
    __tablename__ = 'book_type'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(100), nullable=False)
    book = db_sql.relationship('Book', backref='book_type')
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# 小说Tag（多对多），小说有多个标签
class BookTag(db_sql.Model):
    __tablename__ = 'book_tag'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(100), nullable=False)
    book = db_sql.relationship('Book', backref='tag', secondary='book_book_tag')
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# 小说书籍（一对多），书籍有多个章节
class Book(db_sql.Model):
    __tablename__ = 'book'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(300), nullable=False)
    author_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('author.id'))
    author = db_sql.relationship('Author', backref='book')
    book_type_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('book_type.id'))
    book_type = db_sql.relationship('BookType', backref='book')
    tag = db_sql.relationship('BookTag', backref='book', secondary='book_book_tag')
    content = db_sql.Column(db_sql.String(500), nullable=False)
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# 小说章节
class Category(db_sql.Model):
    __tablename__ = 'category'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(300), nullable=False)
    index_float = db_sql.Column(db_sql.Float, nullable=False)
    book_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    book = db_sql.relationship('Book', backref='category', cascade='all, delete-orphan')
    content = db_sql.Column(db_sql.Text, nullable=False)
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


# 定义book_book_tag表，用于Book和BookTag之间的多对多关系
book_book_tag = db_sql.Table('book_book_tag',
    db_sql.Column('book_id', db_sql.Integer, db_sql.ForeignKey('book.id'), primary_key=True),
    db_sql.Column('book_tag_id', db_sql.Integer, db_sql.ForeignKey('book_tag.id'), primary_key=True)
)


# if __name__ == '__main__':
#     # 测试外键关联
#     book = Book.query.first()
#     for i in book.category:
#         print(i.name)
#     pass
