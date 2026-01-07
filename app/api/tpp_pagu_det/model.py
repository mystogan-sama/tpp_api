from threading import Thread

from sqlalchemy import event, func, text
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName
from ..tpp_kriteria.model import tpp_kriteria
from ..tpp_trans.model import tpp_trans


class tpp_pagu_det(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_pagu = db.Column(db.Integer, db.ForeignKey("tpp_pagu.id"), nullable=True)
    id_kriteria = db.Column(db.Integer, nullable=True)
    kriteria_code = db.Column(db.String(512), nullable=True)
    kriteria_name = db.Column(db.String(512), nullable=True)
    kriteria_pagu = db.Column(mssql.MONEY, default=0, nullable=True)

    # tpp_structural = db.relationship("tpp_structural", backref=modelName, lazy="dynamic")
    # kriteria = db.relationship("tpp_kriteria", foreign_keys=[id_kriteria], backref="kerja_details")

    @property
    def id_parent(self):
        return self.kriteria.parent_id if self.kriteria else None

    @property
    def parent_name(self):
        if self.kriteria and self.kriteria.parent_id:
            parent = tpp_kriteria.query.get(self.kriteria.parent_id)
            return parent.name if parent else None
        return None

    @property
    def total_beban_kerja(self):
        """
        SUM(beban_kerja_rp_bln * bulan)
        berdasarkan:
        - id_unit dari parent tpp_pagu
        - asn dari parent tpp_pagu
        """

        sql = text("""
            SELECT COALESCE(SUM(t.beban_kerja_rp_bln * t.bulan), 0)
            FROM tpp_trans t
            WHERE t.id_unit = (
                SELECT p.id_unit
                FROM tpp_pagu p
                WHERE p.id = :id_pagu
            )
            AND t.asn = (
                SELECT p.asn
                FROM tpp_pagu p
                WHERE p.id = :id_pagu
            )
        """)

        total = db.session.execute(
            sql,
            {"id_pagu": self.id_pagu}
        ).scalar()

        return float(total)

    @property
    def total_prestasi_kerja(self):
        sql = text("""
            SELECT COALESCE(SUM(t.prestasi_kerja_rp_bln * t.bulan), 0)
            FROM tpp_trans t
            WHERE t.id_unit = (
                SELECT p.id_unit FROM tpp_pagu p WHERE p.id = :id_pagu
            )
            AND t.asn = (
                SELECT p.asn FROM tpp_pagu p WHERE p.id = :id_pagu
            )
        """)
        return float(db.session.execute(sql, {"id_pagu": self.id_pagu}).scalar())

    @property
    def total_kondisi_kerja(self):
        sql = text("""
            SELECT COALESCE(SUM(t.kondisi_kerja_rp_bln * t.bulan), 0)
            FROM tpp_trans t
            WHERE t.id_unit = (
                SELECT p.id_unit FROM tpp_pagu p WHERE p.id = :id_pagu
            )
            AND t.asn = (
                SELECT p.asn FROM tpp_pagu p WHERE p.id = :id_pagu
            )
        """)
        return float(db.session.execute(sql, {"id_pagu": self.id_pagu}).scalar())

    @property
    def total_realisasi(self):
        """
        Menyesuaikan total berdasarkan kriteria_name
        """

        kriteria = (self.kriteria_code or "").lower()

        if "1." in kriteria:
            return self.total_beban_kerja

        if "2." in kriteria:
            return self.total_prestasi_kerja

        if "3." in kriteria:
            return self.total_kondisi_kerja

        return 0.0
# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_pagu_det)
#
#
# @event.listens_for(tpp_pagu_det, 'before_insert')
# def check_unit_privilege_insert(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_pagu_det, 'before_update')
# def check_unit_privilege_delete(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_pagu_det, 'before_delete')
# def check_unit_privilege_update(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_pagu_det, 'after_insert')
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
# @event.listens_for(tpp_pagu_det, 'after_update')
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
# @event.listens_for(tpp_pagu_det, 'after_delete')
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