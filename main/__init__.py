from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap
import sqlite3
from flask_bcrypt import Bcrypt
from myFashionRecommender.config.configuration import ConfigurationManager

config = ConfigurationManager()
database_config = config.get_database_config()
app = Flask(__name__)
app.config['SECRET_KEY'] = database_config.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = database_config.database_uri

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

connection1 = sqlite3.connect(database_config.fashion_database_path,check_same_thread=False)
connection2 = sqlite3.connect(database_config.user_database_path,check_same_thread=False)

from main import routes