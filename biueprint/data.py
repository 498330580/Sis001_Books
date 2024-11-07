# 对外提供api对接浏览器插件，储存未进行数据清理的数据至数据库
from exts import db_sql
from models.data import TmpData
from flask import Blueprint, request, jsonify
from sqlalchemy import desc, asc, or_    # asc正序，desc倒序

# v1版api
data_bp_v1 = Blueprint('data_bp_v1', __name__, url_prefix='/api/v1/data')


# 获取全部数据、创建新数据
@data_bp_v1.route('/', methods=['GET', 'POST'])
def v1_list():
    if request.method == 'GET':     # 获取全部数据
        tmp_data = TmpData.query.order_by(desc(TmpData.update_time)).all()
        return {'code': 200, 'data': tmp_data, 'mess': '获取成功'}, 200
    elif request.method == 'POST' and request.is_json:      # 创建新数据
        data = request.get_json()
        tmp_data = TmpData(**data)
        db_sql.session.add(tmp_data)
        db_sql.session.commit()
        return jsonify({'code': 201, 'data': tmp_data.to_json(), 'mess': '新增成功'}), 201
    else:
        return jsonify({'code': 400, 'data': [], 'mess': '方法错误'}), 400


# 通过id获取、更新、删除数据
@data_bp_v1.route('/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def v1_one(uid):
    tmp_data = TmpData.query.get(uid)
    if tmp_data:
        if request.method == 'GET':         # 获取单条数据
            return jsonify({'code': 200, 'data': tmp_data.to_json(), 'mess': '获取成功'}), 200
        elif request.method == 'PUT':       # 更新单条数据
            data = request.json
            tmp_data.name = data['name']
            tmp_data.url = data['url']
            tmp_data.is_crawled = data['is_crawled']
            tmp_data.is_sorted = data['is_sorted']
            tmp_data.content = data['content']
            db_sql.session.commit()
            return jsonify({'code': 200, 'data': tmp_data.to_json(), 'mess': '更新成功'}), 200
        elif request.method == 'DELETE':    # 删除单条数据
            db_sql.session.delete(tmp_data)
            db_sql.session.commit()
            return jsonify({'code': 204, 'data': tmp_data.to_json(), 'mess': '删除成功'}), 204
        else:
            return jsonify({'code': 400, 'data': [], 'mess': '方法错误'}), 400
    else:
        return jsonify({'code': 404, 'data': [], 'mess': '数据不存在'}), 404


# 核对url是否存在
@data_bp_v1.route('/search', methods=['GET'])
def v1_search():
    keyword = request.args.get('keyword')  # 从查询参数中获取关键字
    if not keyword:
        return jsonify({'code': 400, 'data': [], 'mess': '没有传入查询关键字 keyword'}), 400

    search_type = request.args.get('type')
    if not search_type:
        return jsonify({'code': 400, 'data': [], 'mess': '没有传入查询类型关键字 type'}), 400

    if search_type == 'url':
        tmp_data = TmpData.query.filter_by(url=keyword).first()
        if tmp_data:
            return jsonify({'code': 200, 'data': tmp_data.to_json(), 'mess': '获取成功'}), 200
        else:
            return jsonify({'code': 404, 'data': [], 'mess': '数据不存在'}), 404
    elif search_type == 'name':
        tmp_data = TmpData.query.filter(TmpData.name.contains(keyword)).all()
        return jsonify({'code': 200, 'data': tmp_data.to_json(), 'mess': '获取成功'}), 200
    elif search_type == 'content':
        tmp_data = TmpData.query.filter(TmpData.content.contains(keyword)).all()
        return jsonify({'code': 200, 'data': tmp_data.to_json(), 'mess': '获取成功'}), 200
    else:
        tmp_data = TmpData.query.filter(or_(TmpData.name.contains(keyword), TmpData.content.contains(keyword))).all()
        return jsonify({'code': 200, 'data': tmp_data.to_json(), 'mess': '请传入url参数'}), 200
