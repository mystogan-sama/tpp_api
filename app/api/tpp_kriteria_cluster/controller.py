from flask import request, current_app
from flask_restx import Resource, reqparse, inputs

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, generateDefaultResponse, message, \
    error_response
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .service import Service
from ..tpp_cluster.model import tpp_cluster
from ..tpp_cluster_det.model import tpp_cluster_det
from ..tpp_kriteria_cluster_det.model import tpp_kriteria_cluster_det
from ... import internalApi_byUrl, db
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
    if 'parent_id' in respAndPayloadFields:
        parser.add_argument('flat_mode', type=inputs.boolean, default=False, help='flat response data')
    if filterField:
        for row in filterField:
            parser.add_argument(
                f"{row.replace(':', '').replace('>', '').replace('<', '').replace('=', '').replace('!', '')}")

    #### GET
    @doc.getRespDoc
    @api.expect(parser)
    @token_required
    def get(self):
        return GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)

    #### POST SINGLE/MULTIPLE
    @doc.postRespDoc
    # @api.expect(doc.default_data_response, validate=True)
    @token_required
    def post(self):
        payload = request.get_json()
        print(payload)

        id_cluster = payload['id_cluster']

        # 🔍 Ambil ID Kriteria Cluster berdasarkan ID Unit
        cluster = db.session.query(tpp_cluster).filter_by(id=id_cluster).first()
        if not cluster:
            return {"status": False, "message": "Kriteria cluster tidak ditemukan"}, 404

        cluster_id = cluster.id

        # 🔍 Ambil semua detail kriteria dari cluster
        cluster_dets = db.session.query(tpp_cluster_det).filter_by(
            id_cluster=cluster_id).all()
        if not cluster_dets:
            return {"status": False, "message": "Tidak ada detail kriteria ditemukan"}, 404

        # ✅ Simpan ke tpp_kriteria_kerja (master) terlebih dahulu
        result_post = GeneralPost(doc, crudTitle, Service, request)

        # Pastikan penyimpanan berhasil, dan ambil ID hasil insert
        if not result_post[1] == 200 or not result_post[0].get("data", {}).get("id"):
            return {"status": False, "message": "Gagal menyimpan data kriteria kerja"}, 500

        id_kriteriaCluster = result_post[0]["data"]["id"]

        # 🔁 Simpan semua detail dari cluster ke tpp_kriteria_kerja_det
        for det in cluster_dets:
            cluster_det = tpp_kriteria_cluster_det(
                id_kriteriaCluster=id_kriteriaCluster,
                id_kriteria=det.id_kriteria,
                kriteria_name=det.kriteria_name,
                kriteria_formula=det.kriteria_formula
            )
            db.session.add(cluster_det)

        db.session.commit()

        return result_post
        # return GeneralPost(doc, crudTitle, Service, request)

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


#### GET SUMMARY
@api.route("/summary")
class Summary(Resource):
    @doc.getSummaryRespDoc
    @token_required
    def get(self):
        try:
            args = parser.parse_args()
            resultData = Service.getSummary(args)
            # if not resultData:
            #     return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)
            resp = message(True, generateDefaultResponse(crudTitle, 'get-sum', 200))
            resp['data'] = resultData
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)