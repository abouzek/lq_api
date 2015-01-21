from flask import jsonify
from extensions import auth, send_push
from schemas import LinkSchema
from models import Link, User
from . import api

link_schema = LinkSchema()

@api.route('/links', methods=['POST'])
@auth.login_required
def create_link():
	user_id = request.json.get('user_id')
	link_code = request.json.get('link_code')

	if user_id is None or link_code is None:
		abort(400)
	# Still need to check for pre-existence of a link here

	second_user = User.query.filter_by(link_code=link_code).first_or_404()

	link = Link(user_id, second_user.id)
	db.session.add(link)
	db.session.commit()

	msg = link.first_user.username + " has linked up with you!"
	send_push(msg, link.second_user)

	return jsonify(link_schema.dump(link).data)

@api.route('/links/<int:id>', methods=['GET'])
@auth.login_required
def get_link(id):
	link = Link.query.get_or_404(id)
	return jsonify(link_schema.dump(link).data)

@api.route('/links/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_link(id):
	link = Link.query.get_or_404(id)

	msg = "The link between you and " + link.second_user.username + " was removed"
	send_push(push_msg, link.first_user)
	msg = "The link between you and " + link.first_user.username + " was removed"
	send_push(push_msg, link.second_user)

	db.session.delete(link)
	db.session.commit()
	return '', 204