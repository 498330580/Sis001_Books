# 书籍api


from flask import Blueprint


# v1版api
book_bp_v1 = Blueprint('book_bp_v1', __name__, url_prefix='/api/v1/book')
