import os
import config.config_reader as cr

BASEDIR = os.path.abspath(os.path.dirname(__file__))
APP_NAME = "app"


class Config(object):
	UPLOAD_FOLDER = os.path.join(BASEDIR, APP_NAME, 'static/')
	CSRF_ENABLED = True
	SECRET_KEY = cr.get_server_secret_key()
	MONGODB_DB = cr.get_db_name()
	MONGODB_HOST = cr.get_db_host()
	MONGODB_PORT = cr.get_db_port()


class DevConfig(Config):
	DEBUG = True


class ProdConfig(Config):
	DEBUG = False
