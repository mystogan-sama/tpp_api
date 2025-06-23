import os
from flask import Blueprint
from flask_restx import Api

internal_bp = Blueprint("internal", __name__)

authorizations = {
            'apikey': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Apikey',
                'description': "Type in the *'Value'* input box below: **'&lt;apikey&gt;'**"
            }
        }

internal = Api(internal_bp,
               title=f'{os.environ.get("APPNAME")} Internal API',
               description="For Internal routes.")
