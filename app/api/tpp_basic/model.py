from datetime import datetime

from sqlalchemy import func
from sqlalchemy.dialects import mssql

from app import db
from . import modelName
from ..tpp_indeks.model import tpp_indeks


# from ..tpp_basicDetail.model import tpp_basicDetail


class tpp_basic(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kelas = db.Column(db.Integer, nullable=False, index=True)
    bpk_ri = db.Column(mssql.MONEY, nullable=True)
    indeks = db.Column(db.DECIMAL(16, 15), default=0, nullable=True)
    tahun = db.Column(db.Integer, nullable=False, index=True)

    tpp_structural = db.relationship("tpp_structural", backref=modelName, lazy="dynamic")

    @property
    def nilai_basic_tpp(self):
        """
        Ambil indeks_tpp dari tpp_indeks (tahun ini) dan hitung bpk_ri * indeks_tpp.
        Tidak menggunakan kelas_jab karena tidak ada keterkaitan langsung.
        """
        tahun_ini = datetime.now().year

        indeks = db.session.query(tpp_indeks.indeks_tpp) \
            .filter(func.year(tpp_indeks.created_date) == tahun_ini) \
            .order_by(tpp_indeks.created_date.desc()) \
            .first()

        if indeks:
            return self.bpk_ri * indeks[0]
        return None

    @property
    def indeks_tpp(self):
        tahun_ini = datetime.now().year

        indeks = db.session.query(tpp_indeks.indeks_tpp) \
            .filter(func.year(tpp_indeks.created_date) == tahun_ini) \
            .order_by(tpp_indeks.created_date.desc()) \
            .first()

        return indeks[0]
    # @property
    # def detail_count(self):
    #     return db.session.query(func.count(tpp_basicDetail.id)).filter(
    #         tpp_basicDetail.id_tpp_basic == self.id
    #     ).scalar()
    #
    # @property
    # def success_count(self):
    #     return db.session.query(func.count(tpp_basicDetail.id)).filter(
    #         tpp_basicDetail.id_tpp_basic == self.id, tpp_basicDetail.status == 1
    #     ).scalar()
    #
    # @property
    # def _disabled_delete_(self):
    #     return db.session.query(func.count(tpp_basicDetail.id)).filter(
    #         tpp_basicDetail.id_tpp_basic == self.id
    #     ).scalar() >= 1


#
# # BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_basic)
#
#
# @event.listens_for(tpp_basic, 'before_insert')
# def check_unit_privilege_insert(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_basic, 'before_update')
# def check_unit_privilege_delete(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_basic, 'before_delete')
# def check_unit_privilege_update(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_basic, 'after_insert')
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
# @event.listens_for(tpp_basic, 'after_update')
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
# @event.listens_for(tpp_basic, 'after_delete')
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