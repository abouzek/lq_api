from flask import jsonify, request
from json import dumps
from models import User, Link, Coupon
from schemas import UserSchema, CouponSchema, LinkSchema
from extensions import auth, returns_json, db
from . import api

user_schema = UserSchema()
coupons_schema = CouponSchema(many=True)

@api.route('/users', methods=['POST'])
def create_user():
	username = request.json.get('username')
	password = request.json.get('password')
	link_code = request.json.get('link_code')

	if username is None or password is None:
		abort(400)
	if User.query.filter_by(username=username).first() is not None:
		abort(400)

	user = User(username, link_code)
	user.hash_password(password)
	db.session.add(user)
	db.session.commit()

	return jsonify(user_schema.dump(user).data)

@api.route('/users/<int:id>', methods=['GET'])
@auth.login_required
def get_user(id):
	user = User.query.get_or_404(id)
	return jsonify(user_schema.dump(user).data)

@api.route('/users/<username>', methods=['GET'])
@auth.login_required
def get_user_by_username(username):
	user = User.query.filter_by(username=username).first_or_404()
	return jsonify(user_schema.dump(user).data)



@api.route('/users/<int:id>/link', methods=['GET'])
@auth.login_required
def get_link_for_user(id):
	link = Link.query.filter_by(first_user_id=id).first()
	if link is None:
		link = Link.query.filter_by(second_user_id=id).first_or_404()
	return jsonify(link_schema.dump(link).data)

@api.route('/users/<int:id>/coupons', methods=['GET'])
@auth.login_required
@returns_json
def get_coupons_for_user(id):
	coupons = Coupon.query.filter_by(owner_id=id).filter(Coupon.count > 0).all()
	return dumps(coupons_schema.dump(coupons).data)

@api.route('/users/<int:id>/sentCoupons', methods=['GET'])
@auth.login_required
@returns_json
def get_sent_coupons_for_user(id):
	sent_coupons = Coupon.query.filter_by(sender_id=id).filter(Coupon.count > 0).all()
	return dumps(coupons_schema.dump(sent_coupons).data)