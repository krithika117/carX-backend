from asyncio import constants
from app import app
from flask import Response
from flask import Flask, render_template, url_for, request, json, jsonify
# from flaskext.mysql import MySQL
import pymysql
import time
from timeit import default_timer as timer

from flask_cors import CORS, cross_origin
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

import sib_api_v3_sdk
from dotenv import load_dotenv
from config import mysql


@app.route("/login", methods=["POST", "GET"])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    mail = _json['mail']
    password = _json['password']
    if request.method == "POST":
        cursor.execute(
            "SELECT mail, password FROM accounts WHERE mail = (%s) AND password = (%s)", (mail, password))
        infolist = cursor.fetchall()
        if len(infolist) < 1:
            resp = jsonify({'response': 'exists'})
            return resp
        else:
            resp = jsonify({'response': 'success'})
            return resp
    cursor.close()
    conn.close()


@app.route("/login/admin", methods=["POST", "GET"])
def loginadmin():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    mail = _json['mail']
    password = _json['password']
    key = _json['key']
    if request.method == "POST":
        if mail == 'admin@gmail.com' and password == 'administrator' and key == 'radisson':
            resp = jsonify({'response': 'success'})
            return resp
        else:
            resp = jsonify({'response': 'failure'})
            return resp
    cursor.close()
    conn.close()


@app.route("/signup", methods=["POST", "GET"])
def signup():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    name = _json['name']
    mail = _json['mail']
    password = _json['password']
    contact = _json['contact']
    if request.method == "POST":
        cursor.execute("SELECT * FROM accounts WHERE mail = (%s)", (mail))
        infolist = cursor.fetchall()
        if len(infolist) < 1:
            cursor.execute(
                "INSERT INTO accounts(name, mail, password, contact) VALUES (%s,%s,%s,%s)", (name, mail, password, contact))
            resp = jsonify({'response': 'success'})
            sendMail(mail)
            conn.commit()
            print('Inserted')
            cursor.close()
            conn.close()
            return resp
        else:
            resp = jsonify({'response': 'failure'})
            return resp


@app.route("/show/service", methods=["POST", "GET"])
def showservice():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    if request.method == "POST":
        cursor.execute("SELECT * FROM services ORDER BY serviceId ASC")
        infolist = cursor.fetchall()
        print(infolist)
        print('all list')
        return jsonify({'response': infolist})


@app.route("/show/places", methods=["POST", "GET"])
def showplaces():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == "POST":
        cursor.execute("SELECT placeId, location, address FROM places")
        infolist = cursor.fetchall()
        print(infolist)
        print('all list')
        return jsonify({'response': infolist})


@app.route("/list/requests", methods=["POST", "GET"])
def list_requests():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    if request.method == "POST":
        cursor.execute("SELECT * FROM requests")
        infolist = cursor.fetchall()
        print(infolist)
        print('all list')
        return jsonify({'response': infolist})


@app.route("/get/branch", methods=["POST", "GET"])
def get_branch():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    if request.method == "POST":
        cursor.execute("SELECT * FROM places")
        infolist = cursor.fetchall()
        print(infolist)
        print('all list')
        return jsonify({'response': infolist})


@app.route("/show/associations", methods=["POST", "GET"])
def asssociations():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    if request.method == "POST":
        cursor.execute("SELECT * FROM fullbranchdetails")
        infolist = cursor.fetchall()
        print(infolist)
        print('all list')
        return jsonify({'response': infolist})


@app.route("/create/associations", methods=["POST", "GET"])
def create_asssociations():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    serviceId = _json['serviceId']
    placeId = _json['placeId']
    if request.method == "POST":
        cursor.execute("INSERT INTO branchdetails(serviceId, placeId) VALUES(%s, %s)",
                       (serviceId, placeId))
        resp = jsonify({'response': 'success'})
        conn.commit()
        print('Inserted')
        cursor.close()
        conn.close()
        return resp


@app.route("/get/services", methods=["POST", "GET"])
def get_services():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    placename = _json['placename']
    if request.method == "POST":
        cursor.execute(
            "SELECT serviceName FROM fullbranchdetails WHERE location = (%s)", (placename))
        infolist = cursor.fetchall()
        print(infolist)
        print('all list')
        return jsonify({'response': infolist})


@app.route("/get/date", methods=["POST", "GET"])
def get_date():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    placename = _json['placename']
    if request.method == "POST":
        cursor.execute(
            "SELECT DISTINCT(date) FROM requests WHERE placeId = (SELECT placeId FROM places WHERE location = (%s))", (placename))
        infolist = cursor.fetchall()
        print(infolist)
        print('all list')
        return jsonify({'response': infolist})


