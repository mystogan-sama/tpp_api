from flask_restx import fields

moduleTitle = ''
crudTitle = 'tpp_kriteria_cluster'
apiPath = 'tpp_kriteria_cluster'
modelName = 'tpp_kriteria_cluster'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "id_unit": fields.Integer(example=1, ),
    "unit_name": fields.String(example="", ),
    "id_cluster": fields.Integer(required=True, example=1, ),
    "cluster_name": fields.String(example="", ),
}
uniqueField = []
searchField = ["unit_name"]
sortField = []
filterField = ["id_unit", "id_cluster"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'