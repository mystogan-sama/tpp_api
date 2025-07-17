from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects import mssql

from app import db
from . import modelName
# from ..tpp_clusterDetail.model import tpp_clusterDetail


class tpp_cluster(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(512), nullable=False, index=True)
    description = db.Column(db.String(512), nullable=False, index=True)

    tpp_kriteria_cluster = db.relationship("tpp_kriteria_cluster", backref=modelName, lazy="dynamic")

    # @property
    # def detail_count(self):
    #     return db.session.query(func.count(tpp_clusterDetail.id)).filter(
    #         tpp_clusterDetail.id_tpp_cluster == self.id
    #     ).scalar()
    #
    # @property
    # def success_count(self):
    #     return db.session.query(func.count(tpp_clusterDetail.id)).filter(
    #         tpp_clusterDetail.id_tpp_cluster == self.id, tpp_clusterDetail.status == 1
    #     ).scalar()
    #
    # @property
    # def _disabled_delete_(self):
    #     return db.session.query(func.count(tpp_clusterDetail.id)).filter(
    #         tpp_clusterDetail.id_tpp_cluster == self.id
    #     ).scalar() >= 1


#
# # BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_cluster)
#
#
# @event.listens_for(tpp_cluster, 'before_insert')
# def check_unit_privilege_insert(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_cluster, 'before_update')
# def check_unit_privilege_delete(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_cluster, 'before_delete')
# def check_unit_privilege_update(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_cluster, 'after_insert')
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
# @event.listens_for(tpp_cluster, 'after_update')
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
# @event.listens_for(tpp_cluster, 'after_delete')
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