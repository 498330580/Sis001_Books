# 对外提供api对接浏览器插件，储存未进行数据清理的数据至数据库
from exts import db_sql, return_json, _code
from models.data import TmpData, History
from flask import Blueprint, request
from sqlalchemy import desc, or_    # asc正序，desc倒序


# v1版api
data_bp_v1 = Blueprint('data_bp_v1', __name__, url_prefix='/api/v1/data')
lishi_bp_v1 = Blueprint('lishi_bp_v1', __name__, url_prefix='/api/v1/lishi')


# 获取全部数据、创建新数据
@data_bp_v1.route('/', methods=['GET', 'POST'])
def data_v1_list_add():
    if request.method == 'GET':     # 获取全部数据
        tmp_data = TmpData.query.order_by(desc(TmpData.update_time)).all()
        results_list = [item.to_json() for item in tmp_data]
        return return_json(data=results_list)
    elif request.method == 'POST' and request.is_json:      # 创建新数据
        data = request.get_json()
        if TmpData.query.filter(TmpData.url.contains(data['url'])).all():
            return return_json(code=_code.Error, data=data, mess="数据已存在")
        tmp_data = TmpData(**data)
        db_sql.session.add(tmp_data)
        db_sql.session.commit()
        return return_json(code=_code.Add_Update, data=tmp_data.to_json())
    else:
        return return_json(code=_code.Error)


# 通过id获取、更新、删除数据
@data_bp_v1.route('/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def data_v1_get_update_del(uid):
    tmp_data = TmpData.query.get(uid)
    if tmp_data:
        if request.method == 'GET':         # 获取单条数据
            return return_json(tmp_data.to_json())
        elif request.method == 'PUT':       # 更新单条数据
            data = request.json
            tmp_data.name = data['name']
            tmp_data.url = data['url']
            tmp_data.is_crawled = data['is_crawled']
            tmp_data.is_sorted = data['is_sorted']
            tmp_data.content = data['content']
            db_sql.session.commit()
            return return_json(code=_code.Add_Update, data=tmp_data.to_json())
        elif request.method == 'DELETE':    # 删除单条数据
            db_sql.session.delete(tmp_data)
            db_sql.session.commit()
            return return_json(code=_code.Del)
        else:
            return return_json(code=_code.Error)
    else:
        return return_json(code=_code.NotFound)


# 核对url是否存在
@data_bp_v1.route('/search', methods=['GET'])
def data_v1_search():
    keyword = request.args.get('keyword')  # 从查询参数中获取关键字
    search_type = request.args.get('type')  # 搜索类型

    if not keyword and search_type not in ["is_not_sorted", "all_not_crawled"]:
        return return_json(code=_code.Error, mess="没有传入查询关键字 keyword")

    if search_type == 'url':    # 搜索url
        tmp_data = TmpData.query.filter(TmpData.url.contains(keyword)).order_by(desc(TmpData.update_time)).all()
        if not tmp_data:
            return return_json(code=_code.NotFound, mess=f"查询无数据:{keyword}")
    elif search_type == 'name':     # 查找名称
        tmp_data = TmpData.query.filter(TmpData.name.contains(keyword)).all()
    elif search_type == 'content':  # 查找内容
        tmp_data = TmpData.query.filter(TmpData.content.contains(keyword)).all()
    elif search_type == 'is_url':   # 判断url是否存在
        tmp_data = TmpData.query.filter(TmpData.url.contains(keyword)).all()
        if tmp_data:
            return return_json(data=True, mess=f"查询存在:{keyword}")
        return return_json(code=_code.NotFound, data=False, mess=f"查询不存在:{keyword}")
    elif search_type == 'all_not_crawled':
        tmp_data = TmpData.query.filter_by(is_crawled=False).all()
    elif search_type == 'is_not_sorted':
        tmp_data = TmpData.query.filter_by(is_sorted=False).all()
    else:
        tmp_data = TmpData.query.filter(
            or_(
                TmpData.name.contains(keyword),
                TmpData.content.contains(keyword)
            )
        ).all()
        results_list = [item.to_json() for item in tmp_data]
        if search_type:
            mess = f"传入type参数错误,默认全文搜索:{keyword}"
        else:
            mess = f"未传入type,默认全文搜索:{keyword}"
        return return_json(data=results_list, mess=mess)
    results_list = [item.to_json() for item in tmp_data]
    return return_json(data=results_list, mess=f"搜索成功{keyword}")


@lishi_bp_v1.route('/', methods=['GET', 'POST'])
def lishi_v1_list_add():
    if request.method == 'GET':
        _type = request.args.get('type')
        _keyword = request.args.get('keyword')

        if _type == "is_lishi" and _keyword:
            tmp_data = History.query.filter(History.url.contains(_keyword)).all()
            if tmp_data:
                return return_json(data=True, mess=f"查询存在:{_keyword}")
            return return_json(data=False, mess=f"查询不存在:{_keyword}")

        tmp_data = History.query.order_by(desc(History.update_time)).all()
        results_list = [item.to_json() for item in tmp_data]
        return return_json(data=results_list)
    elif request.method == 'POST' and request.is_json:
        data = request.get_json()
        if History.query.filter(History.url.contains(data["url"])).all():
            return return_json(code=_code.OK, data=data, mess="数据库中已存在")
        tmp_data = History(**data)
        db_sql.session.add(tmp_data)
        db_sql.session.commit()
        return return_json(code=_code.Add_Update, data=tmp_data.to_json())
    else:
        return return_json(code=_code.Error)
