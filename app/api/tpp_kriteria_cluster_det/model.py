from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName
from ..tpp_kriteria.model import tpp_kriteria


class tpp_kriteria_cluster_det(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_kriteriaCluster = db.Column(db.Integer, db.ForeignKey("tpp_kriteria_cluster.id"), nullable=True)
    id_kriteria = db.Column(db.Integer, db.ForeignKey("tpp_kriteria.id"), nullable=True)
    kriteria_name = db.Column(db.String(512), nullable=True)
    kriteria_formula = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    kriteria_nominal = db.Column(mssql.MONEY, default=0, nullable=True)

    # tpp_structural = db.relationship("tpp_structural", backref=modelName, lazy="dynamic")
    kriteria = db.relationship("tpp_kriteria", foreign_keys=[id_kriteria], backref="cluster_details")

    @property
    def id_parent(self):
        return self.kriteria.parent_id if self.kriteria else None

    @property
    def parent_name(self):
        if self.kriteria and self.kriteria.parent_id:
            parent = tpp_kriteria.query.get(self.kriteria.parent_id)
            return parent.name if parent else None
        return None

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_kriteria_cluster_det)
#
#
# @event.listens_for(tpp_kriteria_cluster_det, 'before_insert')
# def check_unit_privilege_insert(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_kriteria_cluster_det, 'before_update')
# def check_unit_privilege_delete(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_kriteria_cluster_det, 'before_delete')
# def check_unit_privilege_update(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_kriteria_cluster_det, 'after_insert')
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
# @event.listens_for(tpp_kriteria_cluster_det, 'after_update')
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
# @event.listens_for(tpp_kriteria_cluster_det, 'after_delete')
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