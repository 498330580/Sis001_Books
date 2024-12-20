from flask_sqlalchemy import SQLAlchemy
from flask import jsonify


db_sql = SQLAlchemy()


# 状态码
class GetCode:
    """
    响应状态码\n
    NotFound    数据不存在\n
    OK          获取成功\n
    Add_Update  创建或更新成功\n
    Del         删除成功\n
    Error       请求错误
    """
    NotFound = 404  # 不存在
    OK = 200        # 获取成功
    Add_Update = 201       # 创建、更新成功
    Del = 204       # 删除成功
    Error = 400     # 请求错误


_code = GetCode()


# 默认返回json
def return_json(code=_code.OK, data=None, mess=None):
    if data is None:
        data = []
    if mess is None:
        if code == _code.OK:
            mess = "获取成功"
        if code == _code.NotFound:
            mess = "不存在"
            data = []
        if code == _code.Add_Update:
            mess = "创建/更新成功"
        if code == _code.Del:
            mess = "删除成功"
            data = []
        if code == _code.Error:
            mess = "请求错误"
            data = []
    return jsonify({"code": code, "data": data, "mess": mess}), code
