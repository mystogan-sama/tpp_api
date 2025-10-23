from flask import current_app
from sqlalchemy import func, and_

from app import db
from . import searchField, uniqueField, sortField, crudTitle, respAndPayloadFields, modelName, filterField
from .doc import doc
from app.utils import GeneralIsExistOnDb, GeneralGetDataAll, GeneralGetDataServerSide, GeneralGetDataById, GeneralAddData, get_model, GeneralUpdateData, \
    GeneralDeleteData, GeneraldeleteMultipleData
from .model import tpp_pagu
from ..tpp_pagu_det.model import tpp_pagu_det

model = tpp_pagu


class Service:
    @staticmethod
    def isExist(data):
        return GeneralIsExistOnDb(uniqueField, model, data)

    @staticmethod
    def getSummary(args):
        try:
            # Ambil parameter dari request args
            id_unit = args.get("id_unit", None)
            asn = args.get("asn", None)

            # Konversi tipe data ke integer bila memungkinkan
            if asn is not None:
                try:
                    asn = int(asn)
                except ValueError:
                    asn = None

            # Mulai bangun query dasar
            select_query = db.session.query(
                tpp_pagu.id_unit,
                func.sum(tpp_pagu_det.kriteria_pagu).label("total_kriteria_pagu")
            ).join(tpp_pagu_det, tpp_pagu.id == tpp_pagu_det.id_pagu)

            # Tambahkan filter opsional
            if id_unit:
                select_query = select_query.filter(tpp_pagu.id_unit == id_unit)
            if asn is not None:
                select_query = select_query.filter(tpp_pagu.asn == asn)

            # Group by untuk menghindari hasil duplicate per unit
            select_query = select_query.group_by(tpp_pagu.id_unit)

            # Eksekusi query
            results = select_query.all()
            total_sum = sum(float(r.total_kriteria_pagu or 0) for r in results)
            # Bentuk response
            total_rupiah = f"Rp. {total_sum:,.0f}".replace(",", ".")

            data = [{
                "title": "Total Pagu",
                "count": total_rupiah
            }]

            # Jika tidak ada hasil, kembalikan total 0
            if not data:
                data.append({
                    "title": f"Total Pagu",
                    "count": "Rp. 0"
                })

            return data

        except Exception as error:
            current_app.logger.error(error)
            return None

    @staticmethod
    def getDataAll(args):
        return GeneralGetDataAll(respAndPayloadFields, model, current_app, args, filterField, sortField)

    @staticmethod
    def getDataServerSide(args):
        return GeneralGetDataServerSide(model, searchField, respAndPayloadFields, sortField, db, current_app, args, filterField)

    @staticmethod
    def getDataById(id):
        return GeneralGetDataById(id, model, current_app)

    @staticmethod
    def addData(data):
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