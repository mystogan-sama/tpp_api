from datetime import datetime

from sqlalchemy import func, event
from sqlalchemy.dialects import mssql

from app import db
from . import modelName
from ..tpp_realisasi_det.model import tpp_realisasi_det
from ...sso_helper import check_unit_and_employee_privilege_on_read_db


# from ..tpp_realisasiDetail.model import tpp_realisasiDetail


class tpp_realisasi(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_unit = db.Column(db.BigInteger, nullable=False)
    unit_name = db.Column(db.String(200), nullable=True)
    asn = db.Column(db.Integer, default=0, nullable=True)
    bulan = db.Column(db.Integer, default=0, nullable=True)
    bulan_str = db.Column(db.String(200), nullable=True)
    tahun = db.Column(db.Integer, default=0, nullable=True)

    @property
    def total_realisasi(self):
        total = (
            db.session.query(func.coalesce(func.sum(tpp_realisasi_det.kriteria_realisasi), 0))
            .filter(tpp_realisasi_det.id_realisasi == self.id)
            .scalar()
        )
        return float(total)

#
# # BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_realisasi)


# @event.listens_for(tpp_realisasi, 'before_insert')
# def check_unit_privilege_insert(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_realisasi, 'before_update')
# def check_unit_privilege_delete(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_realisasi, 'before_delete')
# def check_unit_privilege_update(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_realisasi, 'after_insert')
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
# @event.listens_for(tpp_realisasi, 'after_update')
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
# @event.listens_for(tpp_realisasi, 'after_delete')
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