# 小说数据库
from datetime import datetime
from exts import db_sql


# 小说作者（一对多），作者有多个小说
class Author(db_sql.Model):
    __tablename__ = 'author'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(100), nullable=False)
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


# 小说类型（一对多），类型有多个小说
class BookType(db_sql.Model):
    __tablename__ = 'book_type'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(100), nullable=False)
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


# 小说Tag（多对多），小说有多个标签
class BookTag(db_sql.Model):
    __tablename__ = 'book_tag'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(100), nullable=False)
    book = db_sql.relationship('Book', back_populates='tag', secondary='book_book_tag')
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


# 小说书籍（一对多），书籍有多个章节
class Book(db_sql.Model):
    __tablename__ = 'book'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(300), nullable=False)
    author_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('author.id'))
    author = db_sql.relationship('Author', backref='book')
    book_type_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('book_type.id'))
    book_type = db_sql.relationship('BookType', backref='book')
    tag = db_sql.relationship('BookTag', back_populates='book', secondary='book_book_tag')
    category = db_sql.relationship(
        'Category',
        back_populates='book',
        cascade='all, delete-orphan',
        lazy='dynamic',
        order_by=lambda: Category.index_float.asc()
        # order_by=asc('category.index_float')
    )
    content = db_sql.Column(db_sql.String(500), nullable=False)
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_json(self):
        category_list = [
            {
                "name": item.name,
                "index": item.index_float,
                'create_time': item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': item.update_time.strftime('%Y-%m-%d %H:%M:%S')
            } for item in self.category
        ]

        tag_list = [tag.name for tag in self.tag]

        return {
            'id': self.id,
            'name': self.name,
            'author_id': self.author_id,
            'author': self.author.name,
            'book_type_id': self.book_type_id,
            'book_type': self.book_type.name,
            'tag': tag_list,
            'category': category_list,
            'content': self.content,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


# 小说章节
class Category(db_sql.Model):
    __tablename__ = 'category'
    id = db_sql.Column(db_sql.Integer, primary_key=True, autoincrement=True)
    name = db_sql.Column(db_sql.String(300), nullable=False)
    index_float = db_sql.Column(db_sql.Float, nullable=False)
    book_id = db_sql.Column(db_sql.Integer, db_sql.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    book = db_sql.relationship('Book', back_populates='category')
    url = db_sql.Column(db_sql.String(500), nullable=False)
    content = db_sql.Column(db_sql.Text, nullable=False)
    create_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now)
    update_time = db_sql.Column(db_sql.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def to_json(self):
        tag_list = [tag.name for tag in self.book.tag]
        return {
            'id': self.id,
            'name': self.name,
            'index_float': self.index_float,
            'book_id': self.book_id,
            'book': self.book.name,
            'book_author': self.book.author.name,
            'book_type': self.book.book_type.name,
            'book_tag': tag_list,
            'content': self.content,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': self.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }


# 定义book_book_tag表，用于Book和BookTag之间的多对多关系
book_book_tag = db_sql.Table('book_book_tag',
                             db_sql.Column('book_id', db_sql.Integer, db_sql.ForeignKey('book.id'), primary_key=True),
                             db_sql.Column('book_tag_id', db_sql.Integer, db_sql.ForeignKey('book_tag.id'),
                                           primary_key=True)
                             )
