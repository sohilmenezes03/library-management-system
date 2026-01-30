from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')

db = client['library']
books_collection = db['books']

@app.route('/')
def index():
    books = books_collection.find()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        genre = request.form['genre']
        
        books_collection.insert_one({
            'title': title,
            'author': author,
            'year': year,
            'genre': genre
        })
        
        return redirect(url_for('index'))
    
    return render_template('add_book.html')

@app.route('/delete_book/<book_id>')
def delete_book(book_id):
    books_collection.delete_one({'_id': ObjectId(book_id)})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
