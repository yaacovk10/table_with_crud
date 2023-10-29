from project import app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html', active_page='home')

@app.route('/loans')
def loans():
    return render_template('loans.html', active_page='loans')

@app.route('/customers')
def customers():
    return render_template('customers.html', active_page='customers')

@app.route('/books')
def books():
    return render_template('books.html', active_page='books')


if __name__ == '__main__':
    app.run(debug=True)
