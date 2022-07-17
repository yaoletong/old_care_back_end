# 获取所有系统管理员信息
from flask import request, jsonify

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app import db, app
# from app.mod_user.forms import auth
from app.models import User

import functools


def get_all_user():
    return User.query.all()


# 通过id查找
def select_by_id(id):
    return User.query.filter_by(id=id).first()


# 通过账号密码查找
def select_by_password(name,password):
    return User.query.filter_by(Username=name,
          Password=password).first()


# 通过id删除系统管理员
def delete_by_id(id):
    record = User.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()


# 更新或者新增数据
def update_insert_data(data):
    # if (data.id == 0):
        db.session.add(data)
        # data.imgset_dir = data.imgset_dir+'\\'+str(data.id)
        db.session.commit()
    # else:
    #     _data = data.__dict__
    #
    #     _data.pop('_sa_instance_state')
    #
    #     User.query.filter_by(id=data.id).update(_data)
    #     db.session.commit()


def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    # s = Serializer(app.config["SECRET_KEY"], expires_in=3600)

    # 随机生成token字符串
    # random_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
    # print(random_str)
    """
    X5V1ehPV5QaFQokclSL2
    """

    s = Serializer(app.config["SECRET_KEY"], expires_in=3600)
    print(s)
    # 接收用户id转换与编码
    token = s.dumps({"id": api_user}).decode("utf-8")
    print(token)
    return token


# 解析token
def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''


    # record = User.query.filter_by(jsonauth=token).first()
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        print(Exception)
    # 拿到转换后的数据，根据模型类去数据库查询用户信息
    user = User.query.filter_by(id=data["id"]).first()
    return user


def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            print(request.headers)
            token = request.headers["authorization"]
            print(token)
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code=4103, msg='缺少参数token')

        # record = User.query.filter_by(jsonauth=token).first()
        # if record:
        #     return view_func(*args, **kwargs)
        s = Serializer(app.config["SECRET_KEY"])
        try:
            s.loads(token)
            print(s.loads(token))
        except Exception:
            return jsonify(code=4101, msg="登录已过期")

        return view_func(*args, **kwargs)

    return verify_token