import sqlite3
import logging

logging.basicConfig(filename="database.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

import sqlite3

class DatabaseManager:
    def __init__(self):
        self.db_path = "library.db"  # Path to your database file
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_books_table()

    def create_books_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            isbn TEXT,
            genre TEXT,
            year INTEGER
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def get_books(self):
        query = "SELECT * FROM books"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def search(self, query):
        query = f"%{query}%"  # Add wildcards for partial matching
        search_query = """
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? OR genre LIKE ?
        """
        self.cursor.execute(search_query, (query, query, query, query))
        return self.cursor.fetchall()

    def add_book(self, title, author, isbn, genre, year):
        query = "INSERT INTO books (title, author, isbn, genre, year) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(query, (title, author, isbn, genre, year))
        self.conn.commit()

    def update_book(self, book_id, title, author, isbn, genre, year):
        query = "UPDATE books SET title = ?, author = ?, isbn = ?, genre = ?, year = ? WHERE id = ?"
        self.cursor.execute(query, (title, author, isbn, genre, year, book_id))
        self.conn.commit()

    def delete_book(self, book_id):
        query = "DELETE FROM books WHERE id = ?"
        self.cursor.execute(query, (book_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


    def search_books(self, term):
        try:
            query = '''
                SELECT * FROM books
                WHERE LOWER(title) LIKE ? OR LOWER(author) LIKE ? OR isbn LIKE ?
                OR LOWER(genre) LIKE ? OR CAST(year AS TEXT) LIKE ?
            '''
            params = tuple(f"%{term.lower()}%" for _ in range(5))
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Search failed: {e}")
            return []

    def get_books(self):
        self.cursor.execute('SELECT * FROM books')
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()
