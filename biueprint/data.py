# 对外提供api对接浏览器插件，储存未进行数据清理的数据至数据库


from flask import Blueprint

# v1版api
data_bp_v1 = Blueprint('data_bp_v1', __name__, url_prefix='/api/v1/data')


# 获取全部数据
@data_bp_v1.route('/', methods=['GET'])
def get_v1_list():
    return '获取全部未爬取数据'


# 通过id获取单个数据
@data_bp_v1.route('/{int:id}', methods=['GET'])
def get_v1_one(id):
    return f'{id}'


# 通过post新增单条数据
@data_bp_v1.route('/', methods=['POST'])
def post_v1_one():
    return '新增成功'


# 通过put更新数据
@data_bp_v1.route('/<int:id>', methods=['PUT'])
def put_v1_one(id):
    return f'更新成功{id}'


# 通过delete删除数据
@data_bp_v1.route('/<int:id>', methods=['DELETE'])
def delete_v1_one(id):
    return f'删除{id}成功'