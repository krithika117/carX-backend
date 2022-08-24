from app import app
import os

from flaskext.mysql import MySQL
import pymysql
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'carwashapp'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
print('worked')
