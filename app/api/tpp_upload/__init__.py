from flask_restx import fields

moduleTitle = ''
crudTitle = 'tpp_upload'
apiPath = 'tpp_upload'
modelName = 'tpp_upload'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "name": fields.String(required=True, min_length=5, max_length=200, ),
    "url_file": fields.String(required=False, min_length=5, max_length=100, ),
    "created_date": fields.DateTime(readonly=True, example="2023-01-01T00:00:00"),
}
uniqueField = ["name"]
searchField = ["name"]
sortField = ["id"]
filterField = []
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'