import json
from flask import  Blueprint, request, render_template
from project.models import Customer
from project import db

customers = Blueprint('customers', __name__, url_prefix= '/customers' )

@customers.route('/')
def home():
    return render_template('index.html')

@customers.route('/get',  methods = ['GET'])
def get_customers():
    res=[]
    for cust in Customer.query.all():
        res.append({"addr":cust.addr,"city":cust.city,"id":cust.id,"name":cust.name})
    return  (json.dumps(res))

@customers.route('/add',  methods = ['POST'])
def add_customer():
    data = request.json
    print(data)
    newCustomer = Customer(data["name"], data["city"], data["addr"])
    db.session.add(newCustomer)
    db.session.commit()
    return (data)

   
    
@customers.route('/<id>',  methods = ['PUT'])
def upd_cust(id):
    data = request.json
    upd_row = Customer.query.filter_by(id=id).first()
    if upd_row:
        upd_row.city = data['city']
        upd_row.name = data["name"]
        upd_row.addr = data["addr"]
        db.session.commit()
        return {'upd': 'true'}
    return {'upd': 'false'}

@customers.route('/<id>', methods = ['DELETE'])
def delete(id):
    del_row = Customer.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return {'del': 'true'}
    return {'del': 'false'}