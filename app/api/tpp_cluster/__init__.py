from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableInteger

moduleTitle = ''
crudTitle = 'tpp_cluster'
apiPath = 'tpp_cluster'
modelName = 'tpp_cluster'
respAndPayloadFields = {
    "id":  NullableInteger(readonly=True, example=1, ),
    "name": fields.String(required=True, min_length=5, max_length=512, example="tpp_structural sample", ),
    "description": fields.String(required=False, example="Description sample", ),
}
uniqueField = ["name"]
searchField = ["kelas"]
sortField = ["id"]
filterField = ["kelas"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'