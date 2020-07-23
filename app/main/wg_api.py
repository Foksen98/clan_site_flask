import config.config_reader as cr
import requests


OPENID_URL = 'https://api.worldoftanks.ru/wot/auth/login/?application_id={}&redirect_uri={}'


class WG_API:

	def __init__(self):
		self.__application_id = cr.get_wg_app_id()
		self.__redirect_uri = cr.get_wg_app_redirect_uri()

	def __fetch_object(self, obj_class, obj_id):
		url = 'https://stepik.org/api/{}s/{}'.format(obj_class, obj_id)
		response = requests.get(
			url,
			headers={'Authorization': 'Bearer {}'.format(self.__token)}).json()

		return response['{}s'.format(obj_class)][0]

	# **************************************************************************
	# Public functions
	# **************************************************************************
	def login_with_openid(self):
		# return requests.get(OPENID_URL.format(self.__application_id, self.__redirect_uri))
		return OPENID_URL.format(self.__application_id, self.__redirect_uri)
