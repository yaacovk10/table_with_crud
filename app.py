import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column('student_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    
    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr

@app.route('/customers',  methods = ['GET'])
def get_customers():
    res=[]
    for cust in Customer.query.all():
        res.append({"addr":cust.addr,"city":cust.city,"id":cust.id,"name":cust.name})
    return  (json.dumps(res))


@app.route('/customers',  methods = ['POST'])
def add_customer():
    data = request.json
    print(data)
    newCustomer = Customer(data["name"], data["city"], data["addr"])
    db.session.add(newCustomer)
    db.session.commit()
    return (data)
   
    
@app.route('/customers/<id>',  methods = ['PUT'])
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

@app.route('/customers/<id>', methods = ['DELETE'])
def delete(id):
    del_row = Customer.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return {'del': 'true'}
    return {'del': 'false'}



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
