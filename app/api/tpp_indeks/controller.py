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
from ... import internalApi_byUrl, db
from ...sso_helper import token_required, current_user
api = doc.api

parser = reqparse.RequestParser()
parser.add_argument('fetch_child', type=inputs.boolean, help='boolean input for fetch unit children', default=True)

parser.add_argument('sort', type=str, help='for sorting, fill with column name')
parser.add_argument('sort_dir', type=str, choices=('asc', 'desc'), help='fill with "asc" or "desc"')
parser.add_argument('tahun', type=int, help='Filter by tahun', default=None)


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
        args = parser.parse_args()

        # Paksa tahun masuk ke args
        args['tahun'] = current_user['data_year']

        # Paksa parser agar 'tahun' terlihat di payload (args) untuk GeneralGetList
        for action in parser.args:
            if action.name == 'tahun':
                action.default = current_user['data_year']

        return GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)



    #### POST SINGLE/MULTIPLE
    @doc.postRespDoc
    # @api.expect(doc.default_data_response, validate=True)
    @token_required
    def post(self):
        payload = request.get_json()

        # Konversi aman ke float
        hasil_iid = float(payload.get("hasil_iid", 0))
        hasil_rbpd = float(payload.get("hasil_rbpd", 0))
        hasil_ipm = float(payload.get("hasil_ipm", 0))
        hasil_igr = float(payload.get("hasil_igr", 0))

        # nilai_iid
        if hasil_iid == 0:
            payload["nilai_iid"] = 0
        elif 0 < hasil_iid <= 34.99:
            payload["nilai_iid"] = 500
        elif 35.00 <= hasil_iid <= 60.00:
            payload["nilai_iid"] = 800
        elif 60.01 <= hasil_iid <= 100:
            payload["nilai_iid"] = 1000
        else:
            payload["nilai_iid"] = 0

        # nilai_rbpd
        if hasil_rbpd >= 8:
            payload["nilai_rbpd"] = 200
        elif hasil_rbpd > 6.00:
            payload["nilai_rbpd"] = 400
        elif hasil_rbpd > 4.00:
            payload["nilai_rbpd"] = 600
        elif hasil_rbpd >= 2.00:
            payload["nilai_rbpd"] = 800
        elif hasil_rbpd < 2.00:
            payload["nilai_rbpd"] = 1000
        else:
            payload["nilai_rbpd"] = 0

        # nilai_ipm
        if hasil_ipm <= 60:
            payload["nilai_ipm"] = 250
        elif hasil_ipm <= 69:
            payload["nilai_ipm"] = 500
        elif hasil_ipm <= 79:
            payload["nilai_ipm"] = 750
        elif hasil_ipm >= 80:
            payload["nilai_ipm"] = 1000
        else:
            payload["nilai_ipm"] = 0

        # nilai_igr
        if hasil_igr >= 0.5:
            payload["nilai_igr"] = 350
        elif hasil_igr >= 0.36:
            payload["nilai_igr"] = 700
        elif hasil_igr < 0.36:
            payload["nilai_igr"] = 1000
        else:
            payload["nilai_igr"] = 0

        # Hitung total_skor
        total_skor = (
                float(payload.get("olk", 0)) * 0.30 +
                float(payload.get("lppd", 0)) * 0.25 +
                float(payload.get("kppd", 0)) * 0.10 +
                float(payload.get("nilai_iid", 0)) * 0.03 +
                float(payload.get("pkpd", 0)) * 0.18 +
                float(payload.get("nilai_rbpd", 0)) * 0.02 +
                float(payload.get("irbpd", 0)) * 0.02 +
                float(payload.get("nilai_ipm", 0)) * 0.06 +
                float(payload.get("nilai_igr", 0)) * 0.04
        )
        payload["total_skor"] = round(total_skor, 2)

        # Nilai IPPD berdasarkan total_skor
        if total_skor <= 501:
            payload["nilai_ippd"] = 0.6
        elif total_skor <= 601:
            payload["nilai_ippd"] = 0.7
        elif total_skor <= 701:
            payload["nilai_ippd"] = 0.8
        elif total_skor <= 800:
            payload["nilai_ippd"] = 0.9
        else:
            payload["nilai_ippd"] = 1.0

        # Hitung indeks_tpp
        kelas_jab = float(payload.get("kelas_jab", 0))
        ikf = float(payload.get("ikf", 0))
        ikk = float(payload.get("ikk", 0))
        nilai_ippd = float(payload.get("nilai_ippd", 0))

        indeks_tpp = kelas_jab * ikf * ikk * nilai_ippd
        payload["indeks_tpp"] = round(indeks_tpp, 9)

        print(kelas_jab)
        print(ikf)
        print(ikk)
        print(nilai_ippd)
        print(indeks_tpp)

        # Kirim ke Service
        # return GeneralPost(doc, crudTitle, Service, payload)
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

