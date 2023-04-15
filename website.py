from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    book_name = db.Column(db.String(100), nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

@app.before_first_request
def create_tables():
    db.create_all() # checks whether the table exists or not, 
                    # if does not exists creates the table, 
                    # if exists then does not create a new table

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def admin_check():
    admin_name = request.form.get('username')
    admin_password = request.form.get('password')
    if admin_name == 'mom' and admin_password == '2':
       return redirect('/library')
    elif admin_name == 'dad' and admin_password == '1':
        return redirect('/add_books')
    else:    
        return render_template('login.html')
    
@app.route('/add_books')
def addmore():
    return render_template('friend_entry.html')

@app.route('/library')
def library():
    users = Book.query.all()
    return render_template('book.html',users=users)

@app.route('/books', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_name = request.form['user_name']
        book_name = request.form['book_name']
        author_name = request.form['author_name']
        genre = request.form['genre']
        rating = request.form['rating']

        user = Book(user_name=user_name, book_name=book_name, author_name=author_name, genre=genre, rating=rating)
        db.session.add(user)
        db.session.commit()

    users = Book.query.all()
    return redirect('/thank_you')

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Book.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/library')
    except:
        return "There was a problem deleting that user...."

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        users = Book.query.filter_by(user_name=user_name).all()
        return render_template('book_search.html', users=users)
    return render_template('book_search.html')

if __name__ == '__main__':
    app.run(debug=True)