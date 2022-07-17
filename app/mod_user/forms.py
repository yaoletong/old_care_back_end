# 系统管理员视图模块
import smtplib
from flask_httpauth import HTTPBasicAuth
from random import random

from email.mime.text import MIMEText

from flask import Blueprint, request, render_template, jsonify

from app import db, app
from app.models import User

import app.mod_user.controllers as c

user = Blueprint('user', __name__)


# 登出
@user.route('/logout', methods=['GET', 'POST'])
def logout():
    return jsonify({"code": 0, "data": {"result": True, "detail": ""}})

# 登录
@user.route('/login', methods=['GET', 'POST'])
def login():

    print(request.headers)
    # # 表单格式
    # username = request.form['username']
    # password = request.form['password']

    # json格式
    data = request.get_json()
    username = data['UserName']
    password = data['Password']

    # 进入数据库中查对账号
    userExist = c.select_by_password(username, password)
    print(userExist)

    # 查找正确
    if userExist:

        token = c.create_token(userExist.id)
        userExist.jsonauth = token
        db.session.commit()
        return jsonify({"code": 0, "data": {"result": True, "detail": token}})
    # 查找错误
    else:
        return jsonify({"code": 0, "data": {"result": False, "detail": "密码错误"}})


# 注册
@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        # 获取前端传输数据
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
        ver = data['verification']
        ver = int(ver)

        print(username)
        print(email)
        # 获取验证码
        global CorrectVerificationCode

        # 查找数据库中有无重复用户名或者邮箱
        register = User.query.filter_by(Username=username, email=email).first()
        print(register)

        # 注册失败
        if register or ver != int(CorrectVerificationCode):
        # if register:
            return jsonify({"code": 0, "data": {"result": False, "detail": "已注册"}})
        # 注册成功
        else:
            new_user = User()
            new_user.Username = username
            new_user.Password = password
            new_user.email = email
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"code": 0, "data": {"result": True, "detail": ""}})


# 发送验证码
@user.route('/sendemail', methods=['GET', 'POST'])
def send_emailMessage():
    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        print(email)
        mail_host = 'smtp.163.com'
        # 163用户名
        mail_user = '13723723013'
        # 密码(部分邮箱为授权码)
        mail_pass = 'ZY20001206tyl'
        # 邮件发送方邮箱地址
        sender = '13723723013@163.com'

        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [email]

        randomNumber = random.randint(1000, 9999)
        global CorrectVerificationCode
        CorrectVerificationCode = randomNumber
        randomNumberStr = str(randomNumber)
        content = '【智慧养老系统】您的验证码是' + randomNumberStr + '。如非本人操作，请忽略本邮件'
        print(randomNumber)
        print(CorrectVerificationCode)

        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = '智慧养老系统验证码'
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]

        # 登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            # 连接到服务器
            print(2)
            smtpObj.connect(mail_host, 25)
            # 登录到服务器
            print(3)
            smtpObj.login(mail_user, mail_pass)
            # 发送
            print(4)
            smtpObj.sendmail(
                sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print(1)
        except smtplib.SMTPException as e:
            print('error', e)  # 打印错误
        # return 'jsonify({"code": 20000, "data": {"verification": randomNumber}})'
        return randomNumber


# 通过id删除系统管理员信息
@user.route('/user/deleteinfo', methods=['POST'])
def delete_userinfo():
    data = request.get_json()
    id = data['id']
    c.delete_by_id(id)
    return 'success'


# 修改或增加系统管理员信息
# 增加时id为0即自动增加
# 修改时根据不同id查找对应信息进行修改
@user.route('/user/updateinfo', methods=['POST'])
def update_userinfo():
    # 获取前端修改数据（json形式）
    data = request.get_json()
    record = User()
    # record.id = int(data['id'])
    record.Username = data['UserName']
    record.Password = data['Password']
    record.real_name = data['REAL_NAME']
    record.phone = data['PHONE']
    record.email = data['EMAIL']
    record.sex = data['SEX']
    record.passwordAgain = data['PasswordAgain']

    # 获取前端数据（表单形式）
    # record = OldPersoninfo()
    # record.id = int(request.form['record_id'])
    # record.username = request.form['username']
    # record.room_number = request.form['room_number']

    # 通过逻辑层修改数据库中数据
    c.update_insert_data(record)
    return jsonify({"code": 0, "data": {"items": [], "result": True, "detail": ""}})


# 系统管理员修改登录密码
@user.route('/changepassword', methods=['POST'])
def do_changepassword():
    # 接收传输申请数据
    token = request.headers["authorization"]
    data = request.get_json()
    # user_id = session.get('userid')

    now_user = c.verify_token(token)
    old_password = data['password']
    new_password = data['passwd']
    passwdCheck = data['passwdCheck']

    if new_password == passwdCheck:

        # 进入数据库查找修改并提交
        # changeUser = User.query.filter_by(id=now_user.id).first()
        now_user.Password = new_password
        db.session.commit()

        return jsonify({"code": 0, "data": {"items": [], "result": True, "detail": ""}})


# 查找管理员信息
@user.route('/user/search', methods=['GET', 'POST'])
def search_info():
    if request.method == 'GET':
        data = request.get_json()
        id = data['id']
        item = []
        sysUser = c.select_by_id(id)
        print(sysUser)
        if sysUser:
            item.append(sysUser.to_json())
            return jsonify({"code": 20000, "data": {"total": 1, "items": item}})
        else:
            return jsonify({"code": 10000, "data": "false"})
    else:
        return jsonify({"code": 5000, "data": "false"})