from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableInteger

moduleTitle = ''
crudTitle = 'tpp_pagu'
apiPath = 'tpp_pagu'
modelName = 'tpp_pagu'
respAndPayloadFields = {
    "id":  NullableInteger(readonly=True, example=1, ),
    "id_unit": fields.Integer(required=True, example=1001),
    "unit_name": fields.String(example="", ),
    "asn": fields.Integer(required=False, example=1),
    "total_pagu": fields.Fixed(example=1, ),
    "tahun": fields.Integer(required=False, example=1),
}
uniqueField = [""]
searchField = ["id_unit"]
sortField = ["id", "asn"]
filterField = ["id_unit", "asn"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'