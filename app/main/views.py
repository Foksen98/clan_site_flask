from flask import render_template, session, request, redirect, url_for, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.main import main
from app.main.models import Clan, Account, AccountToken
from app.main.wg_api import WG_API, WG_API_CONST


@main.route('/favicon.ico')
def favicon():
	return redirect(url_for('static', filename='images/emblem_195x195.png'))


@main.route('/login/', methods=['GET'])
def login():
	return redirect(WG_API().get_openid_url())


@main.route('/logout/', methods=['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('.index'))


@main.route('/authorization/', methods=['GET'])
def authorization():
	args = request.args
	if args.get(WG_API_CONST().RESPONSE_STATUS) == 'error':
		abort(int(args.get(WG_API_CONST().RESPONSE_CODE)))

	# обновление токена игрока
	AccountToken.objects(account_id=args.get(WG_API_CONST().ACCOUNT_ID)).update_one(
		account_id=args.get(WG_API_CONST().ACCOUNT_ID),
		access_token=args.get(WG_API_CONST().ACCOUNT_TOKEN_ACCESS_TOKEN),
		expires_at=args.get(WG_API_CONST().ACCOUNT_TOKEN_EXPIRES_AT),
		upsert=True)
	account_token = AccountToken.objects(account_id=args.get(WG_API_CONST().ACCOUNT_ID)).first()
	Account.objects(account_id=args.get(WG_API_CONST().ACCOUNT_ID)).update_one(
		account_id=args.get(WG_API_CONST().ACCOUNT_ID),
		token=account_token,
		upsert=True)
	# обновление инфо об игроке при помощи токена
	account = Account.objects(account_id=args.get(WG_API_CONST().ACCOUNT_ID)).first().update_account_info()
	# авторизация игрока в приложении
	login_user(account)

	return redirect(url_for('.index'))


@main.route('/', methods=['GET'])
def index():
	return render_template("main/index.html")
