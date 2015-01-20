from models import User, Link, Coupon, PushRegistration
from marshmallow import Schema, fields

class UserSchema(Schema):
	class Meta:
		fields = ["id", "username", "link_code"]

	coupons = fields.Nested('CouponSchema', many=True)
	sent_coupons = fields.Nested('CouponSchema', many=True)

	def make_object(self, data):
		return User(**data)

class LinkSchema(Schema):
	class Meta:
		fields = ["id", "first_user", "second_user"]

	first_user = fields.Nested('UserSchema', only=['id'])
	second_user = fields.Nested('UserSchema', only=['id'])

	def make_object(self, data):
		return Link(**data)

class CouponSchema(Schema):
	class Meta:
		fields = ["id", "name", "count", "owner", "sender"]

	owner = fields.Nested(UserSchema, only=['id'])
	sender = fields.Nested(UserSchema, only=['id'])

	def make_object(self, data):
		return Coupon(**data)

class PushRegistrationSchema(Schema):
	class Meta:
		fields = ["id", "user_id", "device_token"]

	def make_object(self, data):
		return PushRegistration(**data)