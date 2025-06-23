import os
import shutil
import subprocess
import sys
import threading

from dotenv import load_dotenv
from sqlalchemy_utils import database_exists, create_database

from app.sso_helper import domain_claims, syncronize_resource
from app.task.bridge import internalApi_byUrl

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from app import create_app, db

app = create_app(os.getenv("FLASK_CONFIG") or "default")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@app.teardown_request
def teardown_request(exception):
    if exception:
        db.session.rollback()
    db.session.remove()


# @app.route('/internal/sync_resource', methods=['POST'])
# def sync_resource():
#     return syncronize_resource()


# @app.before_first_request
# def before_first_request():
#     syncronize_resource()

if __name__ == '__main__':
    # before_run_app()
    app.run(
        # host='192.168.1.40',
        # port='5000',
        # use_reloader=False
    threaded=True)