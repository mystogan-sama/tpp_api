from datetime import datetime
from decimal import Decimal
from threading import Thread

from sqlalchemy import event, extract
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import insert_user_activity, current_user, check_unit_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName
from ..tpp_indeks.model import tpp_indeks


class tpp_kriteria(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.BigInteger, nullable=True)
    code = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(512), nullable=False, index=True)
    formula = db.Column(db.DECIMAL(18, 2), default=0, nullable=True)
    nominal = db.Column(mssql.MONEY, default=0, nullable=True)
    depth = db.Column(db.Integer, nullable=True)

    # tpp_kriteria_cluster_det = db.relationship("tpp_kriteria_cluster_det", backref=modelName, lazy="dynamic")
    # tpp_trans = db.relationship("tpp_trans", backref=modelName, lazy="dynamic")

    # @property
    # def UnitKerja_name(self):
    #     return f"| {self.tpp_unitKerja.name}" if self.tpp_unitKerja else None
    #
    # @property
    # def JobLevel_name(self):
    #     return f"| {self.tpp_jobLevel.name}" if self.tpp_jobLevel else None

    # @property
    # def nilai_tpp_basic(self):
    #     if self.tpp_basic and self.tpp_basic.bpk_ri is not None and self.tpp_basic.indeks is not None:
    #         return float(self.tpp_basic.bpk_ri) * float(self.tpp_basic.indeks)
    #     return None

    # @property
    # def indeks_tpp(self):
    #     # Ambil tahun saat ini
    #     tahun_sekarang = datetime.now().year
    #
    #     # Ambil 1 baris data indeks_tpp yang dibuat di tahun saat ini
    #     indeks = db.session.query(tpp_indeks.indeks_tpp).filter(
    #         extract('year', tpp_indeks.created_date) == tahun_sekarang
    #     ).order_by(tpp_indeks.created_date.desc()).first()  # opsional, ambil yang terbaru
    #
    #     return float(indeks[0]) if indeks else None
    #
    # @property
    # def bpk_ri(self):
    #     return f"{self.tpp_basic.bpk_ri}" if self.tpp_basic else None
    #
    # @property
    # def beban_kerja(self):
    #     """Mengembalikan beban kerja dalam format desimal"""
    #     kriteria = self.tpp_kriteria_kerja.first()
    #     if not kriteria or kriteria.beban_kerja is None:
    #         return Decimal('0.00')
    #
    #     # Konversi ke Decimal dengan presisi 2 digit
    #     return Decimal(str(kriteria.beban_kerja)).quantize(Decimal('0.00'))
    #
    # @property
    # def prestasi_kerja(self):
    #     """
    #     Menjumlahkan (SUM) semua nilai prestasi kerja dari komponen yang aktif (status=1)
    #     Mengembalikan nilai dalam format Decimal dengan 2 digit desimal
    #     """
    #     if not self.tpp_kriteria_kerja:
    #         return Decimal('0.00')
    #
    #     kriteria = self.tpp_kriteria_kerja.first()
    #     if not kriteria:
    #         return Decimal('0.00')
    #
    #     komponen = [
    #         (kriteria.status_tapd, kriteria.prestasi_tapd),
    #         (kriteria.status_pptk, kriteria.prestasi_pptk),
    #         (kriteria.status_ja, kriteria.prestasi_ja),
    #         (kriteria.status_jf, kriteria.prestasi_jf),
    #         (kriteria.status_jp, kriteria.prestasi_jp),
    #         (kriteria.status_p_keu, kriteria.prestasi_p_keu)
    #     ]
    #
    #     total = sum(
    #         Decimal(str(prestasi or 0))
    #         for status, prestasi in komponen
    #         if status == 1
    #     )
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # @property
    # def kondisi_kerja(self):
    #     """
    #     Menjumlahkan (SUM) semua nilai kondisi kerja dari komponen yang aktif (status=1)
    #     Mengembalikan nilai dalam format Decimal dengan 2 digit desimal
    #     """
    #     if not self.tpp_kriteria_kerja:
    #         return Decimal('0.00')
    #
    #     kriteria = self.tpp_kriteria_kerja.first()
    #     if not kriteria:
    #         return Decimal('0.00')
    #
    #     komponen = [
    #         (kriteria.status_pengawasan, kriteria.kondisi_pengawasan),
    #         (kriteria.status_kesehatan, kriteria.kondisi_kesehatan),
    #         (kriteria.status_k_p_keu, kriteria.kondisi_p_keu),
    #         (kriteria.status_perencanaan, kriteria.kondisi_perencanaan),
    #         (kriteria.status_trantibumlinmas, kriteria.kondisi_trantibumlinmas),
    #         (kriteria.status_bijak_kdh, kriteria.kondisi_bijak_kdh),
    #         (kriteria.status_resiko_kerja, kriteria.kondisi_resiko_kerja),
    #         (kriteria.status_resiko_tinggi, kriteria.kondisi_resiko_tinggi),
    #         (kriteria.status_kelangkaan_profesi, kriteria.kelangkaan_profesi),
    #         (kriteria.status_tempat_bertugas, kriteria.tempat_bertugas),
    #         (kriteria.status_objektif_lainnya, kriteria.objektif_lainnya)
    #     ]
    #
    #     total = sum(
    #         Decimal(str(kondisi or 0))
    #         for status, kondisi in komponen
    #         if status == 1
    #     )
    #
    #     return total.quantize(Decimal('0.00'))
#
# # BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     orm_execute_state.update_execution_options(populate_existing=True)
#     col_descriptions = orm_execute_state.statement.column_descriptions
#     if col_descriptions[0]['entity'] is tpp_kriteria:
#         columns = orm_execute_state.statement.columns
#         if 'id_unit' in columns.keys():
#             if current_user:
#                 member_of_list = current_user['member_of_list']
#                 check_unit_privilege_on_read_db(orm_execute_state, member_of_list, tpp_kriteria)
#
#
# # BEFORE INSERT ADD ID UNIT
# @event.listens_for(db.Session, 'before_flush')
# def before_flush(session, flush_context, instances):
#     for obj in session.new:
#         if isinstance(obj, tpp_kriteria):
#             set_default_unit(None, None, obj)
#
#
# def set_default_unit(mapper, connection, target):
#     if target.id_unit is None:
#         if current_user:
#             member_of_list = current_user['member_of_list']
#             if member_of_list:
#                 target.id_unit = member_of_list[0]
#
#
# # AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
# @event.listens_for(tpp_kriteria, 'after_insert')
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
# @event.listens_for(tpp_kriteria, 'after_update')
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
# @event.listens_for(tpp_kriteria, 'after_delete')
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