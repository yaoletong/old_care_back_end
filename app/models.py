from app import db


# 系统管理员实体表
class User(db.Model):
    __tablename__ = 'sys_user'
    #colums
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(80), unique=False, nullable=True)
    Password = db.Column(db.String(80), unique=False, nullable=True)
    real_name = db.Column(db.String(80), unique=False, nullable=True)
    email = db.Column(db.String(80), nullable=True)
    sex = db.Column(db.String(20))
    phone = db.Column(db.String(50))
    passwordAgain = db.Column(db.String(50))

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 老人实体表
class OldPersoninfo(db.Model):
    __tablename__ = 'oldperson_info'
    id = db.Column(db.Integer,autoincrement=True, primary_key=True)
    username = db.Column(db.String(50))
    age = db.Column(db.String(50))
    gender = db.Column(db.String(5))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column(db.String(100))
    checkin_date = db.Column(db.String(100))
    checkout_date = db.Column(db.String(50))
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    room_number = db.Column(db.String(50))
    firstguardian_name = db.Column(db.String(50))
    firstguardian_relationship = db.Column(db.String(50))
    firstguardian_phone = db.Column(db.String(50))
    firstguardian_wechat = db.Column(db.String(50))
    secondguardian_name = db.Column(db.String(50))
    secondguardian_relationship = db.Column(db.String(50))
    secondguardian_phone = db.Column(db.String(50))
    secondguardian_wechat = db.Column(db.String(50))
    health_state = db.Column(db.String(50))
    description = db.Column(db.String(255))

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 工作人员实体表
class EmployeeInfo(db.Model):
    __tablename__ = 'employee_info'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    age = db.Column(db.String(50))
    gender = db.Column(db.String(5))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column((db.String(100)))
    hire_date = db.Column((db.String(100)))
    resign_date = db.Column((db.String(100)))
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    description = db.Column(db.String(255))


    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 义工人员实体表
class VolunteerInfo(db.Model):
    __tablename__ = 'volunteer_info'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    age = db.Column(db.String(50))
    address = db.Column(db.String(255))
    gender = db.Column(db.String(5))
    phone = db.Column(db.String(50))
    id_card = db.Column(db.String(50))
    birthday = db.Column((db.String(100)))
    checkin_date = db.Column((db.String(100)))
    checkout_date = db.Column((db.String(100)))
    imgset_dir = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    description = db.Column(db.String(255))

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 老人心情表
class MoodInfo(db.Model):
    __tablename__ = 'mood_info'

    id = db.Column(db.Integer, primary_key=True)
    mood_info = db.Column(db.String(45))
    date = db.Column(db.DateTime)
    address = db.Column(db.String(45))
    oldperson_id = db.Column(db.Integer)
    record = db.Column(db.String(255))

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 老人与义工交互表
class InteractInfo(db.Model):
    __tablename__ = 'interact_info'

    id = db.Column(db.Integer, primary_key=True)
    interact_info = db.Column(db.String(45))
    date = db.Column(db.DateTime)
    distance = db.Column(db.String(45))
    oldperson_name = db.Column(db.String(45))
    record = db.Column(db.String(255))

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 老人摔倒模块表
class FallInfo(db.Model):
    __tablename__ = 'fall_info'

    id = db.Column(db.Integer, primary_key=True)
    fall_info = db.Column(db.String(45))
    date = db.Column(db.DateTime)
    address = db.Column(db.String(45))
    oldperson_id = db.Column(db.Integer)
    record = db.Column(db.String(255))

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 陌生人相关信息表
class StrangerInfo(db.Model):
    __tablename__ = 'stranger_info'

    id = db.Column(db.Integer, primary_key=True)
    stranger_info = db.Column(db.String(45))
    date = db.Column(db.DateTime)
    address = db.Column(db.String(45))
    oldperson_id = db.Column(db.Integer)
    record = db.Column(db.String(255))

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item


# 入侵相关信息表
class InvadeInfo(db.Model):
    __tablename__ = 'invade_info'

    id = db.Column(db.Integer, primary_key=True)
    invade_info = db.Column(db.String(45))
    date = db.Column(db.DateTime)
    address = db.Column(db.String(45))
    oldperson_id = db.Column(db.Integer)
    record = db.Column(db.String(45))

    def to_json(self):
        """将实例对象转化为json"""
        item = self.__dict__
        if "_sa_instance_state" in item:
            del item["_sa_instance_state"]
        return item