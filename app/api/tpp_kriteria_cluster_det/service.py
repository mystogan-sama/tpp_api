from flask import current_app
from sqlalchemy import func

from app import db
from app.utils import GeneralIsExistOnDb, GeneralGetDataAll, GeneralGetDataServerSide, GeneralGetDataById, \
    GeneralAddData, GeneralUpdateData, \
    GeneralDeleteData, GeneraldeleteMultipleData
from . import searchField, uniqueField, sortField, crudTitle, respAndPayloadFields, filterField
from .doc import doc
from .model import tpp_kriteria_cluster_det

model = tpp_kriteria_cluster_det


class Service:
    @staticmethod
    def isExist(data):
        return GeneralIsExistOnDb(uniqueField, model, data)

    @staticmethod
    def getSummary(args):
        try:
            select_query = model.query
            total_data = {
                "title": f"Total {crudTitle}",
                "count": select_query.with_entities(func.count(model.id)).scalar()
            }
            result = [total_data]
            return result
        except Exception as error:
            current_app.logger.error(error)
            return None

    @staticmethod
    def getDataAll(args):
        return GeneralGetDataAll(respAndPayloadFields, model, current_app, args, filterField, sortField)

    @staticmethod
    def getDataServerSide(args):
        return GeneralGetDataServerSide(model, searchField, respAndPayloadFields, sortField, db, current_app, args,
                                        filterField)

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