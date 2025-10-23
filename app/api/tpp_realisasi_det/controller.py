from decimal import Decimal

from flask import request, current_app
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import func

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, generateDefaultResponse, message, \
    error_response, logger
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .model import tpp_realisasi_det
from .service import Service
from ..tpp_pagu.model import tpp_pagu
from ..tpp_pagu_det.model import tpp_pagu_det
from ..tpp_realisasi.model import tpp_realisasi
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
    # @api.expect(doc.default_data_response, validate=False)
    @token_required
    def post(self):
        return GeneralPost(doc, crudTitle, Service, request)

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
        try:
            data = request.get_json()
            kriteria_realisasi = Decimal(str(data.get('kriteria_realisasi', 0)))
            tahun = current_user['data_year']
            print(kriteria_realisasi)
            existing_det = tpp_realisasi_det.query.filter_by(id=id).first()

            if not existing_det:
                return {"message": f"Data dengan id {id} tidak ditemukan"}, 404

            # 2️⃣ Dapatkan id_realisasi dari data lama
            id_realisasi = existing_det.id_realisasi
            id_kriteria = existing_det.id_kriteria
            print("ID Realisasi:", id_realisasi)

            if not id_realisasi:
                return {"message": "id_realisasi wajib diisi"}, 400

            # Cari record realisasi
            existing_realisasi = tpp_realisasi.query.filter_by(id=id_realisasi).first()
            realisasi_unit = existing_realisasi.id_unit
            realisasi_asn = existing_realisasi.asn
            realisasi_tahun = existing_realisasi.tahun
            realisasi = (
                db.session.query(func.coalesce(func.sum(tpp_realisasi_det.kriteria_realisasi), 0))
                .join(tpp_realisasi, tpp_realisasi_det.id_realisasi == tpp_realisasi.id)
                .filter(
                    tpp_realisasi_det.id_kriteria == id_kriteria,
                    tpp_realisasi.tahun == tahun,
                    tpp_realisasi.asn == realisasi_asn
            )
                .scalar()
            )
            realisasi_decimal = Decimal(realisasi)
            total_realisasi = kriteria_realisasi + realisasi_decimal
            print("Total realisasi:", total_realisasi)
            if not existing_realisasi:
                return {"message": f"Data realisasi dengan ID {id_realisasi} tidak ditemukan"}, 404

            # Ambil nilai dari record realisasi


            # Cari data pagu sesuai unit, asn, dan tahun
            pagu = tpp_pagu.query.filter_by(
                id_unit=realisasi_unit,
                asn=realisasi_asn,
                tahun=realisasi_tahun
            ).first()

            if not pagu:
                return {"message": "Data pagu tidak ditemukan untuk unit, asn, dan tahun tersebut"}, 404

            # Ambil total pagu dari property model
            total_pagu = pagu.total_pagu

            # Jika ingin lihat data detail pagu_det juga
            pagu_det = tpp_pagu_det.query.filter_by(id_pagu=pagu.id, id_kriteria=id_kriteria).all()
            pagu_det_list = [
                {
                    "id": det.id,
                    "id_kriteria": det.id_kriteria,
                    "kriteria_name": det.kriteria_name,
                    "kriteria_pagu": det.kriteria_pagu
                }
                for det in pagu_det
            ]
            kriteria_pagu = [float(item['kriteria_pagu']) for item in pagu_det_list]
            print(f"Total pagu: {total_pagu}")
            print("Detail pagu:", pagu_det_list)
            print(f"Kriteria pagu: {kriteria_pagu}")

            # lanjutkan proses update via GeneralPutById
            return GeneralPutById(
                id,
                doc,
                crudTitle,
                Service,
                request,
                modelName,
                current_user,
                fileFields,
                internalApi_byUrl
            )

        except Exception as e:
            logger.error(e)
            return {"message": str(e)}, 500

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