from decimal import Decimal
from threading import Thread

from sqlalchemy.dialects import mssql
from sqlalchemy import event

from app import db
from app.sso_helper import insert_user_activity, current_user, check_unit_privilege_on_read_db, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class tpp_trans(db.Model):
    __tablename__ = f'{modelName}'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    id_unit = db.Column(db.BigInteger, nullable=True)
    id_jabatan = db.Column(db.BigInteger, db.ForeignKey("tpp_structural.id"), nullable=True)
    id_unitKerja = db.Column(db.BigInteger, nullable=True)
    Id_JobLevel = db.Column(db.Integer, nullable=True)
    id_kelas = db.Column(db.BigInteger, nullable=True)
    asn = db.Column(db.Integer, nullable=False)
    jml_pemangku = db.Column(db.Integer, nullable=False)
    bulan = db.Column(db.Integer, nullable=False)
    basic_tpp = db.Column(mssql.MONEY, nullable=True)
    evidence_beban = db.Column(db.String(1024), nullable=True, index=True)
    beban_kerja = db.Column(db.DECIMAL(18, 2), nullable=True)
    beban_kerja_rp = db.Column(mssql.MONEY, nullable=True)
    beban_kerja_rp_bln = db.Column(mssql.MONEY, nullable=True)
    evidence_prestasi = db.Column(db.String(1024), nullable=True, index=True)
    prestasi_kerja = db.Column(db.DECIMAL(18, 2), nullable=True)
    prestasi_kerja_rp = db.Column(mssql.MONEY, nullable=True)
    prestasi_kerja_rp_bln = db.Column(mssql.MONEY, nullable=True)
    evidence_kondisi = db.Column(db.String(1024), nullable=True, index=True)
    kondisi_kerja = db.Column(db.DECIMAL(18, 2), nullable=True)
    kondisi_kerja_rp = db.Column(mssql.MONEY, nullable=True)
    kondisi_kerja_rp_bln = db.Column(mssql.MONEY, nullable=True)
    evidence_tempat_bekerja = db.Column(db.String(1024), nullable=True, index=True)
    tempat_bekerja = db.Column(db.DECIMAL(18, 2), nullable=True)
    tempat_bekerja_rp = db.Column(mssql.MONEY, nullable=True)
    tempat_bekerja_rp_bln = db.Column(mssql.MONEY, nullable=True)
    evidence_kelangkaan_profesi = db.Column(db.String(1024), nullable=True, index=True)
    kelangkaan_profesi = db.Column(db.DECIMAL(18, 2), nullable=True)
    kelangkaan_profesi_rp = db.Column(mssql.MONEY, nullable=True)
    kelangkaan_profesi_rp_bln = db.Column(mssql.MONEY, nullable=True)
    evidence_pertimbangan_objektif_lainnya = db.Column(db.String(1024), nullable=True, index=True)
    pertimbangan_objektif_lainnya = db.Column(db.DECIMAL(18, 2), nullable=True)
    pertimbangan_objektif_lainnya_rp = db.Column(mssql.MONEY, nullable=True)
    pertimbangan_objektif_lainnya_rp_bln = db.Column(mssql.MONEY, nullable=True)
    total_bulan_orang = db.Column(mssql.MONEY, nullable=True)
    total_bulan = db.Column(mssql.MONEY, nullable=True)
    total_tahun = db.Column(mssql.MONEY, nullable=True)

    #
    #
    @property
    def nama_jabatan(self):
        return f"{self.tpp_structural.name}" if self.tpp_structural else None
    #
    # @property
    # def total_bulan(self):
    #     """
    #     Menghitung total per bulan dari:
    #     beban_kerja_rp + prestasi_kerja_rp + kondisi_kerja_rp
    #     Mengembalikan nilai dalam format Decimal dengan 2 digit desimal
    #     """
    #     beban = Decimal(str(self.beban_kerja_rp or 0))
    #     prestasi = Decimal(str(self.prestasi_kerja_rp or 0))
    #     kondisi = Decimal(str(self.kondisi_kerja_rp or 0))
    #     tempat = Decimal(str(self.tempat_bekerja_rp or 0))
    #     profesi = Decimal(str(self.kelangkaan_profesi_rp or 0))
    #     pol = Decimal(str(self.pertimbangan_objektif_lainnya_rp or 0))
    #
    #     total = beban + prestasi + kondisi + tempat + profesi + pol
    #     return total.quantize(Decimal('0.00'))
    #
    # @property
    # def total_tahun(self):
    #     """
    #     Menghitung total per tahun (total_bulan * 12)
    #     Mengembalikan nilai dalam format Decimal dengan 2 digit desimal
    #     """
    #     bulanan = self.total_bulan  # Sudah dalam format Decimal
    #     tahunan = bulanan * self.bulan
    #     return tahunan.quantize(Decimal('0.00'))


# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     check_unit_and_employee_privilege_on_read_db(orm_execute_state, tpp_trans)
#
# # BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
# @event.listens_for(db.session, "do_orm_execute")
# def check_unit_privilege_read(orm_execute_state):
#     orm_execute_state.update_execution_options(populate_existing=True)
#     col_descriptions = orm_execute_state.statement.column_descriptions
#     if col_descriptions[0]['entity'] is tpp_trans:
#         columns = orm_execute_state.statement.columns
#         if 'id_unit' in columns.keys():
#             if current_user:
#                 member_of_list = current_user['member_of_list']
#                 check_unit_privilege_on_read_db(orm_execute_state, member_of_list, tpp_trans)
#
#
# # BEFORE INSERT ADD ID UNIT
# @event.listens_for(db.Session, 'before_flush')
# def before_flush(session, flush_context, instances):
#     for obj in session.new:
#         if isinstance(obj, tpp_trans):
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
# @event.listens_for(tpp_trans, 'after_insert')
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
# @event.listens_for(tpp_trans, 'after_update')
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
# @event.listens_for(tpp_trans, 'after_delete')
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