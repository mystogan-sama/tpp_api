from datetime import datetime
from decimal import Decimal
from threading import Thread

from sqlalchemy import event, extract

from app import db
from app.sso_helper import insert_user_activity, current_user, check_unit_privilege_on_read_db, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName
from ..tpp_indeks.model import tpp_indeks
from ..tpp_kriteria.model import tpp_kriteria


class tpp_structural(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.BigInteger, db.ForeignKey("tpp_structural.id"), nullable=True)
    id_unit = db.Column(db.BigInteger, nullable=True)
    unit_name = db.Column(db.String(200), nullable=True)
    code = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(512), nullable=False, index=True)
    description = db.Column(db.String(512), nullable=True)
    penyetaraan = db.Column(db.Integer, nullable=True)
    attributes = db.Column(db.JSON, nullable=True, server_default='{}')
    id_unitKerja = db.Column(db.BigInteger, db.ForeignKey("tpp_unitKerja.id"), nullable=True)
    Id_JobLevel = db.Column(db.BigInteger, db.ForeignKey("tpp_jobLevel.id"), nullable=True)
    id_kelas = db.Column(db.BigInteger, db.ForeignKey("tpp_basic.kelas"), nullable=True)
    level = db.Column(db.Integer, nullable=True)

    tpp_kriteria_kerja = db.relationship("tpp_kriteria_kerja", backref=modelName, lazy="dynamic")
    tpp_kriteria_kerja_det = db.relationship(
        "tpp_kriteria_kerja_det",
        secondary="tpp_kriteria_kerja",
        primaryjoin="tpp_structural.id == tpp_kriteria_kerja.id_structural",
        secondaryjoin="tpp_kriteria_kerja.id == tpp_kriteria_kerja_det.id_kriteriaKerja",
        viewonly=True,
        lazy='dynamic'
    )
    tpp_trans = db.relationship("tpp_trans", backref=modelName, lazy="dynamic")

    @property
    def UnitKerja_name(self):
        return f"{self.tpp_unitKerja.name}" if self.tpp_unitKerja else None

    @property
    def JobLevel_name(self):
        return f"{self.tpp_jobLevel.name}" if self.tpp_jobLevel else None

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
    #     """Mengembalikan total beban kerja dari kriteria dengan code LIKE '1.%'"""
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("1."):
    #                 try:
    #                     total += Decimal(detail.kriteria_formula or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # @property
    # def beban_kerja_persen(self):
    #     return (self.beban_kerja / Decimal(100))
    #
    # @property
    # def nominal_beban_kerja(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("1."):
    #                 try:
    #                     total += Decimal(detail.kriteria_nominal or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # ### Prestasi Kerja
    # @property
    # def prestasi_kerja(self):
    #     """Mengembalikan total beban kerja dari kriteria dengan code LIKE '1.%'"""
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("2."):
    #                 try:
    #                     total += Decimal(detail.kriteria_formula or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # @property
    # def prestasi_kerja_persen(self):
    #     return (self.prestasi_kerja / Decimal(100))
    #
    # @property
    # def nominal_prestasi_kerja(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("2."):
    #                 try:
    #                     total += Decimal(detail.kriteria_nominal or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # ### Kondisi Kerja
    # @property
    # def kondisi_kerja(self):
    #     """Mengembalikan total beban kerja dari kriteria dengan code LIKE '1.%'"""
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("3."):
    #                 try:
    #                     total += Decimal(detail.kriteria_formula or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # @property
    # def kondisi_kerja_persen(self):
    #     return (self.kondisi_kerja / Decimal(100))
    #
    # @property
    # def nominal_kondisi_kerja(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("3."):
    #                 try:
    #                     total += Decimal(detail.kriteria_nominal or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # ### Tempat Bekerja
    # @property
    # def tempat_bekerja(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("4."):
    #                 try:
    #                     total += Decimal(detail.kriteria_formula or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # @property
    # def tempat_bekerja_persen(self):
    #     return (self.tempat_bekerja / Decimal(100))
    #
    # @property
    # def nominal_tempat_bekerja(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("4."):
    #                 try:
    #                     total += Decimal(detail.kriteria_nominal or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # ### Kelangkaan Profesi
    # @property
    # def kelangkaan_profesi(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("5."):
    #                 try:
    #                     total += Decimal(detail.kriteria_formula or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # @property
    # def kelangkaan_profesi_persen(self):
    #     return (self.kelangkaan_profesi / Decimal(100))
    #
    # @property
    # def nominal_kelangkaan_profesi(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("5."):
    #                 try:
    #                     total += Decimal(detail.kriteria_nominal or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # ## Pertimbangan Objektif Lainnya
    # @property
    # def pertimbangan_objektif_lainnya(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("6."):
    #                 try:
    #                     total += Decimal(detail.kriteria_formula or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))
    #
    # @property
    # def pertimbangan_objektif_lainnya_persen(self):
    #     return (self.pertimbangan_objektif_lainnya / Decimal(100))
    #
    # @property
    # def nominal_pertimbangan_objektif_lainnya(self):
    #     total = Decimal('0.00')
    #
    #     for kerja in self.tpp_kriteria_kerja:  # kerja_list: relasi ke tpp_kriteria_kerja
    #         for detail in kerja.kerja_details:  # kerja_details: relasi ke tpp_kriteria_kerja_det
    #             if detail.kriteria and detail.kriteria.code.startswith("6."):
    #                 try:
    #                     total += Decimal(detail.kriteria_nominal or 0)
    #                 except:
    #                     continue
    #
    #     return total.quantize(Decimal('0.00'))


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
# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_structural)


# # BEFORE INSERT ADD ID UNIT
# @event.listens_for(db.Session, 'before_flush')
# def before_flush(session, flush_context, instances):
#     for obj in session.new:
#         if isinstance(obj, tpp_structural):
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
# @event.listens_for(tpp_structural, 'after_insert')
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
# @event.listens_for(tpp_structural, 'after_update')
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
# @event.listens_for(tpp_structural, 'after_delete')
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