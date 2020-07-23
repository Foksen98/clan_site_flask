from configparser import ConfigParser
import os

CONFIG_PATH = 'config/config.ini'


def get_config_parser():
	config = ConfigParser()
	config.read(CONFIG_PATH)

	return config


def get_server_secret_key():
	return get_config_parser().get('server', 'secret_key')


def get_db_name():
	return get_config_parser().get('db', 'name')


def get_db_host():
	return get_config_parser().get('db', 'host')


def get_db_port():
	return int(get_config_parser().get('db', 'port'))


def get_wg_app_name():
	return get_config_parser().get('wg_app', 'name')


def get_wg_app_id():
	return get_config_parser().get('wg_app', 'id')

def get_wg_app_redirect_uri():
	return get_config_parser().get('wg_app', 'redirect_uri')


def get_clan_id():
	return get_config_parser().get('clan', 'id')
