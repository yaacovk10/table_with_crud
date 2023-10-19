import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from customers import customers


app = Flask(__name__)
app.register_blueprint(customers)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"





if __name__ == '__main__':
    app.run(debug=True)
