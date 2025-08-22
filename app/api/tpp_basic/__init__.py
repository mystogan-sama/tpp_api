from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableInteger

moduleTitle = ''
crudTitle = 'tpp_basic'
apiPath = 'tpp_basic'
modelName = 'tpp_basic'
respAndPayloadFields = {
    "id":  NullableInteger(readonly=True, example=1, ),
    "kelas": fields.Integer(required=False, example="", ),
    "bpk_ri": fields.Fixed(required=False, example="", ),
    'indeks': fields.Float(required=False, description='Harga dalam Rupiah'),
    "nilai_basic_tpp": fields.Fixed(required=False, example="", ),
    'indeks_tpp': fields.Float(required=False, description='Harga dalam Rupiah'),

}
uniqueField = [""]
searchField = ["kelas"]
sortField = [""]
filterField = ["kelas"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'