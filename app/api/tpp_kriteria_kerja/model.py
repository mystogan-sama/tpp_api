from datetime import datetime

from sqlalchemy import func, event
from sqlalchemy.dialects import mssql

from app import db
from . import modelName
from ...sso_helper import check_unit_and_employee_privilege_on_read_db


# from ..tpp_kriteria_kerjaDetail.model import tpp_kriteria_kerjaDetail


class tpp_kriteria_kerja(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_unit = db.Column(db.BigInteger, nullable=False)
    unit_name = db.Column(db.String(200), nullable=True)
    id_structural = db.Column(db.BigInteger, db.ForeignKey("tpp_structural.id"), nullable=False)
    beban_kerja = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)

    # Kolom status dan prestasi
    # status_prestasi = db.Column(db.Integer, default=0, nullable=True)
    # prestasi = db.Column(db.Integer, default=0, nullable=True)
    status_tapd = db.Column(db.Integer, default=0, nullable=True)
    prestasi_tapd = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_pptk = db.Column(db.Integer, default=0, nullable=True)
    prestasi_pptk = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_ja = db.Column(db.Integer, default=0, nullable=True)
    prestasi_ja = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_jf = db.Column(db.Integer, default=0, nullable=True)
    prestasi_jf = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_jp = db.Column(db.Integer, default=0, nullable=True)
    prestasi_jp = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_p_keu = db.Column(db.Integer, default=0, nullable=True)
    prestasi_p_keu = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)

    # Kolom status dan kondisi
    status_pengawasan = db.Column(db.Integer, default=0, nullable=True)
    kondisi_pengawasan = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_kesehatan = db.Column(db.Integer, default=0, nullable=True)
    kondisi_kesehatan = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_k_p_keu = db.Column(db.Integer, default=0, nullable=True)
    kondisi_p_keu = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_perencanaan = db.Column(db.Integer, default=0, nullable=True)
    kondisi_perencanaan = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_trantibumlinmas = db.Column(db.Integer, default=0, nullable=True)
    kondisi_trantibumlinmas = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_bijak_kdh = db.Column(db.Integer, default=0, nullable=True)
    kondisi_bijak_kdh = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_resiko_kerja = db.Column(db.Integer, default=0, nullable=True)
    kondisi_resiko_kerja = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    status_resiko_tinggi = db.Column(db.Integer, default=0, nullable=True)
    kondisi_resiko_tinggi = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)

    # Kolom kelangkaan profesi
    status_kelangkaan_profesi = db.Column(db.Integer, default=0, nullable=True)
    kelangkaan_profesi = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)

    # Kolom tempat bertugas
    status_tempat_bertugas = db.Column(db.Integer, default=0, nullable=True)
    tempat_bertugas = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)

    # Kolom objektif lainnya
    status_objektif_lainnya = db.Column(db.Integer, default=0, nullable=True)
    objektif_lainnya = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)

    # Tambahkan timestamp jika diperlukan
    created_date = db.Column(db.DateTime, default=datetime.now)

    # tpp_structural = db.relationship("tpp_structural", backref=modelName, lazy="dynamic")
    kerja_details = db.relationship("tpp_kriteria_kerja_det", backref="kerja", lazy="dynamic")

    @property
    def structural_name(self):
        return f"{self.tpp_structural.name}" if self.tpp_structural else None
    # @property
    # def detail_count(self):
    #     return db.session.query(func.count(tpp_kriteria_kerjaDetail.id)).filter(
    #         tpp_kriteria_kerjaDetail.id_tpp_kriteria_kerja == self.id
    #     ).scalar()
    #
    # @property
    # def success_count(self):
    #     return db.session.query(func.count(tpp_kriteria_kerjaDetail.id)).filter(
    #         tpp_kriteria_kerjaDetail.id_tpp_kriteria_kerja == self.id, tpp_kriteria_kerjaDetail.status == 1
    #     ).scalar()
    #
    # @property
    # def _disabled_delete_(self):
    #     return db.session.query(func.count(tpp_kriteria_kerjaDetail.id)).filter(
    #         tpp_kriteria_kerjaDetail.id_tpp_kriteria_kerja == self.id
    #     ).scalar() >= 1


#
# # BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_kriteria_kerja)


# @event.listens_for(tpp_kriteria_kerja, 'before_insert')
# def check_unit_privilege_insert(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_kriteria_kerja, 'before_update')
# def check_unit_privilege_delete(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# @event.listens_for(tpp_kriteria_kerja, 'before_delete')
# def check_unit_privilege_update(mapper, connection, target):
#     member_of_list = current_user['member_of_list']
#     check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_kriteria_kerja, 'after_insert')
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
# @event.listens_for(tpp_kriteria_kerja, 'after_update')
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
# @event.listens_for(tpp_kriteria_kerja, 'after_delete')
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