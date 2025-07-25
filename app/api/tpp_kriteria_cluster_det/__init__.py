from flask_restx import fields

moduleTitle = ''
crudTitle = 'tpp_kriteria_cluster_det'
apiPath = 'tpp_kriteria_cluster_det'
modelName = 'tpp_kriteria_cluster_det'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "id_kriteriaCluster": fields.Integer(required=True, example=1, ),
    "id_kriteria": fields.Integer(example=1, ),
    "kriteria_name": fields.String(example="", ),
    "kriteria_formula": fields.Float(required=False, example=75.0, description='Bobot 3%'),
    "parent_name": fields.String(example="", ),
    "id_parent": fields.Integer(example=1, ),
}
uniqueField = []
searchField = ["unit_name"]
sortField = ["id_parent", "id_kriteria"]
filterField = ["id_kriteriaCluster"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'