from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableInteger

moduleTitle = ''
crudTitle = 'tpp_kriteria_kerja'
apiPath = 'tpp_kriteria_kerja'
modelName = 'tpp_kriteria_kerja'
respAndPayloadFields = {
    "id":  NullableInteger(readonly=True, example=1, ),
    "id_unit": fields.Integer(required=True, example=1001),
    "unit_name": fields.String(example="", ),
    "id_structural": fields.Integer(required=True, example=2001),
    "id_kelas": fields.Integer(required=True, example=2001),
    "id_cluster": fields.Integer(required=True, example=2001),
    "cluster_name": fields.String(example="", ),
    "asn": fields.Integer(required=False, example=1),

    # Beban kerja
    "beban_kerja": fields.Float(required=False, example=40),

    # Prestasi kerja
    # "status_prestasi": fields.Integer(required=False, example=1),
    # "prestasi": fields.Integer(required=False, example=85),
    "status_tapd": fields.Integer(required=False, example=1),
    "prestasi_tapd": fields.Float(required=False, example=90),
    "status_pptk": fields.Integer(required=False, example=1),
    "prestasi_pptk": fields.Float(required=False, example=80),
    "status_ja": fields.Integer(required=False, example=1),
    "prestasi_ja": fields.Float(required=False, example=75),
    "status_jf": fields.Integer(required=False, example=1),
    "prestasi_jf": fields.Float(required=False, example=88),
    "status_jp": fields.Integer(required=False, example=1),
    "prestasi_jp": fields.Float(required=False, example=92),
    "status_p_keu": fields.Integer(required=False, example=1),
    "prestasi_p_keu": fields.Float(required=False, example=95),

    # Kondisi kerja
    "status_pengawasan": fields.Integer(required=False, example=1),
    "kondisi_pengawasan": fields.Float(required=False, example=70),
    "status_kesehatan": fields.Integer(required=False, example=1),
    "kondisi_kesehatan": fields.Float(required=False, example=65),
    "status_k_p_keu": fields.Integer(required=False, example=1),
    "kondisi_p_keu": fields.Float(required=False, example=75),
    "status_perencanaan": fields.Integer(required=False, example=1),
    "kondisi_perencanaan": fields.Float(required=False, example=80),
    "status_trantibumlinmas": fields.Integer(required=False, example=1),
    "kondisi_trantibumlinmas": fields.Float(required=False, example=85),
    "status_bijak_kdh": fields.Integer(required=False, example=1),
    "kondisi_bijak_kdh": fields.Float(required=False, example=90),
    "status_resiko_kerja": fields.Integer(required=False, example=1),
    "kondisi_resiko_kerja": fields.Float(required=False, example=55),
    "status_resiko_tinggi": fields.Integer(required=False, example=1),
    "kondisi_resiko_tinggi": fields.Float(required=False, example=60),

    # Kelangkaan profesi
    "status_kelangkaan_profesi": fields.Integer(required=False, example=1),
    "kelangkaan_profesi": fields.Float(required=False, example=50),

    # Tempat bertugas
    "status_tempat_bertugas": fields.Integer(required=False, example=1),
    "tempat_bertugas": fields.Float(required=False, example=45),

    # Objektif lainnya
    "status_objektif_lainnya": fields.Integer(required=False, example=1),
    "objektif_lainnya": fields.Float(required=False, example=30),

    # Timestamp (opsional)
    "created_date": fields.DateTime(readonly=True, example="2023-01-01T00:00:00"),
    "structural_name": fields.String(required=False),

}
uniqueField = [""]
searchField = ["id_unit"]
sortField = ["id_kelas"]
filterField = ["id_unit", "id_kriteriaKerja", "detail", "id_cluster"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'