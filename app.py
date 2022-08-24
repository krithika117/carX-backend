
from flaskext.mysql import MySQL
import pymysql
# from werkzeug import check_password_ha
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from flask_mysqldb import MySQL, MySQLdb

import traceback
import sib_api_v3_sdk

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv


app = Flask(__name__)
cors = CORS(app)


@app.errorhandler(404)
def not_found(error=None):
    """
        404 handler
    """
    message = {
        'status': 404,
        'message': 'There is no record: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 404
    return res


@app.errorhandler(409)
def dup_found(error=None):
    """
        409 handler
    """
    message = {
        'status': 409,
        'message': 'There is no record: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 409
    return res


@app.errorhandler(403)
def forbidden(error=None):
    """
        403 handler
    """
    message = {
        'status': 403,
        'message': 'Forbidden',
    }
    res = jsonify(message)
    res.status_code = 403
    return res


@app.errorhandler(500)
def internal_server_error(error=None):
    """
        500 handler
    """
    message = {
        'status': 500,
        'message': 'Failed to process request',
    }
    res = jsonify(message)
    res.status_code = 500
    traceback.print_exc()
    return res


@app.errorhandler(505)
def firebase_error(error=None):
    """
        505 handler
    """
    message = {
        'status': 505,
        'message': 'Firebase Error',
        "reason": error
    }
    res = jsonify(message)
    res.status_code = 505
    traceback.print_exc()
    return res


@app.route('/')
def home():
    return "Hello"


from routes import route

if __name__ == '__main__':
    app.run(debug=True)
