import decimal
import json
import os
from datetime import datetime

import requests
from flask import request, render_template, Response, current_app, jsonify
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import text, func

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, message, generateDefaultResponse, \
    row2dict_same_api_res, genRecrusive, logger, error_response
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .service import Service
from ..tpp_pagu.model import tpp_pagu
from ..tpp_pagu_det.model import tpp_pagu_det
from ..tpp_realisasi.model import tpp_realisasi
from ..tpp_realisasi_det.model import tpp_realisasi_det
from ..tpp_trans.model import tpp_trans
from ... import internalApi_byUrl, db
from ...sso_helper import token_required, current_user

api = doc.api

parser = reqparse.RequestParser()
parser.add_argument('fetch_child', type=inputs.boolean, help='boolean input for fetch unit children', default=True)

parser.add_argument('sort', type=str, help='for sorting, fill with column name')
parser.add_argument('sort_dir', type=str, choices=('asc', 'desc'), help='fill with "asc" or "desc"')


def checkToken(request):
    url = f'{os.environ.get("SSO_URL")}token_verify'
    logger.debug(f'Verify token to sso : {url} begin ....')

    # =========================
    # AMBIL AUTH (HEADER > QUERY)
    # =========================
    authorization = (
            request.headers.get('Authorization')
            or request.args.get('Authorization')
    )

    if not authorization:
        return jsonify({'msg': 'Missing Authorization Header'}), 401

    if not authorization.startswith('Bearer '):
        return jsonify({
            'msg': 'Authorization Header is invalid. Use: Bearer {access_token}'
        }), 401

    try:
        headers = {"Authorization": authorization}
        jsonPayload = {
            'x_endpoint': request.path,
            'x_method': request.method
        }

        req = requests.post(url, headers=headers, json=jsonPayload)

        if req.status_code != 200:
            logger.error(f'SSO VERIFY FAILED {req.status_code} {req.text}')
            return jsonify(req.json()), req.status_code

        user_data = req.json()
        user_data['access_token'] = authorization
        user_data['origin'] = request.host_url

        logger.debug('Verify token success')
        return user_data

    except Exception as e:
        logger.exception('SSO VERIFY ERROR')
        return jsonify({
            'msg': 'Authorization verification failed',
            'error': str(e)
        }), 500

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
    # @token_required
    def get(self):
        auth_result = checkToken(request)

        # kalau Response → langsung return (error)
        if isinstance(auth_result, Response):
            return auth_result

        userData = auth_result  # sudah dict
        print("USER DATA", userData)
        if not userData:
            return error_response('Not Authorized', 403)
        args = parser.parse_args()
        unit_filter = args.get('unit') or ''
        print("Filter", unit_filter)

        # unit_filter = userData.get("member_of_list", [])

        if args["dashboard"] == '1':
            html = render_template("index.html", auth_qs=request.args.get('Authorization', ''), host_url=request.host_url)
            return Response(html, mimetype="text/html")

        elif args.get("dashboard") == '2':
            try:
                base_query = tpp_trans.query
                unit = userData.get("member_of_list", [])
                current_app.logger.info(f"unit: {unit}")

                if unit:
                    # pastikan unit adalah list
                    if not isinstance(unit, list):
                        unit = [unit]

                    first_unit = str(unit[0])
                    current_app.logger.info(f"first_unit: {first_unit}")

                    # Jika unit pertama adalah 4010003246677 atau 1 → hitung semua unit
                    if first_unit in ["4010003246677", "1"]:
                        current_app.logger.info("first_unit adalah 4010003246677 atau 1 → menghitung semua unit")
                    else:
                        base_query = base_query.filter(tpp_trans.id_unit == first_unit)
                        # print(base_query)
                        current_app.logger.info(f"Menghitung hanya untuk unit: {unit}")
                else:
                    current_app.logger.warning("member_of_list kosong atau tidak valid")

                # Hitung total pemangku
                total_pns = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)).filter(tpp_trans.asn == 1
                                                             ).scalar() or 0

                total_struktural_pns = base_query.with_entities(
                    func.sum(tpp_trans.total_tahun)
                ).filter(
                    tpp_trans.Id_JobLevel.in_([1, 2, 3]),
                    tpp_trans.asn == 1).scalar() or 0

                total_fungsional_pns = base_query.with_entities(
                    func.sum(tpp_trans.total_tahun)
                ).filter(
                    tpp_trans.Id_JobLevel == 4,
                    tpp_trans.asn == 1).scalar() or 0

                total_fungsional_pppk = base_query.with_entities(
                    func.sum(tpp_trans.total_tahun)
                ).filter(
                    tpp_trans.Id_JobLevel == 4,
                    tpp_trans.asn == 0).scalar() or 0

                total_pelaksana_pns = base_query.with_entities(
                    func.sum(tpp_trans.total_tahun)
                ).filter(
                    tpp_trans.Id_JobLevel == 5,
                    tpp_trans.asn == 1).scalar() or 0

                total_pelaksana_pppk = base_query.with_entities(
                    func.sum(tpp_trans.total_tahun)
                ).filter(
                    tpp_trans.Id_JobLevel == 5,
                    tpp_trans.asn == 0).scalar() or 0

                total_guru_pns = base_query.with_entities(
                    func.sum(tpp_trans.total_tahun)
                ).filter(
                    tpp_trans.id_jabatan.in_([232, 233, 234, 235]),
                    tpp_trans.asn == 1).scalar() or 0

                total_guru_pppk = base_query.with_entities(
                    func.sum(tpp_trans.total_tahun)
                ).filter(
                    tpp_trans.id_jabatan.in_([232, 233, 234, 235]),
                    tpp_trans.asn == 0).scalar() or 0

                def to_rupiah(value):
                    return f"Rp. {float(value):,.0f}".replace(",", ".")

                result = [
                    {
                        "title": "Struktural PNS",
                        "icon": "material:account_circle",
                        "count": to_rupiah(total_struktural_pns),
                        "color": "success"
                    },
                    {
                        "title": "Fungsional PNS",
                        "icon": "material:account_circle",
                        "count": to_rupiah(total_fungsional_pns),
                        "color": "success"
                    },
                    {
                        "title": "Fungsional PPPK",
                        "icon": "material:account_circle",
                        "count": to_rupiah(total_fungsional_pppk),
                        "color": "success"
                    },
                    {
                        "title": "Pelaksana PNS",
                        "icon": "material:account_circle",
                        "count": to_rupiah(total_pelaksana_pns),
                        "color": "success"
                    },
                    {
                        "title": "Pelaksana PPPK",
                        "icon": "material:account_circle",
                        "count": to_rupiah(total_pelaksana_pppk),
                        "color": "success"
                    },
                    {
                        "title": "Guru PNS",
                        "icon": "material:account_circle",
                        "count": to_rupiah(total_guru_pns),
                        "color": "success"
                    },
                    {
                        "title": "Guru PPPK",
                        "icon": "material:account_circle",
                        "count": to_rupiah(total_guru_pppk),
                        "color": "success"
                    }
                ]

                return result
                # print(result)

            except Exception as error:
                current_app.logger.error(f"Error in getSummary: {str(error)}")
                return {"error": str(error)}

        elif args.get("dashboard") == '3':
            try:
                base_query = tpp_trans.query
                unit = userData.get("member_of_list", [])
                # print(unit)
                current_app.logger.info(f"unit: {unit}")
                # print(unit)

                # ===============================
                # FILTER UNIT (PEMDA / UNIT)
                # ===============================
                if unit:
                    if not isinstance(unit, list):
                        unit = [unit]

                    first_unit = str(unit[0])

                    # 4010003246677 / 1 = PEMDA (all unit)
                    if first_unit not in ["4010003246677", "1"]:
                        base_query = base_query.filter(tpp_trans.id_unit == first_unit)

                # ===============================
                # QUERY INTI (PNS + PPPK)
                # ===============================
                rows = (
                    base_query
                    .with_entities(
                        tpp_trans.id_kelas,
                        tpp_trans.asn,
                        func.sum(tpp_trans.total_tahun).label("total_tahun")
                    )
                    .filter(tpp_trans.id_kelas.between(1, 15))
                    .group_by(tpp_trans.id_kelas, tpp_trans.asn)
                    .order_by(tpp_trans.id_kelas)
                    .all()
                )

                # ===============================
                # FORMAT RESPONSE
                # ===============================
                result = []
                for row in rows:
                    result.append({
                        "id_kelas": row.id_kelas,
                        "asn": row.asn,  # 1 = PNS, 0 = PPPK
                        "jenis_asn": "PNS" if row.asn == 1 else "PPPK",
                        "total_tahun": float(row.total_tahun or 0)
                    })

                return {
                    "struktur": 3,
                    "data": result
                }

            except Exception as error:
                current_app.logger.error(f"Error struktur=3: {str(error)}")
                return {"error": str(error)}

        elif args.get("dashboard") == '4':
            try:
                tahun = userData.get("data_year")
                unit = userData.get("member_of_list", [])

                # ===============================
                # FILTER UNIT
                # ===============================
                unit_filter = None
                if unit:
                    if not isinstance(unit, list):
                        unit = [unit]
                    first_unit = int(unit[0])
                    if first_unit not in [1, 4010003246677]:
                        unit_filter = first_unit

                # ===============================
                # AMBIL TOTAL PAGU
                # ===============================
                def get_total_pagu(asn):
                    q = (
                        db.session.query(
                            func.coalesce(func.sum(tpp_pagu_det.kriteria_pagu), 0)
                        )
                        .join(tpp_pagu, tpp_pagu.id == tpp_pagu_det.id_pagu)
                        .filter(
                            tpp_pagu.asn == asn,
                            tpp_pagu.tahun == tahun
                        )
                    )

                    if unit_filter:
                        q = q.filter(tpp_pagu.id_unit == unit_filter)

                    return float(q.scalar() or 0)

                total_pagu_pns = get_total_pagu(1)
                total_pagu_pppk = get_total_pagu(0)

                # ===============================
                # AMBIL REALISASI BULANAN
                # ===============================
                def get_serapan(asn, total_pagu):
                    q = (
                        db.session.query(
                            tpp_realisasi.bulan,
                            func.coalesce(
                                func.sum(tpp_realisasi_det.kriteria_realisasi), 0
                            ).label("nilai")
                        )
                        .join(
                            tpp_realisasi_det,
                            tpp_realisasi.id == tpp_realisasi_det.id_realisasi
                        )
                        .filter(
                            tpp_realisasi.asn == asn,
                            tpp_realisasi.tahun == tahun
                        )
                    )

                    if unit_filter:
                        q = q.filter(tpp_realisasi.id_unit == unit_filter)

                    q = (
                        q.group_by(tpp_realisasi.bulan)
                        .order_by(tpp_realisasi.bulan)
                        .all()
                    )

                    # ===============================
                    # HITUNG KUMULATIF + SERAPAN
                    # ===============================
                    hasil = []
                    kumulatif = 0.0

                    for row in q:
                        nilai_bulan = float(row.nilai)
                        kumulatif += nilai_bulan

                        persen = (
                            (kumulatif / total_pagu) * 100
                            if total_pagu > 0 else 0
                        )

                        hasil.append({
                            "bulan": int(row.bulan),
                            "realisasi_bulan": nilai_bulan,
                            "realisasi_kumulatif": kumulatif,
                            "serapan_persen": round(persen, 2)
                        })

                    return hasil

                serapan_pns = get_serapan(1, total_pagu_pns)
                serapan_pppk = get_serapan(0, total_pagu_pppk)

                # ===============================
                # RESPONSE FINAL (SIAP DASHBOARD)
                # ===============================
                return {
                    "tahun": tahun,
                    "unit": unit_filter or "SEMUA UNIT",
                    "pagu": {
                        "pns": total_pagu_pns,
                        "pppk": total_pagu_pppk
                    },
                    "serapan": {
                        "pns": serapan_pns,
                        "pppk": serapan_pppk
                    }
                }

            except Exception as e:
                current_app.logger.error(f"Dashboard serapan error: {str(e)}")
                return {"error": str(e)}, 500

        elif args.get("dashboard") == '5':
            try:
                base_query = tpp_trans.query
                unit = userData.get("member_of_list", [])
                current_app.logger.info(f"unit: {unit}")

                if unit:
                    # pastikan unit adalah list
                    if not isinstance(unit, list):
                        unit = [unit]

                    first_unit = str(unit[0])
                    current_app.logger.info(f"first_unit: {first_unit}")

                    # Jika unit pertama adalah 4010003246677 atau 1 → hitung semua unit
                    if first_unit in ["4010003246677", "1"]:
                        current_app.logger.info("first_unit adalah 4010003246677 atau 1 → menghitung semua unit")
                    else:
                        base_query = base_query.filter(tpp_trans.id_unit == first_unit)
                        # print(base_query)
                        current_app.logger.info(f"Menghitung hanya untuk unit: {unit}")
                else:
                    current_app.logger.warning("member_of_list kosong atau tidak valid")

                filter_pns = base_query.filter(tpp_trans.asn == 1)
                filter_pppk = base_query.filter(tpp_trans.asn == 0)

                total_pns = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)).filter(tpp_trans.asn == 1
                                                             ).scalar() or 0

                total_p3k = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)).filter(tpp_trans.asn == 0
                                                             ).scalar() or 0

                total_struktural_pns = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)
                ).filter(
                    tpp_trans.Id_JobLevel.in_([1, 2, 3]),
                    tpp_trans.asn == 1).scalar() or 0

                total_struktural_p3k = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)
                ).filter(
                    tpp_trans.Id_JobLevel.in_([1, 2, 3]),
                    tpp_trans.asn == 0).scalar() or 0

                total_fungsional_pns = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)
                ).filter(
                    tpp_trans.Id_JobLevel == 4,
                    tpp_trans.asn == 1).scalar() or 0

                total_fungsional_p3k = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)
                ).filter(
                    tpp_trans.Id_JobLevel == 4,
                    tpp_trans.asn == 0).scalar() or 0

                total_pelaksana_pns = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)
                ).filter(
                    tpp_trans.Id_JobLevel == 5,
                    tpp_trans.asn == 1).scalar() or 0

                total_pelaksana_p3k = base_query.with_entities(
                    func.sum(tpp_trans.jml_pemangku)
                ).filter(
                    tpp_trans.Id_JobLevel == 5,
                    tpp_trans.asn == 0).scalar() or 0

                total_beban_pns = (
                        filter_pns.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.beban_kerja_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_beban_pppk = (
                        filter_pppk.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.beban_kerja_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_prestasi_pns = (
                        filter_pns.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.prestasi_kerja_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_prestasi_pppk = (
                        filter_pppk.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.prestasi_kerja_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_kondisi_pns = (
                        filter_pns.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.kondisi_kerja_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_kondisi_pppk = (
                        filter_pppk.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.kondisi_kerja_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_tempat_pns = (
                        filter_pns.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.tempat_bekerja_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_tempat_pppk = (
                        filter_pppk.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.tempat_bekerja_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_kelangkaan_pns = (
                        filter_pns.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.kelangkaan_profesi_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_kelangkaan_pppk = (
                        filter_pppk.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.kelangkaan_profesi_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_pol_pppk = (
                        filter_pppk.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.pertimbangan_objektif_lainnya_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                total_pol_pns = (
                        filter_pns.with_entities(
                            func.sum(
                                func.coalesce(tpp_trans.pertimbangan_objektif_lainnya_rp, 0)
                                * func.coalesce(tpp_trans.jml_pemangku, 0)
                                * func.coalesce(tpp_trans.bulan, 0)
                            )
                        ).scalar() or 0
                )

                # ✅ Jumlahkan totalnya di Python (bukan SQL)
                total_kriteria_pns = (
                        total_beban_pns
                        + total_prestasi_pns
                        + total_kondisi_pns
                        + total_tempat_pns
                        + total_kelangkaan_pns
                        + total_pol_pns
                )

                total_kriteria_p3k = (
                        total_beban_pppk
                        + total_prestasi_pppk
                        + total_kondisi_pppk
                        + total_tempat_pppk
                        + total_kelangkaan_pppk
                        + total_pol_pppk
                )


                def to_rupiah(value):
                    return f"Rp. {float(value):,.0f}".replace(",", ".")

                result = [
                    {
                        "title": "Total PNS",
                        "icon": "material:account_circle",
                        "count": f"{total_pns}",
                        "color": "success"
                    },
                    {
                        "title": "Total PPPK",
                        "icon": "material:account_circle",
                        "count": f"{total_p3k}",
                    },
                    {
                        "title": "Struktural PNS",
                        "icon": "material:account_circle",
                        "count": f"{total_struktural_pns}",
                        "color": "success"
                    },
                    {
                        "title": "Struktural PPPK",
                        "icon": "material:account_circle",
                        "count": f"{total_struktural_p3k}",
                    },
                    {
                        "title": "Fungsional PNS",
                        "icon": "material:account_circle",
                        "count": f"{total_fungsional_pns}",
                        "color": "success"
                    },
                    {
                        "title": "Fungsional PPPK",
                        "icon": "material:account_circle",
                        "count": f"{total_fungsional_p3k}",
                    },
                    {
                        "title": "Pelaksana PNS",
                        "icon": "material:account_circle",
                        "count": f"{total_pelaksana_pns}",
                        "color": "success"
                    },
                    {
                        "title": "Pelaksana PPPK",
                        "icon": "material:account_circle",
                        "count": f"{total_pelaksana_p3k}",
                    },
                    {"title": "Total PNS", "icon": "material:payments", "count": to_rupiah(total_kriteria_pns),
                     "color": "success"},
                    {"title": "Beban Kerja PNS", "icon": "material:payments", "count": to_rupiah(total_beban_pns),
                     "color": "success"},
                    {"title": "Prestasi Kerja PNS", "icon": "material:payments", "count": to_rupiah(total_prestasi_pns),
                     "color": "success"},
                    {"title": "Kondisi Kerja PNS", "icon": "material:payments", "count": to_rupiah(total_kondisi_pns),
                     "color": "success"},
                    {"title": "Tempat Kerja PPPK", "count": to_rupiah(total_tempat_pns)},
                    {"title": "Kelangkaan Profesi PPPK", "count": to_rupiah(total_kelangkaan_pns)},
                    {"title": "Pertimbangan Objektif Lainnya PPPK", "count": to_rupiah(total_pol_pns)},
                    {"title": "Total PPPK", "icon": "material:payments", "count": to_rupiah(total_kriteria_p3k)},
                    {"title": "Beban Kerja PPPK", "icon": "material:payments", "count": to_rupiah(total_beban_pppk)},
                    {"title": "Prestasi Kerja PPPK", "icon": "material:payments", "count": to_rupiah(total_prestasi_pppk)},
                    {"title": "Kondisi Kerja PPPK", "icon": "material:payments", "count": to_rupiah(total_kondisi_pppk)},
                    {"title": "Tempat Kerja PPPK", "count": to_rupiah(total_tempat_pppk)},
                    {"title": "Kelangkaan Profesi PPPK", "count": to_rupiah(total_kelangkaan_pppk)},
                    {"title": "Pertimbangan Objektif Lainnya PPPK", "count": to_rupiah(total_pol_pppk)},
                ]

                return result
                # print(result)

            except Exception as error:
                current_app.logger.error(f"Error in getSummary: {str(error)}")
                return {"error": str(error)}

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