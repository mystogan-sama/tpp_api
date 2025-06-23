from flask_restx import fields

moduleTitle = ''
crudTitle = 'tpp_jobLevel'
apiPath = 'tpp_jobLevel'
modelName = 'tpp_jobLevel'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "name": fields.String(required=True, min_length=5, max_length=200, ),
    "icon": fields.String(required=False, min_length=5, max_length=100, ),
    "index": fields.Integer(required=True, example=1, ),
    "description": fields.String(required=False, min_length=5, max_length=512, ),
}
uniqueField = []
searchField = ["name"]
sortField = []
filterField = []
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'