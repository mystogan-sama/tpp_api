from decimal import Decimal, InvalidOperation

import requests
from flask import request, current_app, jsonify
from flask_restx import Resource, reqparse, inputs

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, message, generateDefaultResponse, \
    row2dict_same_api_res, genRecrusive, logger, error_response
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .model import tpp_trans
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

    @staticmethod
    def safe_decimal(value):
        """Konversi aman ke Decimal. Jika None atau tidak valid → Decimal(0)."""
        try:
            if value is None or value == "":
                return Decimal(0)
            return Decimal(str(value))
        except (InvalidOperation, ValueError, TypeError):
            return Decimal(0)

    @doc.getRespDoc
    @api.expect(parser)
    @token_required
    def get(self):
        # args = parser.parse_args()
        insert_data = GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)
        # print(insert_data)
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
    # @api.expect(doc.default_data_response, validate=True)
    @token_required
    def post(self):
        # try:
        #     data = request.get_json() or {}
        #
        #     # =====================================================
        #     # DATA LAIN
        #     # =====================================================
        #     nominal = self.safe_decimal(data.get("total_bulan_orang"))
        #     id_unit = data.get("id_unit")
        #     id_unitKerja = data.get("id_unitKerja")
        #     asn = data.get("asn")
        #
        #     print(
        #         f"📥 Data diterima: "
        #         f"id_kelas={kelas}, nominal={nominal}, "
        #         f"id_unit={id_unit}, id_unitKerja={id_unitKerja}, asn={asn}"
        #     )
        #
        #     # =====================================================
        #     # 🔍 Cari atasan (kelas lebih tinggi, ASN sama)
        #     # =====================================================
        #     atasan = (
        #         tpp_trans.query
        #         .filter(
        #             tpp_trans.id_unit == id_unit,
        #             tpp_trans.id_kelas > kelas,
        #             tpp_trans.asn == asn
        #         )
        #         .order_by(tpp_trans.id_kelas.asc())
        #         .first()
        #     )
        #
        #     if atasan:
        #         print(
        #             f"✅ Ditemukan atasan: id_kelas={atasan.id_kelas}, ASN={atasan.asn}"
        #         )
        #         print(f"📊 total_bulan_orang atasan={atasan.total_bulan_orang}")
        #
        #     else:
        #         print("⚠️ Tidak ada data atasan dengan kelas lebih tinggi.")
        #
        #     # =====================================================
        #     # 🔢 Normalisasi field numerik
        #     # =====================================================
        #     numeric_fields = [
        #         "beban_kerja",
        #         "prestasi_kerja",
        #         "kondisi_kerja",
        #         "tempat_bekerja",
        #         "kelangkaan_profesi",
        #         "pertimbangan_objektif_lainnya",
        #     ]
        #
        #     for field in numeric_fields:
        #         if field in data and data[field] is not None:
        #             try:
        #                 if isinstance(data[field], str):
        #                     data[field] = float(data[field].replace(",", ""))
        #                 else:
        #                     data[field] = float(data[field])
        #
        #                 data[field] = float(
        #                     Decimal(str(data[field])).quantize(Decimal("0.00"))
        #                 )
        #             except Exception:
        #                 data[field] = None
        #
        #     # =====================================================
        #     # 🧹 BERSIHKAN FIELD TEMPORER
        #     # =====================================================
        #     data.pop("id_kelas_post", None)
        #
        #     # =====================================================
        #     # 🚀 SIMPAN
        #     # =====================================================
        #     request._cached_json = data
        #     return GeneralPost(doc, crudTitle, Service, request)
        #
        # except Exception as e:
        #     logger.error(e)
        #     return {"message": str(e)}, 400
        #KODE SEBELUMNYA YANG JALAN
        try:
            data = request.get_json()
            kelas = int(data.get('id_kelas', 1))
            nominal = self.safe_decimal(data.get("total_bulan_orang"))
            id_unitKerja = data.get('id_unitKerja')
            id_unit = data.get('id_unit')
            asn = data.get('asn')  # <-- penting untuk filter

            print(f"📥 Data diterima: kelas={kelas}, nominal={nominal}, id_unitKerja={id_unitKerja}, asn={asn}")

            # 🔍 Cari atasan: harus 1 unit kerja, kelas lebih tinggi, dan ASN sama
            atasan = (
                tpp_trans.query
                .filter(
                    tpp_trans.id_unit == id_unit,
                    tpp_trans.id_kelas > kelas,
                    tpp_trans.asn == asn  # <-- Filter tambahan ASN
                )
                .order_by(tpp_trans.id_kelas.asc())
                .first()
            )

            if atasan:
                print(f"✅ Ditemukan atasan: id_kelas={atasan.id_kelas}, ASN={atasan.asn}")
                print(f"📊 total_bulan_orang atasan={atasan.total_bulan_orang}")

                kelas_atasan = atasan.id_kelas
                atasan_total = self.safe_decimal(atasan.total_bulan_orang)

                # 🧩 VALIDASI — tidak boleh lebih besar dari atasan
                # if nominal > atasan_total:
                #     print("⛔ Nominal bawahan lebih besar dari atasan! Gagal disimpan.")
                #     return {
                #         "status": "error",
                #         "message": (
                #             f"Total TPP bawahan ({nominal}) tidak boleh lebih besar "
                #             f"dari TPP kelas diatasnya (Kelas {kelas_atasan}) sebesar {atasan_total}."
                #         )
                #     }, 400
                #
                # print("✅ Validasi OK, lanjutkan penyimpanan data.")
            else:
                print("⚠️ Tidak ada data atasan dengan kelas lebih tinggi dan ASN yang sama.")

            # -- konversi angka numeric agar valid --
            numeric_fields = [
                "beban_kerja",
                "prestasi_kerja",
                "kondisi_kerja",
                "tempat_bekerja",
                "kelangkaan_profesi",
                "pertimbangan_objektif_lainnya",
            ]
            for field in numeric_fields:
                if field in data and data[field] is not None:
                    try:
                        if isinstance(data[field], str):
                            data[field] = float(data[field].replace(",", ""))
                        else:
                            data[field] = float(data[field])
                        data[field] = float(
                            Decimal(str(data[field])).quantize(Decimal("0.00"))
                        )
                    except:
                        data[field] = None
            # ✅ lanjut simpan
            return GeneralPost(doc, crudTitle, Service, request)

        except Exception as e:
            logger.error(e)
            return {"message": str(e)}, 400

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

