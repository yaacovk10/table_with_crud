import json
from flask import Blueprint, request, render_template
from project.models import Customer
from project import db

customers = Blueprint('customers', __name__, url_prefix='/customers')

@customers.route('/')
def home():
    return render_template('index.html')

@customers.route('/get', methods=['GET'])
def get_customers():
    res = []
    for cust in Customer.query.all():
        res.append({"id": cust.id, "first_name": cust.first_name, "last_name": cust.last_name, "city": cust.city, "age": cust.age})
    return json.dumps(res)


@customers.route('/add', methods=['POST'])
def add_customer():
    data = request.json
    existing_customer = Customer.query.filter_by(id=data["cust_id"]).first()

    if existing_customer:
        return json.dumps({"error": "Customer with the same ID already exists"})
    else:
        newCustomer = Customer(
            id=data["cust_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            city=data["cust_city"],
            age=data["cust_age"],
        )
        db.session.add(newCustomer)
        db.session.commit()
        return json.dumps(data)


@customers.route('/<id>', methods=['PUT'])
def upd_cust(id):
    data = request.json
    upd_row = Customer.query.filter_by(id=id).first()
    if upd_row:
        upd_row.city = data['city']
        upd_row.first_name = data["first_name"]
        upd_row.last_name = data["last_name"]
        upd_row.age = data["age"]
        db.session.commit()
        return {'upd': 'true'}
    return {'upd': 'false'}


@customers.route('/<id>', methods=['DELETE'])
def delete(id):
    del_row = Customer.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return {'del': 'true'}
    return {'del': 'false'}
