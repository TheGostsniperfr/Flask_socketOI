from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    data_created = db.Column(db.DateTime, default=datetime.now)

#req = "CREATE TABLE IF NOT EXISTS playerDB ( Id INTEGER  PRIMARY KEY, username TEXT, maxScore INTEGER );"
#curseur.execute(req)


#req = 'INSERT INTO playerDB (username, maxScore) VALUES ("thomas", 1);'
#curseur.execute(req)
"""

req = "SELECT * FROM playerDB;"
curseur.execute(req)
print(curseur.fetchall())




bdd.close()

"""