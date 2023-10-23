
from flask import Flask
from flask_sqlalchemy import SQLAlchemy





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

from project.customers import customers
from project.loans import loans
app.register_blueprint(loans)
app.register_blueprint(customers)