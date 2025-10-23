from flask_restx import Namespace, fields

from app.utils import generateDefaultDoc
from . import apiName, apiPath, crudTitle, docName, respAndPayloadFields


class doc:
    api = Namespace(apiPath, description=f"{apiName} Related Operations.")

    default_data_response = api.model(
        f"{docName}_object", respAndPayloadFields
    )

    default_delete_multi_payload = api.model(
        f"{docName}_multi_delete_payload",
        {
            'id': fields.List(fields.Integer(), example=[1, 2, 3, 4, 5])
        }
    )

    default_data_summary_response = api.model(
        f"{docName}_summary_object",
        {
            'total': fields.Integer()
        }
    )

    getRespDoc = generateDefaultDoc(api, default_data_response, crudTitle, "get-list-pagination", docName)
    getByIdRespDoc = generateDefaultDoc(api, default_data_response, crudTitle, "get", docName)
    postRespDoc = generateDefaultDoc(api, default_data_response, crudTitle, "post", docName)
    putRespDoc = generateDefaultDoc(api, default_data_response, crudTitle, "put", docName)
    deleteRespDoc = generateDefaultDoc(api, default_data_response, crudTitle, "delete", docName)
    deleteMultiRespDoc = generateDefaultDoc(api, default_delete_multi_payload, crudTitle, "delete-multi", docName)
    getSummaryRespDoc = generateDefaultDoc(api, default_data_summary_response, crudTitle, "get-sum", docName)