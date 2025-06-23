import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "ngacakW4duK"
    DEBUG = True
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:rb1234!@auth.insaba.co.id,61434/tpp?driver=SQL+Server"
    SQLALCHEMY_BINDS = os.environ.get('DB_CONNECTIONS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_OPERATION_ID = True


class DevelopmentConfig(Config):
    SECRET_KEY = "ngacakW4duK"
    DEBUG = True
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:rb1234!@auth.insaba.co.id,61434/tpp?driver=SQL+Server"
    SQLALCHEMY_BINDS = os.environ.get('DB_CONNECTIONS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_OPERATION_ID = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SECRET_KEY = "ngacakW4duK"
    DEBUG = True
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:rb1234!@auth.insaba.co.id,61434/tpp?driver=SQL+Server"
    SQLALCHEMY_BINDS = os.environ.get('DB_CONNECTIONS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_OPERATION_ID = True


config_by_name = dict(
    development=DevelopmentConfig,
    testing=TestingConfig,
    production=ProductionConfig,
    default=DevelopmentConfig,
)