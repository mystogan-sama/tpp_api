from threading import Thread

from sqlalchemy import event

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class tpp_unitKerja(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.String(512), nullable=True)
    eselon_level = db.Column(db.Integer, nullable=True)
    parent_id = db.Column(db.BigInteger, db.ForeignKey("tpp_unitKerja.id"), nullable=True)

    tpp_structural = db.relationship("tpp_structural", backref=modelName, lazy="dynamic")

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_unitKerja)


@event.listens_for(tpp_unitKerja, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(tpp_unitKerja, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(tpp_unitKerja, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(tpp_unitKerja, 'after_insert')
def insert_activity_insert(mapper, connection, target):
    access_token = current_user['access_token']
    origin = current_user['origin']
    data = {
        "type": 'post',
        'endpoint_path': f'{apiPath}',
        'data_id': target.id,
        'subject': crudTitle,
        'origin': origin,
        "attributes": {
            'data': row2dict(target)
        }
    }
    thread = Thread(target=insert_user_activity, args=(data, access_token,))
    thread.start()
    thread.join()


@event.listens_for(tpp_unitKerja, 'after_update')
def insert_activity_update(mapper, connection, target):
    access_token = current_user['access_token']
    origin = current_user['origin']
    data = {
        "type": 'put',
        'endpoint_path': f'{apiPath}',
        'data_id': target.id,
        'subject': crudTitle,
        'origin': origin,
        "attributes": {
            'data': row2dict(target)
        }
    }
    thread = Thread(target=insert_user_activity, args=(data, access_token,))
    thread.start()
    thread.join()


@event.listens_for(tpp_unitKerja, 'after_delete')
def insert_activity_delete(mapper, connection, target):
    access_token = current_user['access_token']
    origin = current_user['origin']
    data = {
        "type": 'delete',
        'endpoint_path': f'{apiPath}',
        'data_id': target.id,
        'subject': crudTitle,
        'origin': origin,
        "attributes": {
            'data': row2dict(target)
        }
    }
    thread = Thread(target=insert_user_activity, args=(data, access_token,))
    thread.start()
    thread.join()