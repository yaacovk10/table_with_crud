import json
from flask import Blueprint, request
from project.models import Book
from project import db

books = Blueprint('books', __name__, url_prefix='/books')

@books.route('/add', methods=['POST'])
def add_book():
    data = request.json
    name = data.get("name")
    author = data.get("author")
    year_published = data.get("year_published")
    book_type = data.get("book_type")

    if name and author and year_published and book_type:
        new_book = Book(name=name, author=author, year_published=year_published, book_type=book_type)
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

    if not book:
        return {'message': 'Book not found'}, 404

    db.session.delete(book)
    db.session.commit()
    return {'message': 'Book removed successfully'}