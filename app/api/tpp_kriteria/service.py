from flask import current_app
from sqlalchemy import func

from app import db
from app.utils import GeneralIsExistOnDb, GeneralGetDataAll, GeneralGetDataServerSide, \
    GeneralGetDataById, GeneralAddData, GeneralUpdateData, \
    GeneralDeleteData, GeneraldeleteMultipleData
from . import searchField, uniqueField, sortField, crudTitle, respAndPayloadFields, filterField
from .doc import doc
from .model import tpp_kriteria

model = tpp_kriteria


class Service:
    @staticmethod
    def isExist(data):
        return GeneralIsExistOnDb(uniqueField, model, data)

    @staticmethod
    def getDataAll(args):
        return GeneralGetDataAll(respAndPayloadFields, model, current_app, args, filterField)

    @staticmethod
    def getDataById(id):
        return GeneralGetDataById(id, model, current_app)

    @staticmethod
    def addData(data):
        if 'parent_id' not in data:
            data['parent_id'] = None

        if 'code' not in data:
            # parent_siblings_data = model.query.filter(
            #     or_(model.id == data['parent_id'], model.parent_id == data['parent_id'])).order_by(model.code).all()
            parent_siblings_data = model.query.filter(model.parent_id == data['parent_id']).order_by(model.code).all()
            if parent_siblings_data:
                parent_siblings_codes = []
                for row in parent_siblings_data:
                    rowCode = row.code.strip()
                    parent_siblings_codes.append(rowCode)
                    # rowCodeNumOnlyArr = re.findall(r'[0-9]+', rowCode)
                    # rowCodeNumOnlyStr = ''.join(rowCodeNumOnlyArr)
                    # parent_siblings_codes.append(rowCodeNumOnlyStr)

                parent_siblings_codes.sort()
                max_parent_siblings_code = parent_siblings_codes[-1]
                if max_parent_siblings_code.endswith('.'):
                    max_parent_siblings_code = max_parent_siblings_code[:-len('.')]
                max_parent_siblings_codes_arr = max_parent_siblings_code.split('.')
                prefixCodeArr = [*max_parent_siblings_codes_arr]
                prefixCodeArr.pop()
                prefixCode = '.'.join(prefixCodeArr)

                nextCode = prefixCode + '.' + str((int(max_parent_siblings_codes_arr[-1]) + 1)).zfill(2) + '.'
                print(max_parent_siblings_codes_arr)
                data['code'] = nextCode

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