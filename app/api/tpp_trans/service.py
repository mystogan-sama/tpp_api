from flask import current_app
from sqlalchemy import func

from app import db
from app.utils import GeneralIsExistOnDb, GeneralGetDataAll, GeneralGetDataServerSide, \
    GeneralGetDataById, GeneralAddData, GeneralUpdateData, \
    GeneralDeleteData, GeneraldeleteMultipleData
from . import searchField, uniqueField, sortField, crudTitle, respAndPayloadFields, filterField
from .doc import doc
from .model import tpp_trans
from ...sso_helper import current_user

model = tpp_trans


class Service:
    @staticmethod
    def isExist(data):
        return GeneralIsExistOnDb(uniqueField, model, data)

    @staticmethod
    def getSummary(args):
        try:
            base_query = tpp_trans.query
            unit = current_user.get("member_of_list")
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
                func.sum(tpp_trans.jml_pemangku)
            ).filter(
                tpp_trans.Id_JobLevel.in_([1, 2, 3]),
                tpp_trans.asn == 1).scalar() or 0

            total_fungsional_pns = base_query.with_entities(
                func.sum(tpp_trans.jml_pemangku)
            ).filter(
                tpp_trans.Id_JobLevel == 4,
                tpp_trans.asn == 1).scalar() or 0

            total_pelaksana_pns = base_query.with_entities(
                func.sum(tpp_trans.jml_pemangku)
            ).filter(
                tpp_trans.Id_JobLevel == 5,
                tpp_trans.asn == 1).scalar() or 0


            result = [
                {
                    "title": "Total PNS",
                    "icon": "material:account_circle",
                    "count": f"{total_pns}",
                    "color": "success"
                },
                {
                    "title": "Struktural PNS",
                    "icon": "material:account_circle",
                    "count": f"{total_struktural_pns}",
                    "color": "success"
                },
                {
                    "title": "Fungsional PNS",
                    "icon": "material:account_circle",
                    "count": f"{total_fungsional_pns}",
                    "color": "success"
                },
                {
                    "title": "Pelaksana PNS",
                    "icon": "material:account_circle",
                    "count": f"{total_pelaksana_pns}",
                    "color": "success"
                }

            ]


            return result

        except Exception as error:
            current_app.logger.error(f"Error in getSummary: {str(error)}")
            return {"error": str(error)}

    @staticmethod
    def getSummaryP3K(args):
        try:
            base_query = tpp_trans.query
            unit = current_user.get("member_of_list")
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
            total_p3k = base_query.with_entities(
                func.sum(tpp_trans.jml_pemangku)).filter(tpp_trans.asn == 0
            ).scalar() or 0

            total_struktural_p3k = base_query.with_entities(
                func.sum(tpp_trans.jml_pemangku)
            ).filter(
                tpp_trans.Id_JobLevel.in_([1, 2, 3]),
                tpp_trans.asn == 0).scalar() or 0

            total_fungsional_p3k = base_query.with_entities(
                func.sum(tpp_trans.jml_pemangku)
            ).filter(
                tpp_trans.Id_JobLevel == 4,
                tpp_trans.asn == 0).scalar() or 0

            total_pelaksana_p3k = base_query.with_entities(
                func.sum(tpp_trans.jml_pemangku)
            ).filter(
                tpp_trans.Id_JobLevel == 5,
                tpp_trans.asn == 0).scalar() or 0

            result = [
                {
                    "title": "Total PPPK",
                    "icon": "material:account_circle",
                    "count": f"{total_p3k}",
                },
                {
                    "title": "Struktural PPPK",
                    "icon": "material:account_circle",
                    "count": f"{total_struktural_p3k}",
                },
                {
                    "title": "Fungsional PPPK",
                    "icon": "material:account_circle",
                    "count": f"{total_fungsional_p3k}",
                },
                {
                    "title": "Pelaksana PPPK",
                    "icon": "material:account_circle",
                    "count": f"{total_pelaksana_p3k}",
                }
            ]

            return result

        except Exception as error:
            current_app.logger.error(f"Error in getSummary: {str(error)}")
            return {"error": str(error)}

    @staticmethod
    def getSummaryKriteriaPNS(args):
        try:
            query = tpp_trans.query
            unit = current_user.get("member_of_list")
            current_app.logger.info(f"unit: {unit}")

            # 🔹 Filter unit
            if unit:
                if not isinstance(unit, list):
                    unit = [unit]

                first_unit = str(unit[0])
                current_app.logger.info(f"first_unit: {first_unit}")

                if first_unit not in ["4010003246677", "1"]:
                    query = query.filter(tpp_trans.id_unit == first_unit)
                    current_app.logger.info(f"Menghitung hanya untuk unit: {first_unit}")
                else:
                    current_app.logger.info("Super admin → hitung semua unit")
            else:
                current_app.logger.warning("member_of_list kosong atau tidak valid")

            # 🔹 Semua perhitungan dilakukan per-row lalu dijumlah (filter ASN=0 → PPPK)
            filter_asn = query.filter(tpp_trans.asn == 1)

            total_beban = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.beban_kerja_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_prestasi = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.prestasi_kerja_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_kondisi = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.kondisi_kerja_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_tempat = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.tempat_bekerja_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_kelangkaan = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.kelangkaan_profesi_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_pol = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.pertimbangan_objektif_lainnya_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            # ✅ Jumlahkan totalnya di Python (bukan SQL)
            total_kriteria_pns = (
                    total_beban
                    + total_prestasi
                    + total_kondisi
                    + total_tempat
                    + total_kelangkaan
                    + total_pol
            )

            # 🔹 Format rupiah
            def to_rupiah(value):
                return f"Rp. {float(value):,.0f}".replace(",", ".")

            result = [
                {"title": "Total PNS", "icon": "material:payments", "count": to_rupiah(total_kriteria_pns), "color": "success"},
                {"title": "Beban Kerja PNS", "icon": "material:payments", "count": to_rupiah(total_beban), "color": "success"},
                {"title": "Prestasi Kerja PNS", "icon": "material:payments", "count": to_rupiah(total_prestasi), "color": "success"},
                {"title": "Kondisi Kerja PNS", "icon": "material:payments", "count": to_rupiah(total_kondisi), "color": "success"},
                # {"title": "Tempat Kerja PPPK", "count": to_rupiah(total_tempat)},
                # {"title": "Kelangkaan Profesi PPPK", "count": to_rupiah(total_kelangkaan)},
                # {"title": "Pertimbangan Objektif Lainnya PPPK", "count": to_rupiah(total_pol)},
            ]

            return result

        except Exception as error:
            current_app.logger.error(f"Error in getSummaryKriteriaPNS: {error}")
            return None

    @staticmethod
    def getSummaryKriteriaP3K(args):
        try:
            query = tpp_trans.query
            unit = current_user.get("member_of_list")
            current_app.logger.info(f"unit: {unit}")

            # 🔹 Filter unit
            if unit:
                if not isinstance(unit, list):
                    unit = [unit]

                first_unit = str(unit[0])
                current_app.logger.info(f"first_unit: {first_unit}")

                if first_unit not in ["4010003246677", "1"]:
                    query = query.filter(tpp_trans.id_unit == first_unit)
                    current_app.logger.info(f"Menghitung hanya untuk unit: {first_unit}")
                else:
                    current_app.logger.info("Super admin → hitung semua unit")
            else:
                current_app.logger.warning("member_of_list kosong atau tidak valid")

            # 🔹 Semua perhitungan dilakukan per-row lalu dijumlah (filter ASN=0 → PPPK)
            filter_asn = query.filter(tpp_trans.asn == 0)

            total_beban = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.beban_kerja_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_prestasi = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.prestasi_kerja_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_kondisi = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.kondisi_kerja_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_tempat = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.tempat_bekerja_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_kelangkaan = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.kelangkaan_profesi_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            total_pol = (
                    filter_asn.with_entities(
                        func.sum(
                            func.coalesce(tpp_trans.pertimbangan_objektif_lainnya_rp, 0)
                            * func.coalesce(tpp_trans.jml_pemangku, 0)
                            * func.coalesce(tpp_trans.bulan, 0)
                        )
                    ).scalar() or 0
            )

            # ✅ Jumlahkan totalnya di Python (bukan SQL)
            total_kriteria_p3k = (
                    total_beban
                    + total_prestasi
                    + total_kondisi
                    + total_tempat
                    + total_kelangkaan
                    + total_pol
            )

            # 🔹 Format rupiah
            def to_rupiah(value):
                return f"Rp. {float(value):,.0f}".replace(",", ".")

            result = [
                {"title": "Total PPPK", "icon": "material:payments", "count": to_rupiah(total_kriteria_p3k)},
                {"title": "Beban Kerja PPPK", "icon": "material:payments", "count": to_rupiah(total_beban)},
                {"title": "Prestasi Kerja PPPK", "icon": "material:payments", "count": to_rupiah(total_prestasi)},
                {"title": "Kondisi Kerja PPPK", "icon": "material:payments", "count": to_rupiah(total_kondisi)},
                # {"title": "Tempat Kerja PPPK", "count": to_rupiah(total_tempat)},
                # {"title": "Kelangkaan Profesi PPPK", "count": to_rupiah(total_kelangkaan)},
                # {"title": "Pertimbangan Objektif Lainnya PPPK", "count": to_rupiah(total_pol)},
            ]

            return result

        except Exception as error:
            current_app.logger.error(f"Error in getSummaryKriteriaP3K: {error}")
            return None

    @staticmethod
    def getDataAll(args):
        return GeneralGetDataAll(respAndPayloadFields, model, current_app, args, filterField)

    @staticmethod
    def getDataById(id):
        return GeneralGetDataById(id, model, current_app)

    @staticmethod
    def addData(data):
        # if 'parent_id' not in data:
        #     data['parent_id'] = None
        #
        # if 'code' not in data:
        #     # parent_siblings_data = model.query.filter(
        #     #     or_(model.id == data['parent_id'], model.parent_id == data['parent_id'])).order_by(model.code).all()
        #     parent_siblings_data = model.query.filter(model.parent_id == data['parent_id']).order_by(model.code).all()
        #     if parent_siblings_data:
        #         parent_siblings_codes = []
        #         for row in parent_siblings_data:
        #             rowCode = row.code.strip()
        #             parent_siblings_codes.append(rowCode)
        #             # rowCodeNumOnlyArr = re.findall(r'[0-9]+', rowCode)
        #             # rowCodeNumOnlyStr = ''.join(rowCodeNumOnlyArr)
        #             # parent_siblings_codes.append(rowCodeNumOnlyStr)
        #
        #         parent_siblings_codes.sort()
        #         max_parent_siblings_code = parent_siblings_codes[-1]
        #         if max_parent_siblings_code.endswith('.'):
        #             max_parent_siblings_code = max_parent_siblings_code[:-len('.')]
        #         max_parent_siblings_codes_arr = max_parent_siblings_code.split('.')
        #         prefixCodeArr = [*max_parent_siblings_codes_arr]
        #         prefixCodeArr.pop()
        #         prefixCode = '.'.join(prefixCodeArr)
        #
        #         nextCode = prefixCode + '.' + str((int(max_parent_siblings_codes_arr[-1]) + 1)).zfill(2) + '.'
        #         print(max_parent_siblings_codes_arr)
        #         data['code'] = nextCode

        return GeneralAddData(data, db, model, current_app)

    @staticmethod
    def updateData(id, data):
        return GeneralUpdateData(id, data, model, db, current_app)

    @staticmethod
    def deleteData(id):
        return GeneralDeleteData(id, model, db, current_app, doc)

    @staticmethod
    def deleteMultipleData(ids):
        return GeneraldeleteMultipleData(ids, model, db, current_app, doc)