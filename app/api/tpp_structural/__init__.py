from flask_restx import fields

from app.utils import DictItem

moduleTitle = ''
crudTitle = 'tpp_structural'
apiPath = 'tpp_structural'
modelName = 'tpp_structural'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "parent_id": fields.Integer(example=1, ),
    "code": fields.String(required=False, max_length=100, example="1.01.01.", ),
    "name": fields.String(required=True, min_length=5, max_length=512, example="tpp_structural sample", ),
    "description": fields.String(required=False, example="Description sample", ),
    "attributes": DictItem(attribute="attributes"),
    "id_unit": fields.Integer(example=1, ),
    "unit_name": fields.String(example="", ),
    "id_unitKerja": fields.Integer(example=1, ),
    "UnitKerja_name": fields.String(readonly=True,required=False, example="", ),
    "JobLevel_name": fields.String(readonly=True,required=False, example="", ),
    "Id_JobLevel": fields.Integer(example=1, ),
    "id_kelas": fields.Integer(example=1, ),
    # 'nilai_tpp_basic': fields.Float(required=False, description='Harga dalam Rupiah'),
    'bpk_ri': fields.Float(required=False, description='Harga dalam Rupiah'),
    'indeks_tpp': fields.Float(required=False, description='Harga dalam Rupiah'),
    "beban_kerja": fields.Float(readonly=True, required=False, example="", ),
    "prestasi_kerja": fields.Float(readonly=True, required=False, example="", ),
    "kondisi_kerja": fields.Float(readonly=True, required=False, example="", ),
}
uniqueField = ["code"]
searchField = ["code", "name", "UnitKerja_name", "JobLevel_name"]
sortField = []
filterField = ["parent_id", "id", "id_unit"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'