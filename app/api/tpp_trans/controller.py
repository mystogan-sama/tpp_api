import requests
from flask import request
from flask_restx import Resource, reqparse, inputs

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, message, generateDefaultResponse, \
    row2dict_same_api_res, genRecrusive, logger, error_response
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .service import Service
from ... import internalApi_byUrl
from ...sso_helper import token_required, current_user

api = doc.api

parser = reqparse.RequestParser()
parser.add_argument('fetch_child', type=inputs.boolean, help='boolean input for fetch unit children', default=True)

parser.add_argument('sort', type=str, help='for sorting, fill with column name')
parser.add_argument('sort_dir', type=str, choices=('asc', 'desc'), help='fill with "asc" or "desc"')


#### LIST
@api.route("")
class List(Resource):
    if enabledPagination:
        parser.add_argument('page', type=int, help='page/start, fill with number')
        parser.add_argument('length', type=int, help='length of data, fill with number')
        parser.add_argument('search', type=str, help='for filter searching')
    # if 'parent_id' in respAndPayloadFields:
    #     parser.add_argument('flat_mode', type=inputs.boolean, default=False, help='flat response data')
    if filterField:
        for row in filterField:
            parser.add_argument(
                f"{row.replace(':', '').replace('>', '').replace('<', '').replace('=', '').replace('!', '')}")

    @doc.getRespDoc
    @api.expect(parser)
    @token_required
    def get(self):
        # args = parser.parse_args()
        insert_data = GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)
        print(insert_data)
        return insert_data
        # return GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, args, asData=True)
        # try:
        #     resultData = Service.getDataAll(args)
        #
        #     headers = {
        #         'Authorization': request.headers.get('Authorization')
        #     }
        #     employeeReq = requests.get('https://hr-api.insaba.co.id/Employee?sort_dir=desc&sort=id&page=1&length=100',
        #                                headers=headers)
        #     employeeJson = employeeReq.json()
        #     employeeDataJson = employeeJson['data'] if 'data' in employeeJson else []
        #     # print(employeeDataJson)
        #     resp = message(True, generateDefaultResponse(crudTitle, 'get-list', 200))
        #     resultJson = []
        #     if args['flat_mode']:
        #         resp = message(True, generateDefaultResponse(crudTitle, 'get-list', 200))
        #         for row in resultData:
        #             resultJson.append(row2dict_same_api_res(row, doc.default_data_response))
        #     else:
        #         root = {'id': None}
        #         resultDataNew = []
        #         for val in resultData:
        #             newRow = row2dict_same_api_res(val, doc.default_data_response)
        #             # print(newRow)
        #             newRow['expanded'] = True
        #             newRow['checked'] = False
        #             detail = [{
        #                 "name": f"{d['FirstName']} {d['LastName']}",
        #                 "id_number": d['EmployeeIdNumber'],
        #                 "avatar": d['PhotoPath']
        #             } for d in employeeDataJson if d.get('Id_tpp_trans') == val.id]
        #             # print(detail)
        #             newRow['detail'] = detail
        #             resultDataNew.append(newRow)
        #         genRecrusive(sorted(resultDataNew,
        #                             key=lambda d: d['index'] if 'index' in d else d['code'] if 'code' in d else 0),
        #                      root)
        #         resultJson = root['children']
        #     resp['data'] = resultJson
        #     return resp, 200
        # except Exception as e:
        #     logger.error(e)
        #     return error_response(generateDefaultResponse(crudTitle, 'get-list', 500), 500)
        #


    #### POST SINGLE/MULTIPLE
    @doc.postRespDoc
    @api.expect(doc.default_data_response, validate=True)
    @token_required
    def post(self):
        try:
            return GeneralPost(doc, crudTitle, Service, request)
        except Exception as e:
            logger.error(e)
        
        

    #### MULTIPLE-DELETE
    @doc.deleteMultiRespDoc
    @api.expect(doc.default_delete_multi_payload, validate=True)
    @token_required
    def delete(self):
        return GeneralDelete(crudTitle, Service, request, fileFields, modelName, current_user, internalApi_byUrl)


#### BY ID
@api.route("/<int:id>")
class ById(Resource):
    #### GET
    @doc.getByIdRespDoc
    @token_required
    def get(self, id):
        return GeneralGetById(id, doc, crudTitle, Service)

    #### PUT
    @doc.putRespDoc
    @api.expect(doc.default_data_response)
    @token_required
    def put(self, id):
        return GeneralPutById(id, doc, crudTitle, Service, request, modelName, current_user, fileFields,
                              internalApi_byUrl)

    #### DELETE
    @doc.deleteRespDoc
    @token_required
    def delete(self, id):
        return GeneralDeleteById(id, doc, crudTitle, Service, request, modelName, current_user, fileFields,
                                 internalApi_byUrl)