#!/usr/bin/python

from extensions import db
from app import app
from models import User, Coupon, Link


def seed():
	db.drop_all()
	db.create_all()

	# Username: test, Password: test, Link code: test
	test = User('test', 'test')
	test.password = 'test'
	test.hash_password(test.password)

	# Username: test2, Password: test2, Link code: test2
	test2 = User('test2', 'test2')
	test2.password = 'test2'
	test2.hash_password(test2.password)

	db.session.add_all((test, test2))
	db.session.commit()

	# Coupons from test1 -> test 2
	coupon1 = Coupon('Car wash', 3, test.id, test2.id)
	coupon2 = Coupon('Homework help', 1, test.id, test2.id)

	# Coupons from test2 -> test1
	coupon3 = Coupon('Back scratch', 3, test2.id, test.id)
	coupon4 = Coupon('Cook dinner', 5, test2.id, test.id)

	link = Link(test.id, test2.id)

	db.session.add_all((coupon1, coupon2, coupon3, coupon4, link))
	db.session.commit()

if __name__ == '__main__':
	with app.app_context():
		seed()

