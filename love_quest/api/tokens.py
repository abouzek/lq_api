from flask import g, jsonify, request
from models import Link, User
from . import api
from extensions import auth, db

def get_linked_user_id_for_user(id):
	link = Link.query.filter_by(first_user_id=id).first()
	if link is None:
		link = Link.query.filter_by(second_user_id=id).first()
		if link is None:
			return 0
		else:
			return link.first_user_id
	else:
		return link.second_user_id

@api.route('/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	linked_user_id = get_linked_user_id_for_user(g.user.id)
	return jsonify({'token': token.decode('ascii'), 'token_expiration_seconds':3600, 'id': g.user.id, 'linked_user_id': linked_user_id})

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