@api.route("/summary")
class Summary(Resource):
    @doc.getSummaryRespDoc
    @token_required
    def get(self):
        try:
            current_app.logger.info("Memanggil Service.getSummary()")
            resultData = Service.getSummary({})

            resp = message(True, generateDefaultResponse(crudTitle, 'get-sum', 200))
            # pastikan selalu list
            resp['data'] = [resultData] if isinstance(resultData, dict) else (resultData or [])
            return resp, 200

        except Exception as e:
            current_app.logger.error(f"Error in Summary GET: {e}")
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)

@api.route("/summaryP3K")
class Summary(Resource):
    @doc.getSummaryRespDoc
    @token_required
    def get(self):
        try:
            current_app.logger.info("Memanggil Service.getSummary()")
            resultData = Service.getSummaryP3K({})

            resp = message(True, generateDefaultResponse(crudTitle, 'get-sum', 200))
            # pastikan selalu list
            resp['data'] = [resultData] if isinstance(resultData, dict) else (resultData or [])
            return resp, 200

        except Exception as e:
            current_app.logger.error(f"Error in Summary GET: {e}")
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)

@api.route("/summaryKriteriaPNS")
class Summary(Resource):
    @doc.getSummaryRespDoc
    @token_required
    def get(self):
        try:
            current_app.logger.info("Memanggil Service.getSummary()")
            resultData = Service.getSummaryKriteriaPNS({})

            resp = message(True, generateDefaultResponse(crudTitle, 'get-sum', 200))
            # pastikan selalu list
            resp['data'] = [resultData] if isinstance(resultData, dict) else (resultData or [])
            return resp, 200

        except Exception as e:
            current_app.logger.error(f"Error in Summary GET: {e}")
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)

@api.route("/summaryKriteriaP3K")
class Summary(Resource):
    @doc.getSummaryRespDoc
    @token_required
    def get(self):
        try:
            current_app.logger.info("Memanggil Service.getSummary()")
            resultData = Service.getSummaryKriteriaP3K({})

            resp = message(True, generateDefaultResponse(crudTitle, 'get-sum', 200))
            # pastikan selalu list
            resp['data'] = [resultData] if isinstance(resultData, dict) else (resultData or [])
            return resp, 200

        except Exception as e:
            current_app.logger.error(f"Error in Summary GET: {e}")
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)

@api.route("/summaryPaguStr")
class Summary(Resource):
    @doc.getSummaryRespDoc
    @token_required
    def get(self):
        try:
            current_app.logger.info("Memanggil Service.getSummary()")
            resultData = Service.getSummaryPaguStr({})

            resp = message(True, generateDefaultResponse(crudTitle, 'get-sum', 200))
            # pastikan selalu list
            resp['data'] = [resultData] if isinstance(resultData, dict) else (resultData or [])
            return resp, 200

        except Exception as e:
            current_app.logger.error(f"Error in Summary GET: {e}")
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)

@api.route("/summaryPaguKelasPNS")
class Summary(Resource):
    @doc.getSummaryRespDoc
    @token_required
    def get(self):
        try:
            current_app.logger.info("Memanggil Service.getSummary()")
            resultData = Service.getSummaryPaguKelasPNS({})

            resp = message(True, generateDefaultResponse(crudTitle, 'get-sum', 200))
            # pastikan selalu list
            resp['data'] = [resultData] if isinstance(resultData, dict) else (resultData or [])
            return resp, 200

        except Exception as e:
            current_app.logger.error(f"Error in Summary GET: {e}")
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)