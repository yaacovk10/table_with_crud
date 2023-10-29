import datetime
import json
from flask import Blueprint, jsonify, request, render_template
from project.models import  Customer,Book, Loan
from project import db

loans = Blueprint('loans', __name__, url_prefix='/loans')



@loans.route('/')
def book_list():
    return render_template('loans.html', active_page='loans')


@loans.route('/add', methods=['POST'])
def add_loan():
    data = request.get_json()
    if 'book_id' not in data or 'cust_id' not in data:
        return jsonify({'message': 'Missing book_id or cust_id'}), 400

    book_id = data['book_id']
    cust_id = data['cust_id']

    book = Book.query.get(book_id)
    customer = Customer.query.get(cust_id)

    if not book or not customer:
        return jsonify({'message': 'Book or Customer not found'}), 404

    if book.availability:
        loan_date = datetime.datetime.now().date()

        new_loan = Loan(cust_id=cust_id, book_id=book_id, loan_date=loan_date)
        new_loan.planned_return_date = new_loan.calculate_return_date(book_id)

        # Update book availability
        book.availability = False

        db.session.add(new_loan)
        db.session.commit()
        print(f"return_date   = {new_loan.planned_return_date}")
        loan_info = {
            'cust_id': cust_id,
            'cust_first_name': customer.first_name,
            'cust_last_name': customer.last_name,
            'book_id': book_id,
            'book_name': book.name,
            'book_author': book.author,
            'loan_date': loan_date.strftime('%Y-%m-%d'),
            'return_date': new_loan.planned_return_date.strftime('%Y-%m-%d')
        }

        return jsonify({'message': 'Loan added successfully', 'loan_info': loan_info}), 200
    else:
        return jsonify({'message': 'Book not available for loan'}), 400


@loans.route('/get', methods=['GET'])
def get_loans():
    loans_data = []
    for loan in Loan.query.all():
        customer = Customer.query.get(loan.cust_id)
        book = Book.query.get(loan.book_id)
        loans_data.append({
            'loan_id': loan.id,
            'cust_id': loan.cust_id,
            'customer_first_name': customer.first_name,
            'customer_last_name': customer.last_name,
            'book_id': loan.book_id,
            'book_name': book.name,
            'loan_date': loan.loan_date.isoformat(),
            'planned_return_date': loan.planned_return_date.isoformat() if not loan.actual_return_date else None,
            'actual_return_date': loan.actual_return_date.isoformat() if loan.actual_return_date else None
        })
    return json.dumps(loans_data)




@loans.route('/end/<int:loan_id>', methods=['PUT'])
def end_loan(loan_id):
    loan = Loan.query.get(loan_id)

    if not loan:
        return jsonify({'message': 'Loan not found'}), 404

    if loan.actual_return_date:
        return jsonify({'message': 'Loan already ended'}), 400

    book = Book.query.get(loan.book_id)

    if not book:
        return jsonify({'message': 'Book not found'}), 404

    book.availability = True  # Update book availability to True (book is available)
    loan.actual_return_date = datetime.datetime.now().date()

    db.session.commit()

    return jsonify({'message': 'Loan ended successfully', 'loan_id': loan_id}), 200


@loans.route('/get-book-type/<int:book_id>', methods=['GET'])
def get_book_type(book_id):
    book = Book.query.get(book_id)
    if book:
        return {'book_type': book.book_type}
    return {'book_type': None}
