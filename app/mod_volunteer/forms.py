# 义工视图模块

from flask import Blueprint, request, jsonify
import app.mod_volunteer.controllers as c
from app.mod_user.controllers import login_required
from app.models import VolunteerInfo

volunteer = Blueprint('volunteer', __name__)


# 列出所有义工信息
@volunteer.route('/volunteer/infolist', methods=['GET', 'POST'])
@login_required
def list_all_oldpersoninfo():
    item = []
    _listdata = c.get_all_data()
    columns = [
        {
            'title': 'id',
            'slot': 'id'
        },
        {
            'title': '姓名',
            'slot': 'username'
        },
        {
            'title': '性别',
            'slot': 'gender'
        },
        {
            'title': '手机',
            'slot': 'phone'
        },
        {
            'title': '身份证',
            'slot': 'id_card'
        },
        {
            'title': '生日',
            'key': 'birthday'
        },
        {
            'title': '入职时间',
            'key': 'checkin_date'
        },
        {
            'title': '操作',
            'slot': 'action',
            'width': 150,
            'align': 'center'
        }
    ]
    for obj in _listdata:
        item.append(obj.to_json())

    return jsonify({"code": 0, "items": item, "columns": columns})


# 通过id删除义工信息
@volunteer.route('/volunteer/deleteinfo', methods=['POST'])
@login_required
def delete_volunteerinfo():
    data = request.get_json()
    id = data['id']
    c.delete_by_id(id)
    return jsonify({"code": 0, "data": {"result": True, "detail": ""}})


# 修改或增加义工信息
# 增加时id为0即自动增加
# 修改时根据不同id查找对应信息进行修改
@volunteer.route('/volunteer/updateinfo', methods=['POST'])
@login_required
def update_volunteerinfo():
    # 获取前端修改数据（json形式）
    data = request.get_json()
    record = VolunteerInfo()
    record.id = data['id']

    record.username = data['username']
    record.gender = data['gender']
    record.phone = data['phone']
    record.id_card = data['id_card']
    record.birthday = data['birthday']
    record.checkin_date = data['checkin_date']
    record.checkout_date = data['checkout_date']
    # record.imgset_dir = data['imgset_dir']
    # record.profile_photo = data['profile_photo']
    record.description = data['description']
    record.age = "22"


    # 获取前端数据（表单形式）
    # record = OldPersoninfo()
    # record.id = int(request.form['record_id'])
    # record.username = request.form['username']
    # record.room_number = request.form['room_number']

    # 通过逻辑层修改数据库中数据
    c.update_insert_data(record)
    return jsonify({"code": 0, "data": {"result": True, "detail": ""}})


# 查找义工信息
@volunteer.route('/volunteer/search', methods=['GET', 'POST'])
@login_required
def search_info():
    # if request.method == 'GET':
    data = request.get_json()
    name = data['name']
    item = []
    volunteerUser = c.select_by_name(name)
    print(volunteerUser)
    if volunteerUser:
        item.append(volunteerUser.to_json())
        return jsonify({"code": 0, "data": {"items": item, "result": True, "detail": ""}})
        # 未找到数据
    else:
        return jsonify({"code": 0, "data": {"items": [], "result": False, "detail": "查询失败"}})

    # 请求方法不对
    # else:
    #     return jsonify({"code": 0, "data": {"items": [], "result": False, "detail": "请求方法错误"}})


# 义工数据报表
@volunteer.route('/volunteer/statistic', methods=['GET', 'POST'])
@login_required
def run_volunteer_statistic():
    age = c.select_by_age()
    item = []
    man = []
    woman = []
    for obj in age:
        # 在所有数据中取出需要的数据进行传输
        # 如age，gender等数据进行绘图
        item.append(obj.age)
        if obj.gender == "男":
            man.append(obj[2])
            woman.append(0)
        else:
            woman.append(obj[2])
            man.append(0)
    return jsonify({"code":0,"xData":{"data": item},"yData":[{"data":man}, {"data":woman}]})
