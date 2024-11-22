import requests
import sqlite3
import time

# SQLite database connection
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

# Create the books table if it doesn't exist
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL
    )
''')

# Function to fetch books by genre
def fetch_books_by_genre(genre, total_results=1000):
    max_results_per_request = 40  # Google Books API limit per request
    fetched_books = 0

    while fetched_books < total_results:
        start_index = fetched_books  # Start index for the current batch
        url = f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&startIndex={start_index}&maxResults={max_results_per_request}'
        response = requests.get(url)
        
        if response.status_code == 200:
            books_data = response.json().get('items', [])
            
            if not books_data:
                print(f"No more books found for genre '{genre}'. Ending early.")
                break

            for item in books_data:
                volume_info = item.get('volumeInfo', {})
                title = volume_info.get('title', 'Unknown Title')
                authors = volume_info.get('authors', ['Unknown Author'])
                author = ', '.join(authors)

                # Check if the book already exists in the database
                cursor.execute('''
                    SELECT * FROM books WHERE title = ? AND author = ? AND genre = ?
                ''', (title, author, genre))
                existing_book = cursor.fetchone()

                if existing_book:
                    print(f'Book already exists: {title} by {author} (Genre: {genre})')
                else:
                    # Insert book into the database
                    try:
                        cursor.execute('''
                            INSERT INTO books (title, author, genre)
                            VALUES (?, ?, ?)
                        ''', (title, author, genre))
                        print(f'Inserted: {title} by {author} (Genre: {genre})')
                        conn.commit()  # Commit changes after each book
                    except sqlite3.Error as e:
                        print(f"Error inserting book: {title} by {author}. Error: {e}")

            fetched_books += len(books_data)  # Update the count of fetched books
            print(f"Fetched {fetched_books}/{total_results} books for genre '{genre}'.")
            
            if len(books_data) < max_results_per_request:
                print(f"Fewer results returned. No more books to fetch for genre '{genre}'.")
                break  # Exit the loop if fewer books are returned than requested
        else:
            print(f"Failed to fetch books for genre '{genre}'. Status code: {response.status_code}")
            break  # Exit the loop on failure

# Fetch books for different genres
genres = ['fantasy', 'romance', 'thriller', 'sci-fi', 'mystery', 'detective', 'youth', 'adult', 'educational']
for genre in genres:
    fetch_books_by_genre(genre, total_results=1000)
    time.sleep(1)  # Add a delay to avoid hitting API rate limits

# Close the database connection properly
try:
    conn.close()
except sqlite3.Error as e:
    print(f"Error closing the database connection: {e}")
