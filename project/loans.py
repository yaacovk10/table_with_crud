import json
from flask import Blueprint, request
from project.models import  Customer,Book, Loan
from project import db

loans = Blueprint('loans', __name__, url_prefix='/loans')

@loans.route('/add', methods=['POST'])
def add_loan():
    data = request.json
    cust_id = data.get("cust_id")
    book_id = data.get("book_id")
    loan_date = data.get("loan_date")

    if cust_id and book_id and loan_date:
        # Check if the customer and book exist in the database
        customer = Customer.query.get(cust_id)
        book = Book.query.get(book_id)

        if customer and book:
            new_loan = Loan(cust_id=cust_id, book_id=book_id, loan_date=loan_date)
            db.session.add(new_loan)
            db.session.commit()
            return {'message': 'Loan added successfully'}
        else:
            return {'message': 'Customer or book not found'}, 400
    else:
        return {'message': 'Missing data'}, 400

@loans.route('/get', methods=['GET'])
def get_loans():
    loans_data = []
    for loan in Loan.query.all():
        customer = Customer.query.get(loan.cust_id)
        book = Book.query.get(loan.book_id)
        loans_data.append({
            'loan_id': loan.id,
            'cust_id': loan.cust_id,
            'customer_name': customer.name,
            'book_id': loan.book_id,
            'book_name': book.name,
            'loan_date': loan.loan_date.isoformat(),
            'return_date': loan.return_date.isoformat() if loan.return_date else None
        })
    return json.dumps(loans_data)


# Existing imports and blueprint definition

@loans.route('/end/<loan_id>', methods=['PUT'])
def end_loan(loan_id):
    data = request.json

    loan = Loan.query.get(loan_id)

    if not loan:
        return {'message': 'Loan not found'}, 404

    if "return_date" not in data:
        return {'message': 'Missing return date'}, 400

    return_date = data["return_date"]
    loan.return_date = return_date
    db.session.commit()

    return {'message': 'Loan ended successfully'}
