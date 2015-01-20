from extensions import db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	password_hash = db.Column(db.String(128))
	link_code = db.Column(db.String(80), unique=True)
	push_registration = db.relationship('PushRegistration', uselist=False, backref='user')

	def __init__(self, username, link_code):
		self.username = username
		self.link_code = link_code

	def __repr__(self):
		return '<User %r>' % self.username

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def generate_auth_token(self, expiration=3600):
		from app import app
		s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
		return s.dumps({'id': self.id})

	@staticmethod
	def verify_auth_token(token):
		from app import app
		s = Serializer(app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = User.query.get(data['id'])
		return user


class Link(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
	first_user = db.relationship(User, foreign_keys=[first_user_id], uselist=False)
	second_user_id = db.Column(db.Integer, db.ForeignKey(User.id))
	second_user = db.relationship(User, foreign_keys=[second_user_id], uselist=False)

	def __init__(self, first_user_id, second_user_id):
		self.first_user_id = first_user_id
		self.second_user_id = second_user_id

	def __repr__(self):
		return '<Link %r>' % self.id


class Coupon(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	count = db.Column(db.Integer)

	owner_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	sender_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
	owner = db.relationship(User, foreign_keys=[owner_id], backref='coupons')
	sender = db.relationship(User, foreign_keys=[sender_id], backref='sent_coupons')

	def __init__(self, name, count, sender_id, owner_id):
		self.name = name
		self.count = count
		self.sender_id = sender_id
		self.owner_id = owner_id

	def __repr__(self):
		return '<Coupon %r>' % self.name


class PushRegistration(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	device_token = db.Column(db.String(255))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, user_id, device_token):
		self.user_id = user_id
		self.device_token = device_token

	def __repr__(self):
		return '<PushRegistration %r>' % self.id

