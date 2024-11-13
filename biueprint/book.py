# 书籍api
from flask import Blueprint, request
from models.book import Book, Author, BookTag, BookType, Category
from exts import return_json, _code, db_sql
from sqlalchemy import desc

# v1版api
book_bp_v1 = Blueprint('book_bp_v1', __name__, url_prefix='/api/v1/book')


# 获取全部book
@book_bp_v1.route('/', methods=['GET', 'POST'])
def book_v1_list():
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
                    print(f"作者 {book_author} 不存在,创建作者")

                # 验证并获取book_type
                _type = BookType.query.filter_by(name=book_book_type).first()
                if not _type:
                    # book_type不存在
                    _type = BookType(name=book_book_type)
                    db_sql.session.add(_type)
                    db_sql.session.commit()
                    print(f"类型 {book_book_type} 不存在，创建type")

                _book = Book(name=book_name, author=_author, book_type=_type, content=book_content)
                db_sql.session.add(_book)
                db_sql.session.flush()  # 确保新书籍有 id

                # 验证tag是否存在
                tags = []
                for tag in book_tag:
                    _tag = BookTag.query.filter_by(name=tag).first()
                    if not _tag:
                        # tag不存在
                        _tag = BookTag(name=tag)
                        db_sql.session.add(_tag)
                        db_sql.session.flush()
                        print(f"Tag {book_tag} 不存在，创建Tag")
                    tags.append(_tag)

                _book.tag = tags
                db_sql.session.commit()

                return return_json(code=_code.Add_Update, data=_book.to_json())
        return return_json(code=_code.Error, mess=mess)
    else:
        return return_json(code=_code.Error)
