from project import app, db
from enum import Enum
from datetime import datetime, timedelta


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column('customer_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    loans = db.relationship('Loan', back_populates='customer')

    
    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr

# Define an Enum for book types
class BookType(Enum):
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.Integer, default=BookType.TYPE1)
    loans = db.relationship('Loan', back_populates='book')

    
    


    def __init__(self, name, author, year_published, book_type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type



class Loan(db.Model):
    __tablename__ = 'loan'
    id = db.Column('loan_id', db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)

    def __init__(self, cust_id, book_id, loan_date):
        self.cust_id = cust_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = self.calculate_return_date(book_id)

    def calculate_return_date(self, book_id):
        # Assume 'book_type' is defined as an attribute of the 'Book' model
        book = Book.query.get(book_id)
        if book and book.book_type == BookType.TYPE1:
            return self.loan_date + timedelta(days=10)
        elif book and book.book_type == BookType.TYPE2:
            return self.loan_date + timedelta(days=5)
        elif book and book.book_type == BookType.TYPE3:
            return self.loan_date + timedelta(days=2)
        else:
            return None


with app.app_context():
    db.create_all()