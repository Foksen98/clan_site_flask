from flask_login import UserMixin
from app.create_app import db, login_manager
from app.main.wg_api import WG_API, WG_API_CONST


class Clan(db.Document):
	serial_id = db.SequenceField()
	clan_id = db.IntField(unique=True)
	accepts_join_requests = db.BooleanField()
	color = db.StringField()
	created_at = db.IntField()
	description = db.StringField()
	description_html = db.StringField()
	members_count = db.IntField()
	motto = db.StringField()
	name = db.StringField()
	tag = db.StringField()
	updated_at = db.IntField()
	# emblem = db.StringField() - много ссылок на эмблемы разных размеров
	# online_members = db.ListField(db.IntField()) - вообще не приходит это поле
	# clan_treasury - казна клана (credits, crystal, gold) - приходит только gold, а в crystal - null

	def get_info(self):
		return self.to_json()


class Account(UserMixin, db.Document):
	serial_id = db.SequenceField()
	clan = db.ReferenceField('Clan')
	private = db.ReferenceField('AccountPrivate')
	statistics = db.ReferenceField('AccountStatistics')
	member = db.ReferenceField('AccountMember')
	token = db.ReferenceField('AccountToken')
	account_id = db.IntField(unique=True)
	created_at = db.IntField()
	global_rating = db.IntField()
	last_battle_time = db.IntField()
	logout_at = db.IntField()
	nickname = db.StringField()
	updated_at = db.IntField()
	# avatar = db.ImageField() - или лучше хранить url ?
	# name = db.StringField() - настоящее имя игрока

	def __set_public_info(self, account_info):
		self.created_at = account_info.get(WG_API_CONST().ACCOUNT_CREATED_AT)
		self.global_rating = account_info.get(WG_API_CONST().ACCOUNT_GLOBAL_RATING)
		self.last_battle_time = account_info.get(WG_API_CONST().ACCOUNT_LAST_BATTLE_TIME)
		self.logout_at = account_info.get(WG_API_CONST().ACCOUNT_LOGOUT_AT)
		self.nickname = account_info.get(WG_API_CONST().ACCOUNT_NICKNAME)
		self.updated_at = account_info.get(WG_API_CONST().ACCOUNT_UPDATED_AT)

		return self

	# **************************************************************************
	# Public methods
	# **************************************************************************
	def get_id(self):
		return str(self.id)

	def get_info(self):
		return self.to_json()

	def update_account_info(self):
		account_info = WG_API().get_account_info(self.account_id, self.token.access_token).get(WG_API_CONST().RESPONSE_DATA).get(str(self.account_id))
		self.__set_public_info(account_info)
		# private
		if (account_info.get(WG_API_CONST().ACCOUNT_PRIVATE)):
			AccountPrivate.objects(account_id=self.account_id).update_one(account_id=self.account_id, updated_at=self.updated_at, upsert=True)
			self.private = AccountPrivate.objects(account_id=self.account_id).first().update_account_private(account_info.get(WG_API_CONST().ACCOUNT_PRIVATE)).save()
		# statistics
		AccountStatistics.objects(account_id=self.account_id).update_one(account_id=self.account_id, upsert=True)
		self.statistics = AccountStatistics.objects(account_id=self.account_id).first().update_account_statistics(account_info.get(WG_API_CONST().ACCOUNT_STATISTICS).get(WG_API_CONST().ACCOUNT_STATISTICS_ALL)).save()

		return self.save()


class AccountPrivate(db.Document):
	serial_id = db.SequenceField()
	account_id = db.IntField(unique=True)
	ban_info = db.StringField()
	ban_time = db.IntField()
	bonds = db.IntField()
	gold = db.IntField()
	credits = db.IntField()
	free_xp = db.IntField()
	is_premium = db.BooleanField()
	premium_expires_at = db.IntField()
	# значение берется из account и показывает последнее обновление "приватных" полей (на случай прекращения действия токена)
	updated_at = db.IntField()

	def get_info(self):
		return self.to_json()

	def update_account_private(self, account_private_info):
		self.ban_info = account_private_info.get(WG_API_CONST().ACCOUNT_PRIVATE_BAN_INFO)
		self.ban_time = account_private_info.get(WG_API_CONST().ACCOUNT_PRIVATE_BAN_TIME)
		self.bonds = account_private_info.get(WG_API_CONST().ACCOUNT_PRIVATE_BONDS)
		self.gold = account_private_info.get(WG_API_CONST().ACCOUNT_PRIVATE_GOLD)
		self.credits = account_private_info.get(WG_API_CONST().ACCOUNT_PRIVATE_CREDITS)
		self.free_xp = account_private_info.get(WG_API_CONST().ACCOUNT_PRIVATE_FREE_XP)
		self.is_premium = account_private_info.get(WG_API_CONST().ACCOUNT_PRIVATE_IS_PREMIUM)
		self.premium_expires_at = account_private_info.get(WG_API_CONST().ACCOUNT_PRIVATE_PREMIUM_EXPIRES_AT)

		return self


class AccountStatistics(db.Document):
	serial_id = db.SequenceField()
	account_id = db.IntField(unique=True)
	battle_avg_xp = db.IntField()
	battles = db.IntField()
	wins = db.IntField()
	draws = db.IntField()
	losses = db.IntField()
	survived_battles = db.IntField()
	hits_percents = db.IntField()
	max_damage = db.IntField()
	max_damage_tank_id = db.IntField()
	max_frags = db.IntField()
	max_frags_tank_id = db.IntField()
	max_xp= db.IntField()
	max_xp_tank_id = db.IntField()

	def get_info(self):
		return self.to_json()

	def update_account_statistics(self, account_statistics_info):
		self.battle_avg_xp = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_BATTLE_AVG_XP)
		self.battles = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_BATTLES)
		self.wins = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_WINS)
		self.draws = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_DRAWS)
		self.losses = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_LOSSES)
		self.survived_battles = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_SURVIVED_BATTTLES)
		self.hits_percents = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_HITS_PERCENTS)
		self.max_damage = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_MAX_DAMAGE)
		self.max_damage_tank_id = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_MAX_DAMAGE_TANK_ID)
		self.max_frags = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_MAX_FRAGS)
		self.max_frags_tank_id = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_MAX_FRAGS_TANK_ID)
		self.max_xp = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_MAX_XP)
		self.max_xp_tank_id = account_statistics_info.get(WG_API_CONST().ACCOUNT_STATISTICS_MAX_XP_TANK_ID)

		return self


class AccountMember(db.Document):
	serial_id = db.SequenceField()
	account_id = db.IntField(unique=True)
	joined_at = db.IntField()
	role = db.StringField()
	role_i18n = db.StringField()

	def get_info(self):
		return self.to_json()


class AccountToken(db.Document):
	serial_id = db.SequenceField()
	account_id = db.IntField(unique=True)
	access_token = db.StringField()
	expires_at = db.IntField()

	def get_info(self):
		return self.to_json()

	# TODO: продление токена (если не удалось продлить, удаляем AccountToken, AccountPrivate перестает обновляться)
	def plrolongate_token():
		return True


@login_manager.user_loader
def load_user(account_id):
	try:
		return Account.objects(id=account_id).first()
	except:
		return None
