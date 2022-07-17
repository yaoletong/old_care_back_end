# 老人模块逻辑
from sqlalchemy import func

from app.models import OldPersoninfo
from app import db


def get_all_data():
    return OldPersoninfo.query.all()


def select_by_id(id):
    return OldPersoninfo.query.filter_by(id=id).first()


def select_by_name(name):
    return OldPersoninfo.query.filter_by(username=name).first()


def delete_by_id(id):
    record = OldPersoninfo.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()


def select_by_age():
    return db.session.query(OldPersoninfo.age, OldPersoninfo.gender, func.count(OldPersoninfo.id)).group_by(OldPersoninfo.age, OldPersoninfo.gender).all()


# 更新或者新增数据
def update_insert_data(data):
    if (data.id == 0):
        db.session.add(data)
        # data.imgset_dir = data.imgset_dir+'\\'+str(data.id)
        db.session.commit()
    else:
        _data = data.__dict__

        _data.pop('_sa_instance_state')

        OldPersoninfo.query.filter_by(id=data.id).update(_data)
        db.session.commit()