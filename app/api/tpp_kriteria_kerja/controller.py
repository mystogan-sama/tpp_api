import decimal
import json
import math
import os
import threading
from decimal import Decimal

from sqlalchemy import text
from datetime import datetime

import sqlalchemy
from flask import request, current_app, jsonify, copy_current_request_context
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import create_engine, exc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql.elements import Null
from werkzeug.datastructures import MultiDict

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, generateDefaultResponse, message, \
    error_response, DateTimeEncoder, logger
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .service import Service
from ..tpp_kriteria_cluster.model import tpp_kriteria_cluster
from ..tpp_kriteria_cluster_det.model import tpp_kriteria_cluster_det
from ..tpp_kriteria_kerja_det.model import tpp_kriteria_kerja_det
from ... import internalApi_byUrl, db
from ...sso_helper import token_required, current_user
api = doc.api

parser = reqparse.RequestParser()
parser.add_argument('fetch_child', type=inputs.boolean, help='boolean input for fetch unit children', default=True)

parser.add_argument('sort', type=str, help='for sorting, fill with column name')
parser.add_argument('sort_dir', type=str, choices=('asc', 'desc'), help='fill with "asc" or "desc"')


#### LIST
def row2dictOneData(data):
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

    return a[0]


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
            parser.add_argument(row.split(":")[2] if len(row.split(":")) > 2 else row.split(":")[0])

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

        id_unit = payload['id_unit']

        # 🔍 Ambil ID Kriteria Cluster berdasarkan ID Unit
        kriteria_cluster = db.session.query(tpp_kriteria_cluster).filter_by(id_unit=id_unit).first()
        if not kriteria_cluster:
            return {"status": False, "message": "Kriteria cluster tidak ditemukan"}, 404

        id_kriteria_cluster = kriteria_cluster.id

        # 🔍 Ambil semua detail kriteria dari cluster
        kriteria_cluster_dets = db.session.query(tpp_kriteria_cluster_det).filter_by(
            id_kriteriaCluster=id_kriteria_cluster).all()
        if not kriteria_cluster_dets:
            return {"status": False, "message": "Tidak ada detail kriteria ditemukan"}, 404

        # ✅ Simpan ke tpp_kriteria_kerja (master) terlebih dahulu
        result_post = GeneralPost(doc, crudTitle, Service, request)

        # Pastikan penyimpanan berhasil, dan ambil ID hasil insert
        if not result_post[1] == 200 or not result_post[0].get("data", {}).get("id"):
            return {"status": False, "message": "Gagal menyimpan data kriteria kerja"}, 500

        id_kriteriaKerja = result_post[0]["data"]["id"]

        # 🔁 Simpan semua detail dari cluster ke tpp_kriteria_kerja_det
        for det in kriteria_cluster_dets:
            kerja_det = tpp_kriteria_kerja_det(
                id_kriteriaKerja=id_kriteriaKerja,
                id_kriteria=det.id_kriteria,
                kriteria_name=det.kriteria_name,
                kriteria_formula=det.kriteria_formula
            )
            db.session.add(kerja_det)

        db.session.commit()

        return result_post

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
            resp['data'] = resultData or []
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)