@app.route("/add/services", methods=["POST", "GET"])
def add_service():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    servicename = _json['servicename']
    if request.method == "POST":
        cursor.execute(
            "INSERT INTO services(serviceName) VALUES (%s)", (servicename))
        resp = jsonify({'response': 'success'})
        conn.commit()
        print('Inserted')
        cursor.close()
        conn.close()
        return resp


@app.route("/add/places", methods=["POST", "GET"])
def add_place():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    location = _json['location']
    address = _json['address']
    if request.method == "POST":
        cursor.execute(
            "INSERT INTO places(location, address) VALUES (%s,%s)", (location, address))
        resp = jsonify({'response': 'success'})
        conn.commit()
        print('Inserted')
        cursor.close()
        conn.close()
        return resp


@app.route("/search", methods=["POST", "GET"])
def search():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    placename = _json['placename']
    if request.method == "POST":
        cursor.execute(
            "SELECT places.placeId, places.location, places.address FROM places WHERE location = (%s)", (placename))
        infolist = cursor.fetchall()

        resp = jsonify({'response': infolist})
        conn.commit()
        print(infolist)
        cursor.close()
        conn.close()
        return resp


@app.route("/filter", methods=["POST", "GET"])
def filter():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    date = _json['date']
    placename = _json['placename']
    if request.method == "POST":
        cursor.execute(
            "SELECT * FROM requests WHERE date = (%s)", (date))
        infolist = cursor.fetchall()
        resp = jsonify({'response': infolist})
        conn.commit()
        print(infolist)
        cursor.close()
        conn.close()
        return resp


@app.route("/customer/filter", methods=["POST", "GET"])
def customer_filter():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    mail = _json['mail']
    if request.method == "POST":
        cursor.execute(
            "SELECT * FROM requests WHERE mail = (%s)", (mail))
        infolist = cursor.fetchall()
        resp = jsonify({'response': infolist})
        conn.commit()
        print(infolist)
        cursor.close()
        conn.close()
        return resp


@app.route("/listdata", methods=["POST", "GET"])
def listdata():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == "POST":
        cursor.execute(
            "SELECT reqId, name, mail, places.location, time, date, status FROM requests,places WHERE places.placeId = requests.placeId and requests.status='Pending'")
        infolist = cursor.fetchall()
        resp = jsonify({'response': infolist})
        conn.commit()
        print(infolist)
        cursor.close()
        conn.close()
        return resp


@app.route("/availslots", methods=["POST", "GET"])
def availslots():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    date = _json['date']
    places = _json['places']
    if request.method == "POST":
        cursor.execute(
            "SELECT * FROM slots WHERE number NOT IN(SELECT time as slot FROM requests WHERE date = (%s) AND placeId = (SELECT placeId FROM places WHERE location = (%s)))", (date, places))
        infolist = cursor.fetchall()
        resp = jsonify({'response': infolist})
        conn.commit()
        print(infolist)
        cursor.close()
        conn.close()
        return resp


@app.route("/requests", methods=["POST", "GET"])
def requests():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    date = _json['date']
    placename = _json['placename']
    slot = _json['slot']
    service = _json['service']
    customername = _json['customername']
    mail = _json['mail']
    if request.method == "POST":
        cursor.execute(
            "INSERT INTO requests(name, mail, placeId, date, time, status) VALUES (%s, %s,(SELECT placeId FROM places WHERE location = (%s)),%s,%s,'Pending')", (customername, mail, placename, date, slot))
        resp = jsonify({'response': 'success'})
        conn.commit()
        print('Inserted')
        cursor.close()
        conn.close()
        return resp


@app.route("/request/denied", methods=["POST", "GET"])
def deny_requests():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    reqId = _json['reqId']

    if request.method == "POST":
        cursor.execute(
            "UPDATE requests SET status = 'Denied' WHERE reqId = (%s)", (reqId))
        resp = jsonify({'response': 'success'})
        conn.commit()
        print('Inserted')
        cursor.close()
        conn.close()
        return resp


@app.route("/request/approved", methods=["POST", "GET"])
def approve_requests():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    _json = request.json
    reqId = _json['reqId']

    if request.method == "POST":
        cursor.execute(
            "UPDATE requests SET status = 'Approved' WHERE reqId = (%s)", (reqId))
        resp = jsonify({'response': 'success'})
        conn.commit()
        print('Inserted')
        cursor.close()
        conn.close()
        return resp

# Mail -  send in blue


def sendMail(email):
    print("Sending Mail tp " + email)
    # print(firstName)
    # print(email)
    # print(serviceClubChoice)
    # print(techClubChoice1)
    # print(techClubChoice2)

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'

 # create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration))

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{
            "email": email,
        }],
        template_id=1,
        headers={
            "X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
            "charset": "iso-8859-1"
        }
    )  # SendSmtpEmail | Values to send a transactional email

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
        print('sent')
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        print('error')
