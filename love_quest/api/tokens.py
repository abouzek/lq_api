from flask import g, jsonify, request
from models import Link, User
from . import api
from extensions import auth, db

@api.route('/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii'), 'token_expiration_seconds':3600, 'user_id': g.user.id})

@auth.verify_password
def verify_password(username_or_token, password):
	# try to authenticate by token
	user = User.verify_auth_token(username_or_token)
	if not user:
		# try to authenticate with username/password
		user = User.query.filter_by(username=username_or_token).first()
		if not user or not user.verify_password(password):
			return False
	g.user = user
	return True