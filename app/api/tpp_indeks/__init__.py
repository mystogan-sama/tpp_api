from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableInteger

moduleTitle = ''
crudTitle = 'tpp_indeks'
apiPath = 'tpp_indeks'
modelName = 'tpp_indeks'
respAndPayloadFields = {
    "id":  NullableInteger(readonly=True, example=1, ),
    "kelas_jab": fields.Integer(required=True, example=3, description='Bobot 30%'),
    "ikf": fields.Integer(required=True, example=3, description='Bobot 30%'),

    "ikk_daerah": fields.Float(required=False, example=75.0, description='Bobot 3%'),
    "ikk_jkt": fields.Float(required=False, example=75.0, description='Bobot 3%'),
    "ikk": fields.Float(required=False, example=75.0, description='Bobot 3%'),

    "ippd": fields.Float(required=False, example=75.0, description='Bobot 3%'),

    "olk": fields.Integer(required=True, example=3, description='Bobot 30%'),

    "lppd": fields.Integer(required=False, example=78.5, description='Bobot 25%'),

    "kppd": fields.Integer(required=False, example=81.2, description='Bobot 10%'),

    "hasil_iid": fields.Float(required=False, example=75.0, description='Bobot 3%'),
    "nilai_iid": fields.Integer(required=True, example=82),

    "pkpd": fields.Integer(required=True, example=87, description='Bobot 18%'),

    "hasil_rbpd": fields.Float(required=False, example=79.9, description='Bobot 2%'),
    "nilai_rbpd": fields.Integer(required=True, example=83),

    "irbpd": fields.Integer(required=False, example=72.4, description='Bobot 2%'),

    "hasil_ipm": fields.Float(required=False, example=76.1, description='Bobot 6%'),
    "nilai_ipm": fields.Integer(required=True, example=84),

    "hasil_igr": fields.Float(required=False, example=70.5, description='Bobot 4%'),
    "nilai_igr": fields.Integer(required=True, example=85),

    "total_skor": fields.Float(readonly=True, example=612.1),
    "nilai_ippd": fields.Float(readonly=True, example=612.1),
    "indeks_tpp": fields.Float(readonly=True, example=612.1),
    "created_date": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "tahun": fields.Integer(required=False, example=78.5, description='Bobot 25%'),

}
uniqueField = [""]
searchField = ["kelas"]
sortField = [""]
filterField = ["kelas", "tahun"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'