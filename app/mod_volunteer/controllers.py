# 义工逻辑模块
from sqlalchemy import func

from app import db
from app.models import VolunteerInfo


def get_all_data():
    return VolunteerInfo.query.all()


# 根据id查询义工信息
def select_by_id(id):
    return VolunteerInfo.query.filter_by(id=id).first()


# 根据姓名查询义工信息
def select_by_name(name):
    return VolunteerInfo.query.filter_by(name=name).first()


def select_by_age():
    return db.session.query(VolunteerInfo.age, VolunteerInfo.gender, func.count(VolunteerInfo.id)).group_by(VolunteerInfo.age, VolunteerInfo.gender).all()


# 根据id删除义工信息
def delete_by_id(id):
    record = VolunteerInfo.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()


# 更新或新增数据
# id为0为新增，id为其他为更改
def update_insert_data(data):
    if (data.id == 0):
        db.session.add(data)
        # data.imgset_dir = data.imgset_dir+'\\'+str(data.id)
        db.session.commit()
    else:
        _data = data.__dict__

        _data.pop('_sa_instance_state')

        VolunteerInfo.query.filter_by(id=data.id).update(_data)
        db.session.commit()
