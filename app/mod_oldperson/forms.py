# 老人模块视图
import json

import threading

import os

import socketio
from datetime import time

from flask import render_template, request, session, jsonify
from flask_cors import cross_origin

from app import app
import app.mod_oldperson.controllers as c
from flask import Blueprint

from app.mod_user.controllers import login_required
from app.models import OldPersoninfo

oldperson = Blueprint('oldperson', __name__)


# 列出所有老人信息
@oldperson.route('/oldperson/infolist', methods=['GET', 'POST'])
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
            'title': '身份证号',
            'slot': 'id_card'
        },
        {
            'title': '年龄',
            'slot': 'age'
        },
        {
            'title': '监护人',
            'key': 'firstguardian_name'
        },
        {
            'title': '操作',
            'slot': 'action',
            'width': 150,
            'align': 'center'
        }
    ]

    # 查找数据成功
    if _listdata:
        for obj in _listdata:
            item.append(obj.to_json())

        return jsonify({"code": 0, "items": item, "columns": columns})
    # 失败
    else:
        return jsonify({"code": 1, "items": [], "columns": []})


# 通过id删除老人信息
@oldperson.route('/oldperson/deleteinfo', methods=['POST'])
@login_required
def delete_oldpersoninfo():
    data = request.get_json()
    id = data['id']
    c.delete_by_id(id)
    return jsonify({"code": 0, "data": {"result": True, "detail": ""}})


# 修改或增加老人信息
# 增加时id为0即自动增加
# 修改时根据不同id查找对应信息进行修改
@oldperson.route('/oldperson/updateinfo', methods=['POST'])
@login_required
def update_oldpersoninfo():
    # 获取前端修改数据（json形式）
    print(request)
    data = request.get_json()
    print(data)
    record = OldPersoninfo()

    record.id = data['id']
    record.username = data['username']
    record.gender = data['gender']
    record.phone = data['phone']
    record.birthday = data['birthday']
    record.checkin_date = data['checkin_date']
    record.checkout_date = data['checkout_date']
    record.id_card = data['id_card']
    # record.imgset_dir = data['imgset_dir']
    # record.profile_photo = data['profile_photo']
    record.firstguardian_name = data['firstguardian_name']
    record.firstguardian_phone = data['firstguardian_phone']
    record.health_state = data['health_state']
    record.age = "22"
    if record.gender == "male":
        record.gender = "男"

    # 获取前端数据（表单形式）
    # record = OldPersoninfo()
    # record.id = int(request.form['record_id'])
    # record.username = request.form['username']
    # record.room_number = request.form['room_number']

    # 通过逻辑层修改数据库中数据
    c.update_insert_data(record)
    return jsonify({"code": 0, "data": {"result": True, "detail": ""}})


# 查找老人信息
@oldperson.route('/oldperson/searchByName', methods=['GET', 'POST'])
@login_required
def search_info():
    if request.method == 'POST':
        data = request.get_json()
        name = data['name']
        item = []
        oldpersonUser = c.select_by_name(name)
        print(oldpersonUser)

        # 找到数据库中对应的数据
        if oldpersonUser:
            item.append(oldpersonUser.to_json())
            return jsonify({"code": 0, "data": {"items": item, "result": True, "detail": ""}})
            # 未找到数据
        else:
            return jsonify({"code": 0, "data": {"items": [], "result": False, "detail": "查询失败"}})

    # 请求方法不对
    else:
        return jsonify({"code": 0, "data": {"items": [], "result": False, "detail": "请求方法错误"}})


# 上传老人头像
@oldperson.route('/oldperson/setoldpersonid/<int:id>')
def set_id_session(id):
    session['oldpersonid'] = id
    selectdata = c.select_by_id(id)


    # 接下来的代码放到了一个多线程里运行，作用是监测特定文件夹下有没有文件变化，如果有新的图片文件，就直接推送到web页面上：
    _image_dir = app.static_folder + '/img/oldperson' + '/' + str(id)
    if not os.path.exists(_image_dir):
        os.mkdir(_image_dir)

    # start file monitor program, need run in a single thread
    _file_monitor = threading.Thread(target=run_file_monitor,
                kwargs={'data': selectdata})
    _file_monitor.start()

    return" redirect('/oldpersonimagelist')"


# 老人数据分析
@oldperson.route('/oldperson/statistic', methods=['GET', 'POST'])
@login_required
def run_oldperson_statistic():
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
