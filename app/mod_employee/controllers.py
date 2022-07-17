# 工作人员逻辑层
from sqlalchemy import func

from app import db
from app.models import EmployeeInfo


def get_all_data():
    return EmployeeInfo.query.all()


def select_by_id(id):
    return EmployeeInfo.query.filter_by(id=id).first()


def select_by_name(name):
    return EmployeeInfo.query.filter_by(username=name).first()


def delete_by_id(id):
    record = EmployeeInfo.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()


def select_by_age():
    return db.session.query(EmployeeInfo.age, EmployeeInfo.gender, func.count(EmployeeInfo.id)).group_by(EmployeeInfo.age, EmployeeInfo.gender).all()


# 更新或者新增数据
def update_insert_data(data):
    if (data.id == 0):
        db.session.add(data)
        # data.imgset_dir = data.imgset_dir+'\\'+str(data.id)
        db.session.commit()
        return True
    else:
        _data = data.__dict__

        _data.pop('_sa_instance_state')

        EmployeeInfo.query.filter_by(id=data.id).update(_data)
        db.session.commit()
        return True