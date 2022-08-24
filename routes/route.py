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


@app.route("/select/req", methods=["POST", "GET"])
def select_data():
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
            "INSERT INTO requests(name, mail, placeId, date, time, status) VALUES (%s, %s,(SELECT placeId FROM places WHERE location = (%s)),%s,%s,0)", (customername, mail, placename, date, slot))
        resp = jsonify({'response': 'success'})
        conn.commit()
        print('Inserted')
        cursor.close()
        conn.close()
        return resp
