from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from apns import APNs, Payload
from flask.ext.heroku import Heroku
from functools import wraps

db = SQLAlchemy()
heroku = Heroku()
auth = HTTPBasicAuth()
apns = APNs(use_sandbox=True, cert_file='dev-cer.pem')

def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='application/json; charset=utf-8')
    return decorated_function


def send_push(msg, user):
	if user.push_registration is not None:
		payload = Payload(alert=msg, sound="default", badge=1)
		apns.gateway_server.send_notification(user.push_registration.device_token, payload)