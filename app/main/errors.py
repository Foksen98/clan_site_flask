from flask import render_template, request, jsonify
from app.main import main


@main.app_errorhandler(401)
def unauthorized(e):
	if request.accept_mimetypes.accept_json and \
			not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'unauthorized'})
		response.status_code = 401
		return response
	return render_template('errors/401.html'), 401


@main.app_errorhandler(403)
def forbidden(e):
	if request.accept_mimetypes.accept_json and \
			not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'forbidden'})
		response.status_code = 403
		return response
	return render_template('errors/403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
	if request.accept_mimetypes.accept_json and \
			not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'not found'})
		response.status_code = 404
		return response
	return render_template('errors/404.html'), 404


@main.app_errorhandler(405)
def method_not_allowed(e):
	if request.accept_mimetypes.accept_json and \
			not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'not allowed'})
		response.status_code = 404
		return response
	return render_template('errors/405.html'), 405


@main.app_errorhandler(500)
def internal_server_error(e):
	if request.accept_mimetypes.accept_json and \
			not request.accept_mimetypes.accept_html:
		response = jsonify({'error': 'internal server error'})
		response.status_code = 500
		return response
	return render_template('errors/500.html'), 500

# TODO:
# ВХОД ПО OPENID
# 401 AUTH_CANCEL Пользователь отменил авторизацию для приложения
# 403 AUTH_EXPIRED Превышено время ожидания авторизации пользователя
# 410 AUTH_ERROR Ошибка аутентификации
