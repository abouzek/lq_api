from flask import jsonify
from models import Coupon, User
from schemas import CouponSchema
from extensions import auth, send_push
from . import api

coupon_schema = CouponSchema()

@api.route('/coupons', methods=['POST'])
@auth.login_required
def create_coupon():
	owner_id = request.json.get('owner')['id']
	sender_id = request.json.get('sender')['id']
	name = request.json.get('name')
	count = request.json.get('count')

	if owner_id is None or sender_id is None or name is None or count is None:
		abort(400)
	# Still need to check for pre existing coupon

	coupon = Coupon(name, count, sender_id, owner_id)
	db.session.add(coupon)
	db.session.commit()

	msg = coupon.sender.username + " just gave you a new coupon: " + name
	send_push(msg, coupon.sender)

	return jsonify(coupon_schema.dump(coupon).data)

@api.route('/coupons/<int:id>', methods=['GET'])
@auth.login_required
def get_coupon(id):
	coupon = Coupon.query.get_or_404(id)
	return jsonify(coupon_schema.dump(coupon).data)

@api.route('/coupons/<int:id>', methods=['PUT'])
@auth.login_required
def update_coupon(id):
	owner_id = request.json.get('owner')['id']
	sender_id = request.json.get('sender')['id']
	name = request.json.get('name')
	count = request.json.get('count')

	if owner_id is None or sender_id is None or name is None or count is None:
		abort(400)

	coupon = Coupon.query.get_or_404(id)
	coupon.owner_id = owner_id
	coupon.sender_id = sender_id
	coupon.name = name
	coupon.count = count

	db.session.commit()
	return '', 204

@api.route('/coupons/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_coupon(id):
	coupon = Coupon.query.get_or_404(id)

	msg = coupon.sender.username + " removed a coupon you had: " + coupon.name
	send_push(msg, coupon.sender)

	db.session.delete(coupon)
	db.session.commit()
	return '', 204