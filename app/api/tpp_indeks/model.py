from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects import mssql

from app import db
from . import modelName
# from ..tpp_indeksDetail.model import tpp_indeksDetail


class tpp_indeks(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kelas_jab = db.Column(db.Integer, nullable=False, index=True)
    ikf = db.Column(db.Integer, nullable=False, index=True)

    ikk_daerah = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    ikk_jkt = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    ikk = db.Column(db.DECIMAL(18, 8), default=0, nullable=True)

    ippd = db.Column(db.DECIMAL(18, 8), default=0, nullable=True)

    olk = db.Column(db.Integer, nullable=False, index=True)

    lppd = db.Column(db.Integer, nullable=False, index=True)

    kppd = db.Column(db.Integer, nullable=False, index=True)

    hasil_iid = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    nilai_iid = db.Column(db.Integer, nullable=False, index=True)

    pkpd = db.Column(db.Integer, nullable=False, index=True)

    hasil_rbpd = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    nilai_rbpd = db.Column(db.Integer, nullable=False, index=True)

    irbpd = db.Column(db.Integer, nullable=False, index=True)

    hasil_ipm = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    nilai_ipm = db.Column(db.Integer, nullable=False, index=True)

    hasil_igr = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    nilai_igr = db.Column(db.Integer, nullable=False, index=True)

    total_skor = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    nilai_ippd = db.Column(db.DECIMAL(18, 3), default=0, nullable=True)
    indeks_tpp = db.Column(db.DECIMAL(18, 9), default=0, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.now, nullable=True)


    # tpp_structural = db.relationship("tpp_structural", backref=modelName, lazy="dynamic")

    # @property
    # def detail_count(self):
    #     return db.session.query(func.count(tpp_indeksDetail.id)).filter(
    #         tpp_indeksDetail.id_tpp_indeks == self.id
    #     ).scalar()
    #
    # @property
    # def success_count(self):
    #     return db.session.query(func.count(tpp_indeksDetail.id)).filter(
    #         tpp_indeksDetail.id_tpp_indeks == self.id, tpp_indeksDetail.status == 1
    #     ).scalar()
    #
    # @property
    # def _disabled_delete_(self):
    #     return db.session.query(func.count(tpp_indeksDetail.id)).filter(
    #         tpp_indeksDetail.id_tpp_indeks == self.id
    #     ).scalar() >= 1


#
# # BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_indeks)
#
#
# @event.listens_for(tpp_indeks, 'before_insert')
# def check_unit_privilege_insert(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_indeks, 'before_update')
# def check_unit_privilege_delete(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_indeks, 'before_delete')
# def check_unit_privilege_update(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_indeks, 'after_insert')
# def insert_activity_insert(mapper, connection, target):
#     access_token = current_user['access_token']
#     origin = current_user['origin']
#     data = {
#         "type": 'post',
#         'endpoint_path': f'{apiPath}',
#         'data_id': target.id,
#         'subject': crudTitle,
#         'origin': origin,
#         "attributes": {
#             'data': row2dict(target)
#         }
#     }
#     thread = Thread(target=insert_user_activity, args=(data, access_token,))
#     thread.start()
#     thread.join()
#
#
# @event.listens_for(tpp_indeks, 'after_update')
# def insert_activity_update(mapper, connection, target):
#     access_token = current_user['access_token']
#     origin = current_user['origin']
#     data = {
#         "type": 'put',
#         'endpoint_path': f'{apiPath}',
#         'data_id': target.id,
#         'subject': crudTitle,
#         'origin': origin,
#         "attributes": {
#             'data': row2dict(target)
#         }
#     }
#     thread = Thread(target=insert_user_activity, args=(data, access_token,))
#     thread.start()
#     thread.join()
#
#
# @event.listens_for(tpp_indeks, 'after_delete')
# def insert_activity_delete(mapper, connection, target):
#     access_token = current_user['access_token']
#     origin = current_user['origin']
#     data = {
#         "type": 'delete',
#         'endpoint_path': f'{apiPath}',
#         'data_id': target.id,
#         'subject': crudTitle,
#         'origin': origin,
#         "attributes": {
#             'data': row2dict(target)
#         }
#     }
#     thread = Thread(target=insert_user_activity, args=(data, access_token,))
#     thread.start()
#     thread.join()