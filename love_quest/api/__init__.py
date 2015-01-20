from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api')

import tokens, coupons, links, users