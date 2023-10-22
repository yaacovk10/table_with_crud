from project import app, db



class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column('customer_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    
    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr

with app.app_context():
    db.create_all()