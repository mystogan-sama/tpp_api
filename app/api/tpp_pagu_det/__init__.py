from flask_restx import fields

moduleTitle = ''
crudTitle = 'tpp_pagu_det'
apiPath = 'tpp_pagu_det'
modelName = 'tpp_pagu_det'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "id_pagu": fields.Integer(required=True, example=1, ),
    "id_kriteria": fields.Integer(example=1, ),
    "kriteria_code": fields.String(example="", ),
    "kriteria_name": fields.String(example="", ),
    "kriteria_pagu": fields.Fixed(example=1, ),
    "total_realisasi": fields.Fixed(example=1, ),
}
uniqueField = []
searchField = ["unit_name"]
sortField = ["id_parent", "kriteria_code"]
filterField = ["id_pagu"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'