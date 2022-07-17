# 工作人员视图
from flask import Blueprint, render_template, request, jsonify
import app.mod_employee.controllers as c
from app.mod_user.controllers import login_required
from app.models import EmployeeInfo

# 建立蓝图与主程序连接
employee = Blueprint('employee', __name__)


# 查找所有工作人员信息
@employee.route('/employee/infolist')
@login_required
def list_all_employeeinfo():
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
            'title': '身份证号',
            'slot': 'id_card'
        },
        {
            'title': '年龄',
            'slot': 'age'
        },
        {
            'title': '雇佣日期',
            'key': 'hire_date'
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


# 通过id删除工作人员信息
@employee.route('/employee/deleteinfo', methods=['POST'])
@login_required
def delete_employeeinfo():
    data = request.get_json()
    id = data['id']
    c.delete_by_id(id)
    return jsonify({"code": 0, "data": {"result": True, "detail": ""}})


# 修改或增加工作人员信息
# 增加时id为0即自动增加
# 修改时根据不同id查找对应信息进行修改
@employee.route('/employee/updateinfo', methods=['POST'])
@login_required
def update_employeeinfo():
    # 获取前端修改数据（json形式）
    data = request.get_json()
    record = EmployeeInfo()
    record.id = data['id']
    record.username = data['username']
    record.gender = data['gender']
    record.phone = data['phone']
    record.id_card = data['id_card']
    record.address = data['address']
    record.birthday = data['birthday']
    record.hire_date = data['hire_date']
    record.resign_date = data['resign_date']
    # record.imgset_dir = data['imgset_dir']
    # record.profile_photo = data['profile_photo']
    record.description = data['description']


    # 获取前端数据（表单形式）
    # record = OldPersoninfo()
    # record.id = int(request.form['record_id'])
    # record.username = request.form['username']
    # record.room_number = request.form['room_number']

    # 通过逻辑层修改数据库中数据
    judge = c.update_insert_data(record)

    # 添加或者修改成功
    if judge:
        return jsonify({"code": 0, "data": {"result": True, "detail": ""}})

    # 添加失败
    return jsonify({"code": 1, "data": {"result": False, "detail": "操作失败"}})


# 查找工作人员信息（name）
@employee.route('/employee/searchByName', methods=['GET', 'POST'])
@login_required
def search_info():
    data = request.get_json()
    name = data['name']
    item = []
    employeeUser = c.select_by_name(name)
    print(employeeUser)

    # 找到数据库中对应的数据
    if employeeUser:
        item.append(employeeUser.to_json())
        return jsonify({"code":0,"data":{"items": item, "result": True, "detail": ""}})
    # 未找到数据
    else:
        return jsonify({"code":0,"data":{"items":[],"result":False,"detail":"查询失败"}})

    # 请求方法不对
    # else:
    #     return jsonify({"code":0,"data":{"items":[],"result":False,"detail":"请求方法错误"}})


# 工作人员数据分析
@employee.route('/employee/statistic', methods=['GET', 'POST'])
@login_required
def run_employee_statistic():
    age = c.select_by_age()
    item = []
    man = []
    woman = []
    for obj in age:
        # 在所有数据中取出需要的数据进行传输
        # 如age，gender等数据进行绘图
        print(obj)
        item.append(obj.age)
        if obj.gender == "男":
            man.append(obj[2])
            woman.append(0)
        else:
            woman.append(obj[2])
            man.append(0)
    return jsonify({"code":0,"xData":{"data": item},"yData":[{"data":man}, {"data":woman}]})