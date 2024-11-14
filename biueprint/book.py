# 书籍api
from flask import Blueprint, request

from models.book import Book, Author, BookTag, BookType, Category
from exts import return_json, _code, db_sql
from sqlalchemy import desc

# v1版api
book_bp_v1 = Blueprint('book_bp_v1', __name__, url_prefix='/api/v1/book')
category_bp_v1 = Blueprint('category_bp_v1', __name__, url_prefix='/api/v1/category')


# 获取全部book、创建book
@book_bp_v1.route('/', methods=['GET', 'POST'])
def book_v1_list_add():
    if request.method == 'GET':
        tmp_data = Book.query.order_by(desc(Book.update_time)).all()
        results_list = [item.to_json() for item in tmp_data]
        return return_json(data=results_list)
    elif request.method == 'POST' and request.is_json:  # 创建新数据
        data = request.get_json()
        book_name = data.get('name', None)
        book_author = data.get('author', None)
        book_book_type = data.get('book_type', None)
        book_tag = data.get('tag', None)
        book_content = data.get('content', None)

        if not book_name:
            mess = "error:字段中无name"
        elif not book_author:
            mess = "error:字段中无author"
        elif not book_book_type:
            mess = "error:字段中无book_type"
        elif not book_tag:
            mess = "error:字段中无book_tag"
        elif not book_content:
            mess = "error:字段中无book_content"
        else:
            # 验证书籍是否已存在
            _book = Book.query.filter_by(name=book_name).first()
            if _book:
                # 书籍已存在
                mess = "书籍已存在"
                tmp_data = Book.query.filter_by(name=book_name).first().to_json()
                return return_json(code=_code.Add_Update, data=tmp_data, mess=mess)
            else:
                # 书籍不存在
                # 验证并获取book_author
                _author = Author.query.filter_by(name=book_author).first()
                if not _author:
                    # 作者不存在
                    _author = Author(name=book_author)
                    db_sql.session.add(_author)
                    db_sql.session.commit()

                # 验证并获取book_type
                _type = BookType.query.filter_by(name=book_book_type).first()
                if not _type:
                    # book_type不存在
                    _type = BookType(name=book_book_type)
                    db_sql.session.add(_type)
                    db_sql.session.commit()

                _book = Book(name=book_name, author=_author, book_type=_type, content=book_content)
                db_sql.session.add(_book)
                db_sql.session.flush()  # 确保新书籍有 id

                for tag in book_tag:
                    _tag = BookTag.query.filter_by(name=tag).first()
                    if not _tag:
                        # tag不存在
                        _tag = BookTag(name=tag)
                        db_sql.session.add(_tag)
                        db_sql.session.flush()
                    _book.tag.append(_tag)

                db_sql.session.commit()

                return return_json(code=_code.Add_Update, data=_book.to_json())
        return return_json(code=_code.Error, mess=mess)
    else:
        return return_json(code=_code.Error)


# 读取、更新、删除单个书籍
@book_bp_v1.route('/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def book_v1_get_update_del(book_id):
    tmp_data = Book.query.get(book_id)
    if tmp_data:
        if request.method == 'GET':
            return return_json(data=tmp_data.to_json())
        elif request.method == 'PUT' and request.is_json:
            data = request.get_json()
            book_name = data.get('name', None)
            book_author_id = data.get('author_id', None)
            book_type_id = data.get('book_type_id', None)
            book_tag = data.get('tag', None)
            book_content = data.get('content', None)

            if not book_name:
                mess = "error:字段中无name"
            elif not book_author_id:
                mess = "error:字段中无author_id"
            elif not book_type_id:
                mess = "error:字段中无book_type_id"
            elif not book_tag:
                mess = "error:字段中无book_tag"
            elif not book_content:
                mess = "error:字段中无book_content"
            else:
                tmp_data.name = book_name
                tmp_data.author_id = book_author_id
                tmp_data.book_type_id = book_type_id
                tmp_data.content = book_content

                # 处理标签tag
                current_tag_names = {tag.name for tag in tmp_data.tag}
                new_tag_names = set(data['tag'])
                # 添加新标签
                for tag_name in new_tag_names - current_tag_names:
                    tag = BookTag.query.filter_by(name=tag_name).first()
                    if not tag:
                        tag = BookTag(name=tag_name)
                        db_sql.session.add(tag)
                        db_sql.session.flush()
                    tmp_data.tag.append(tag)
                # 删除现有标签
                for tag_name in current_tag_names - new_tag_names:
                    tag = BookTag.query.filter_by(name=tag_name).first()
                    tmp_data.tag.remove(tag)

                db_sql.session.commit()

                return return_json(code=_code.Add_Update, data=request.get_json())
            return return_json(code=_code.Error, mess=mess)
        elif request.method == 'DELETE':
            db_sql.session.delete(tmp_data)
            db_sql.session.commit()
        else:
            return return_json(code=_code.Error)
    else:
        return return_json(code=_code.NotFound)


# 获取所有章节、创建章节
@book_bp_v1.route('/<int:book_id>', methods=['GET', 'POST'])
def category_v1_list_add(book_id):
    if request.method == 'GET':
        book = Book.query.filter_by(id=book_id).first()
        if not book:
            return return_json(code=_code.Error, mess=f"书籍ID:{book_id}不存在")
        if book.category:
            category_list = [category_item.to_json() for category_item in book.category]
        else:
            category_list = []
        return return_json(data=category_list)
    elif request.method == 'POST' and request.is_json:
        pass
    else:
        return return_json(code=_code.Error)
