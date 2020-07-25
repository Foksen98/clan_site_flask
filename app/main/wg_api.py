import config.config_reader as cr
import requests

class WG_API_CONST:

	def __init__(self):
		# urls
		self.OPENID_URL = 'https://api.worldoftanks.ru/wot/auth/login/?application_id={}&redirect_uri={}'
		self.ACCOUNT_INFO_URL = 'https://api.worldoftanks.ru/wot/account/info/?application_id={}&account_id={}&access_token={}'
		# response keys
		self.RESPONSE_STATUS = 'status'
		self.RESPONSE_CODE = 'code'
		self.RESPONSE_DATA = 'data'
		# account response keys
		self.ACCOUNT_ID = 'account_id'
		self.ACCOUNT_CREATED_AT = 'created_at'
		self.ACCOUNT_GLOBAL_RATING = 'global_rating'
		self.ACCOUNT_LAST_BATTLE_TIME = 'last_battle_time'
		self.ACCOUNT_LOGOUT_AT = 'logout_at'
		self.ACCOUNT_NICKNAME = 'nickname'
		self.ACCOUNT_UPDATED_AT = 'updated_at'
		# account private response keys
		self.ACCOUNT_PRIVATE = 'private'
		self.ACCOUNT_PRIVATE_BAN_INFO = 'ban_info'
		self.ACCOUNT_PRIVATE_BAN_TIME = 'ban_time'
		self.ACCOUNT_PRIVATE_BONDS = 'bonds'
		self.ACCOUNT_PRIVATE_GOLD = 'gold'
		self.ACCOUNT_PRIVATE_CREDITS = 'credits'
		self.ACCOUNT_PRIVATE_FREE_XP = 'free_xp'
		self.ACCOUNT_PRIVATE_IS_PREMIUM = 'is_premium'
		self.ACCOUNT_PRIVATE_PREMIUM_EXPIRES_AT = 'premium_expires_at'
		# ...
		# account statistics response keys
		self.ACCOUNT_STATISTICS = 'statistics'
		self.ACCOUNT_STATISTICS_ALL = 'all'
		self.ACCOUNT_STATISTICS_BATTLE_AVG_XP = 'battle_avg_xp'
		self.ACCOUNT_STATISTICS_BATTLES = 'battles'
		self.ACCOUNT_STATISTICS_WINS = 'wins'
		self.ACCOUNT_STATISTICS_DRAWS = 'draws'
		self.ACCOUNT_STATISTICS_LOSSES = 'losses'
		self.ACCOUNT_STATISTICS_SURVIVED_BATTTLES = 'survived_battles'
		self.ACCOUNT_STATISTICS_HITS_PERCENTS = 'hits_percents'
		self.ACCOUNT_STATISTICS_MAX_DAMAGE = 'max_damage'
		self.ACCOUNT_STATISTICS_MAX_DAMAGE_TANK_ID = 'max_damage_tank_id'
		self.ACCOUNT_STATISTICS_MAX_FRAGS = 'max_frags'
		self.ACCOUNT_STATISTICS_MAX_FRAGS_TANK_ID = 'max_frags_tank_id'
		self.ACCOUNT_STATISTICS_MAX_XP = 'max_xp'
		self.ACCOUNT_STATISTICS_MAX_XP_TANK_ID = 'max_xp_tank_id'
		# account member response keys
		# account token response keys
		self.ACCOUNT_TOKEN_ACCESS_TOKEN = 'access_token'
		self.ACCOUNT_TOKEN_EXPIRES_AT = 'expires_at'
		# clan response keys


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
	# Public methods
	# **************************************************************************
	def get_openid_url(self):
		return WG_API_CONST().OPENID_URL.format(self.__application_id, self.__redirect_uri)

	def get_account_info(self, account_id, access_token=''):
		return requests.get(WG_API_CONST().ACCOUNT_INFO_URL.format(self.__application_id, account_id, access_token)).json()
