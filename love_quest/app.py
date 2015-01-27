from flask import Flask
from extensions import db, heroku
from api import api
from sys import stdout
import logging

app = Flask(__name__)
app.config.update(
	#SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
	SECRET_KEY='the quick brown fox jumps over the lazy dog',
	SQLALCHEMY_COMMIT_ON_TEARDOWN=True
)

app.logger.addHandler(logging.StreamHandler(stdout))
app.logger.setLevel(logging.ERROR)

heroku.init_app(app)
db.init_app(app)

app.register_blueprint(api)

with app.app_context():
	db.create_all()

if __name__ == '__main__':
	app.run(debug=True)

