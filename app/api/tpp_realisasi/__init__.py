from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableInteger

moduleTitle = ''
crudTitle = 'tpp_realisasi'
apiPath = 'tpp_realisasi'
modelName = 'tpp_realisasi'
respAndPayloadFields = {
    "id":  NullableInteger(readonly=True, example=1, ),
    "id_unit": fields.Integer(required=True, example=1001),
    "unit_name": fields.String(example="", ),
    "asn": fields.Integer(required=False, example=1),
    "bulan": fields.Integer(required=False, example=1),
    "bulan_str": fields.String(example="", ),
    "total_realisasi": fields.Fixed(example=1, ),
    "tahun": fields.Integer(required=False, example=1),
}
uniqueField = [""]
searchField = ["id_unit"]
sortField = ["id", "asn", "bulan"]
filterField = ["id_unit", "asn", "bulan", "tahun"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'