from flask import jsonify, request
from models import PushRegistration
from schemas import PushRegistrationSchema
from extensions import auth, db
from . import api

push_schema = PushRegistrationSchema()

@api.route('/push', methods=['POST'])
@auth.login_required
def create_push():
	user_id = request.json.get('user')['id']
	device_token = request.json.get('device_token')

	if user_id is None or device_token is None:
		abort(400)

	push = PushRegistration.query.filter_by(device_token=device_token).filter(User.id == user_id).first()
	if push is not None:
		abort(409)

	push = PushRegistration(user_id, device_token)
	db.session.add(push)
	db.session.commit()

	return jsonify(push_schema.dump(push).data)

@api.route('/push/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_push(id):
	push = PushRegistration.query.get_or_404(id)
	db.session.delete(push)
	db.session.commit()
	return '', 204
