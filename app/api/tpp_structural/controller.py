import decimal
import json
from datetime import datetime

import requests
from flask import request
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import text

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, message, generateDefaultResponse, \
    row2dict_same_api_res, genRecrusive, logger, error_response
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .service import Service
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

    @doc.getRespDoc
    @api.expect(parser)
    @token_required
    def get(self):
        # args = parser.parse_args()
        args = parser.parse_args()
        if args["struktur"] == '1' and args['id_unit']:
            # Buat kondisi WHERE dinamis
            where_clauses = [f"ts.id_unit = {args['id_unit']}"]

            if args.get('id_unitKerja'):
                where_clauses.append(f"ts.id_unitKerja = {args['id_unitKerja']}")
            if args.get('asn'):
                where_clauses.append(f"tkk.asn = {args['asn']}")

            # Gabungkan semua kondisi jadi satu string
            where_clause = " AND ".join(where_clauses)

            sqlQuery = text(f'''
                SELECT 
                    ts.id,
                    ts.name,
                    ts.id_unit,
                    ts.id_kelas,
                    ts.id_unitKerja,
                    ts.Id_JobLevel,
                    ts.description,
                    tkc.id_cluster,
                    tb.bpk_ri,

                    -- === 1. Beban Kerja ===
                    SUM(CASE WHEN tk.code LIKE '1.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) AS beban_kerja,
                    SUM(CASE WHEN tk.code LIKE '1.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) / 100 AS beban_kerja_persen,
                    SUM(CASE WHEN tk.code LIKE '1.%' THEN CAST(tkkd.kriteria_nominal AS DECIMAL(18,2)) ELSE 0 END) AS nominal_beban_kerja,

                    -- === 2. Prestasi Kerja ===
                    SUM(CASE WHEN tk.code LIKE '2.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) AS prestasi_kerja,
                    SUM(CASE WHEN tk.code LIKE '2.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) / 100 AS prestasi_kerja_persen,
                    SUM(CASE WHEN tk.code LIKE '2.%' THEN CAST(tkkd.kriteria_nominal AS DECIMAL(18,2)) ELSE 0 END) AS nominal_prestasi_kerja,

                    -- === 3. Kondisi Kerja ===
                    SUM(CASE WHEN tk.code LIKE '3.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) AS kondisi_kerja,
                    SUM(CASE WHEN tk.code LIKE '3.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) / 100 AS kondisi_kerja_persen,
                    SUM(CASE WHEN tk.code LIKE '3.%' THEN CAST(tkkd.kriteria_nominal AS DECIMAL(18,2)) ELSE 0 END) AS nominal_kondisi_kerja,

                    -- === 4. Tempat Bekerja ===
                    SUM(CASE WHEN tk.code LIKE '4.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) AS tempat_bekerja,
                    SUM(CASE WHEN tk.code LIKE '4.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) / 100 AS tempat_bekerja_persen,
                    SUM(CASE WHEN tk.code LIKE '4.%' THEN CAST(tkkd.kriteria_nominal AS DECIMAL(18,2)) ELSE 0 END) AS nominal_tempat_bekerja,

                    -- === 5. Kelangkaan Profesi ===
                    SUM(CASE WHEN tk.code LIKE '5.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) AS kelangkaan_profesi,
                    SUM(CASE WHEN tk.code LIKE '5.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) / 100 AS kelangkaan_profesi_persen,
                    SUM(CASE WHEN tk.code LIKE '5.%' THEN CAST(tkkd.kriteria_nominal AS DECIMAL(18,2)) ELSE 0 END) AS nominal_kelangkaan_profesi,

                    -- === 6. Pertimbangan Objektif Lainnya ===
                    SUM(CASE WHEN tk.code LIKE '6.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) AS pertimbangan_objektif_lainnya,
                    SUM(CASE WHEN tk.code LIKE '6.%' THEN CAST(tkkd.kriteria_formula AS DECIMAL(18,2)) ELSE 0 END) / 100 AS pertimbangan_objektif_lainnya_persen,
                    SUM(CASE WHEN tk.code LIKE '6.%' THEN CAST(tkkd.kriteria_nominal AS DECIMAL(18,2)) ELSE 0 END) AS nominal_pertimbangan_objektif_lainnya,

                    -- === Indeks TPP (hasil perhitungan) ===
                    (SELECT TOP 1 ti.indeks_tpp 
                     FROM tpp_indeks ti
                     WHERE YEAR(ti.created_date) = YEAR(GETDATE())
                     ORDER BY ti.created_date DESC)
                     AS indeks_tpp

                FROM tpp_structural AS ts
                INNER JOIN tpp_kriteria_cluster AS tkc 
                    ON tkc.id_unit = ts.id_unit
                INNER JOIN tpp_kriteria_kerja AS tkk 
                    ON tkk.id_cluster = tkc.id_cluster
                    AND tkk.id_kelas = ts.id_kelas
                INNER JOIN tpp_basic AS tb 
                    ON tb.kelas = ts.id_kelas
                LEFT JOIN tpp_kriteria_kerja_det AS tkkd
                    ON tkkd.id_kriteriaKerja = tkk.id
                LEFT JOIN tpp_kriteria AS tk
                    ON tk.id = tkkd.id_kriteria
                WHERE {where_clause}
                GROUP BY 
                    ts.id, ts.name, ts.id_unit, ts.id_kelas, ts.id_unitKerja, ts.Id_JobLevel, ts.description, tkc.id_cluster, tb.bpk_ri;
            ''')

            data = db.engine.execute(sqlQuery)
            d, a = {}, []
            for rowproxy in data:
                for column, value in rowproxy.items():
                    if isinstance(value, datetime):
                        d = {**d, **{column: value.isoformat()}}
                    elif isinstance(value, decimal.Decimal):
                        d = {**d, **{column: float(value)}}
                    else:
                        d = {**d, **{column: value}}
                a.append(d)

            resp = message(True, generateDefaultResponse(crudTitle, 'get-list', 200))
            resp['data'] = a
            return resp, 200

        elif args.get("struktur") == '2' and args.get('id_unitKerja') and args.get('level'):
            id_unitKerja = args.get('id_unitKerja')
            level = int(args.get('level', 1))

            print(f"Level diterima: {level}, ID UnitKerja: {id_unitKerja}")

            if level == 1:
                print("🔹 Level 1 terdeteksi: tidak memiliki atasan. Menampilkan data dummy.")
                a = [{
                    "id": None,
                    "id_unitKerja": id_unitKerja,
                    "name": "Tidak ada atasan",
                    "description": None,
                    "level": None,
                    "created_at": None,
                    "updated_at": None
                }]
                resp = message(True, generateDefaultResponse(crudTitle, 'get-list', 200))
                resp['data'] = a
                return resp, 200

            # Level satu tingkat di atas
            level_atas = max(level - 1, 1)

            # Query pertama
            sqlQuery = text('''
                SELECT *
                FROM tpp_structural
                WHERE id_unitKerja = :id_unitKerja
                  AND CAST(level AS CHAR) = :level_atas
            ''')

            data = db.engine.execute(sqlQuery, {
                'id_unitKerja': id_unitKerja,
                'level_atas': str(level_atas)
            })

            a = []
            for rowproxy in data:
                d = {}
                for column, value in rowproxy.items():
                    if isinstance(value, datetime):
                        d[column] = value.isoformat()
                    elif isinstance(value, decimal.Decimal):
                        d[column] = float(value)
                    else:
                        d[column] = value
                a.append(d)

            # Jika kosong, coba dua level di atas
            if not a:
                level_dua_atas = max(level - 2, 1)
                print(f"Tidak ditemukan di level {level_atas}, coba cari di level {level_dua_atas}")

                sqlQuery2 = text('''
                    SELECT *
                    FROM tpp_structural
                    WHERE id_unitKerja = :id_unitKerja
                      AND CAST(level AS CHAR) = :level_dua_atas
                ''')

                data2 = db.engine.execute(sqlQuery2, {
                    'id_unitKerja': id_unitKerja,
                    'level_dua_atas': str(level_dua_atas)
                })

                for rowproxy in data2:
                    d = {}
                    for column, value in rowproxy.items():
                        if isinstance(value, datetime):
                            d[column] = value.isoformat()
                        elif isinstance(value, decimal.Decimal):
                            d[column] = float(value)
                        else:
                            d[column] = value
                    a.append(d)

                    # Jika tetap kosong, tampilkan dummy juga
            if not a:
                print("⚠️ Tidak ditemukan atasan di dua level atas, tampilkan data dummy.")
                a = [{
                    "id": None,
                    "id_unitKerja": id_unitKerja,
                    "name": "Tidak ada atasan",
                    "description": None,
                    "level": None,
                    "created_at": None,
                    "updated_at": None
                }]

            print("Jumlah hasil ditemukan:", len(a))

            resp = message(True, generateDefaultResponse(crudTitle, 'get-list', 200))
            resp['data'] = a
            return resp, 200

        elif args.get("struktur") == '3':
            code = args.get("code", "1.34.%")  # default filter
            # SQL utama
            sqlQuery = text(f"""
                            SELECT 
                                u.id,
                                u.parent_id,
                                u.code,
                                u.name,
                                u.depth,
                                u.attributes,
                                u.created_date,
                                u.created_by,
                                u.updated_date,
                                u.updated_by,
                                CASE 
                                    WHEN EXISTS (
                                        SELECT 1 FROM [saba_auth].[dbo].[unit] AS c 
                                        WHERE c.parent_id = u.id
                                    ) THEN CAST(1 AS BIT)
                                    ELSE CAST(0 AS BIT)
                                END AS hasChild
                            FROM [saba_auth].[dbo].[unit] AS u
                            WHERE u.code LIKE :code
                            AND u.id NOT IN (
                                SELECT DISTINCT id_unit FROM tpp_kriteria_cluster
                            )
                            ORDER BY u.depth, u.code
                        """)

            data = db.engine.execute(sqlQuery, {"code": code})
            result = []

            for row in data:
                item = {}
                for column, value in row.items():
                    if isinstance(value, datetime):
                        item[column] = value.isoformat()
                    elif isinstance(value, decimal.Decimal):
                        item[column] = float(value)
                    else:
                        item[column] = value

                # Ubah attributes ke dict
                if item.get("attributes"):
                    try:
                        item["attributes"] = json.loads(item["attributes"])
                    except Exception:
                        item["attributes"] = {}
                else:
                    item["attributes"] = {}

                # pastikan hasChild boolean
                item["hasChild"] = bool(item.get("hasChild", False))
                result.append(item)

            resp = {
                "status": True,
                "message": f"Unit data sent",
                "data": result
            }

            return resp, 200
        else:
            return GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)
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
        #             } for d in employeeDataJson if d.get('Id_tpp_structural') == val.id]
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