from project import app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/loans')
def loans():
    return render_template('loans.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/books')
def books():
    return render_template('books.html')


if __name__ == '__main__':
    app.run(debug=True)
