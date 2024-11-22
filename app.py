from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import Flask-CORS
import sqlite3
import random

app = Flask(__name__, static_folder='static')

# Enable CORS for all routes
CORS(app)

# Helper function to get a random book based on genre
def get_random_book(genre):
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    query = "SELECT title, author FROM books WHERE genre = ?"
    cursor.execute(query, (genre,))
    books = cursor.fetchall()
    conn.close()

    if books:
        # Create an Amazon link based on the book title and author
        book = random.choice(books)
        title, author = book
        amazon_link = f"https://www.amazon.com/s?k={title}+{author}&ref=nb_sb_noss"  # Amazon search URL
        return title, author, amazon_link
    return None

# Route to serve the frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Route to get a book recommendation
@app.route('/recommend', methods=['GET'])
def recommend():
    genre = request.args.get('genre')

    if not genre:
        return jsonify({"error": "Please provide a genre"}), 400

    book = get_random_book(genre)

    if book:
        title, author, amazon_link = book
        return jsonify({
            "title": title,
            "author": author,
            "amazon_link": amazon_link
        })
    else:
        return jsonify({"message": "No book found for this genre"}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
