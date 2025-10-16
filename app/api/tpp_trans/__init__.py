from flask_restx import fields

from app.utils import DictItem

moduleTitle = ''
crudTitle = 'tpp_trans'
apiPath = 'tpp_trans'
modelName = 'tpp_trans'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "id_unit": fields.Integer(example=1),
    "id_jabatan": fields.Integer(example=10),
    "id_unitKerja": fields.Integer(example=20),
    "Id_JobLevel": fields.Integer(example=3),
    "id_kelas": fields.Integer(example=2),
    "jml_pemangku": fields.Integer(required=True, example=5),
    "bulan": fields.Integer(required=True, example=5),
    "basic_tpp": fields.Float(example=3000000.00),  # mssql.MONEY ditranslasikan ke float
    "evidence_beban": fields.String(required=False, example="path/to/evidence1.pdf"),
    "beban_kerja": fields.Float(required=False, example=70),
    "beban_kerja_rp": fields.Fixed(required=False, example="", ),
    "beban_kerja_rp_bln": fields.Fixed(required=False, example="", ),
    "evidence_prestasi": fields.String(required=False, example="path/to/evidence2.pdf"),
    "prestasi_kerja": fields.Float(required=False, example=80),
    "prestasi_kerja_rp": fields.Fixed(required=False, example="", ),
    "prestasi_kerja_rp_bln": fields.Fixed(required=False, example="", ),
    "evidence_kondisi": fields.String(required=False, example="path/to/evidence3.pdf"),
    "kondisi_kerja": fields.Float(required=False, example=60),
    "kondisi_kerja_rp": fields.Fixed(required=False, example="", ),
    "kondisi_kerja_rp_bln": fields.Fixed(required=False, example="", ),
    "evidence_tempat_bekerja": fields.String(required=False, example="path/to/evidence3.pdf"),
    "tempat_bekerja": fields.Float(required=False, example=60),
    "tempat_bekerja_rp": fields.Fixed(required=False, example="", ),
    "tempat_bekerja_rp_bln": fields.Fixed(required=False, example="", ),
    "evidence_kelangkaan_profesi": fields.String(required=False, example="path/to/evidence3.pdf"),
    "kelangkaan_profesi": fields.Float(required=False, example=60),
    "kelangkaan_profesi_rp": fields.Fixed(required=False, example="", ),
    "kelangkaan_profesi_rp_bln": fields.Fixed(required=False, example="", ),
    "evidence_pertimbangan_objektif_lainnya": fields.String(required=False, example="path/to/evidence3.pdf"),
    "pertimbangan_objektif_lainnya": fields.Float(required=False, example=60),
    "pertimbangan_objektif_lainnya_rp": fields.Fixed(required=False, example="", ),
    "pertimbangan_objektif_lainnya_rp_bln": fields.Fixed(required=False, example="", ),
    "nama_jabatan": fields.String(required=False, example="path/to/evidence3.pdf"),
    "total_bulan": fields.Fixed(required=False, example="", ),
    "total_tahun": fields.Fixed(required=False, example="", ),
}
uniqueField = ["code"]
searchField = ["code", "nama_jabatan"]
sortField = ["id"]
filterField = ["id", "id_unit"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'