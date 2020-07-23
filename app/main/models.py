from app.create_app import db, login_manager
from flask_login import UserMixin
import re


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


class Player(UserMixin, db.Document):
	serial_id = db.SequenceField()
	clan = db.ReferenceField('Clan')
	private = db.ReferenceField('PlayerPrivate')
	statistics = db.ReferenceField('PlayerStatistics')
	member = db.ReferenceField('PlayerMember')
	account_id = db.IntField(unique=True)
	created_at = db.IntField()
	global_rating = db.IntField()
	last_battle_time = db.IntField()
	logout_at = db.IntField()
	nickname = db.StringField()
	# avatar = db.ImageField() - или лучше хранить url ?

	def get_id(self):
		return str(self.id)

	def get_info(self):
		return self.to_json()


class PlayerPrivate(db.Document):
	serial_id = db.SequenceField()
	player = db.ReferenceField('Player')
	ban_info = db.StringField()
	ban_time = db.IntField()
	bonds = db.IntField()
	gold = db.IntField()
	credits = db.IntField()
	free_xp = db.IntField()
	is_premium = db.BooleanField()
	premium_expires_at = db.IntField()

	def get_info(self):
		return self.to_json()


class PlayerStatistics(db.Document):
	serial_id = db.SequenceField()
	player = db.ReferenceField('Player')
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


class PlayerMember(db.Document):
	serial_id = db.SequenceField()
	player = db.ReferenceField('Player')
	joined_at = db.IntField()
	role = db.StringField()
	role_i18n = db.StringField()

	def get_info(self):
		return self.to_json()


class PlayerToken(db.Document):
	serial_id = db.SequenceField()
	player = db.ReferenceField('Player')
	access_token = db.StringField()
	expires_at = db.IntField()

	def get_info(self):
		return self.to_json()


@login_manager.user_loader
def load_user(account_id):
	try:
		return Player.objects(account_id=account_id).first()
	except:
		return None
