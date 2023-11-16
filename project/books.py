import json
from flask import Blueprint, request, render_template
from project.models import Book,Loan
from project import db

books = Blueprint('books', __name__, url_prefix='/books')



@books.route('/')
def book_list():
    return render_template('books.html', active_page='books')

@books.route('/add', methods=['POST'])
def add_book():
    data = request.json
    book_name = data.get("name")
    author_name = data.get("author")
    year_publish = data.get("year_published")
    book_typ = data.get("book_type")

    if book_name and author_name and year_publish and book_typ:
        new_book = Book(name=book_name, author=author_name, year_published=year_publish, book_type=book_typ, availability=True)
        db.session.add(new_book)
        db.session.commit()
        return {'message': 'Book added successfully'}
    else:
        return {'message': 'Missing data'}, 400

@books.route('/get', methods=['GET'])
def get_books():
    books_data = []
    for book in Book.query.all():
        books_data.append({
            'id': book.id,
            'name': book.name,
            'author': book.author,
            'year_published': book.year_published,
            'book_type': book.book_type,
            'availability': book.availability
        })
    return json.dumps(books_data)

@books.route('/update/<book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    book = Book.query.get(book_id)

    if not book:
        return {'message': 'Book not found'}, 404

    if "name" in data:
        book.name = data["name"]
    if "author" in data:
        book.author = data["author"]
    if "year_published" in data:
        book.year_published = data["year_published"]
    if "book_type" in data:
        book.book_type = data["book_type"]

    db.session.commit()
    return {'message': 'Book updated successfully'}

@books.route('/remove/<book_id>', methods=['DELETE'])
def remove_book(book_id):
    book = Book.query.get(book_id)
    # Delete related loans first
    for loan in Loan.query.filter_by(book_id=book.id).all():
        if not loan.actual_return_date:
            return {'message': 'Book is on loan. You can\'t remove it'}, 404

    Loan.query.filter_by(book_id=book.id).delete()

    if not book:
        return {'message': 'Book not found'}, 404

    db.session.delete(book)
    db.session.commit()
    return {'message': 'Book removed successfully'}