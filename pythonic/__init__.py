from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)


app.config['SECRET_KEY'] = 'daa75c750b3aedd0b69a7fa6ae208e4172d1cdb3cf48b15fbf9c110899d910a5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pythonic.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy()
bcrypt = Bcrypt(app)

from pythonic import routes