from flask_restx import fields

from app.utils import DictItem

moduleTitle = ''
crudTitle = 'tpp_kriteria'
apiPath = 'tpp_kriteria'
modelName = 'tpp_kriteria'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "parent_id": fields.Integer(example=1, ),
    "code": fields.String(required=False, max_length=100, example="1.01.01.", ),
    "name": fields.String(required=True, min_length=5, max_length=512, example="tpp_kriteria sample", ),
    "formula": fields.Float(readonly=True, required=False, example="", ),
    "nominal": fields.Fixed(example=1, ),
    "depth": fields.Integer(example=1, ),
}
uniqueField = ["code", "name"]
searchField = ["code", "name"]
sortField = []
filterField = ["parent_id", "id", "depth", "kriteria", "disabled"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'