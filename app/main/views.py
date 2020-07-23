from flask import render_template, session, request, redirect, url_for, abort, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.main import main
from app.main.models import Clan, Player
from app.main.wg_api import WG_API


@main.route('/favicon.ico')
def favicon():
    # return redirect(url_for('static', filename='images/favicon.ico'))
    return redirect(url_for('static', filename='images/emblem_195x195.png'))


@main.route('/login/', methods=['GET', 'POST'])
def login():
	return redirect(WG_API().login_with_openid())


@main.route('/logout/', methods=['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('.index'))


@main.route('/authorization/', methods=['GET', 'POST'])
def authorization():
    args = request.args
    if args.get('status') == 'error':
        abort(args.get('code'))

    print(args)

	# login_user(player)
    login_user(current_user)

    return redirect(url_for('.index'))


@main.route('/', methods=['GET'])
def index():
	return render_template("main/index.html")
