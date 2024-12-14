from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton,
    QTabWidget, QLabel, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QStatusBar, QMessageBox
)
from PyQt5.QtCore import Qt
from database_manager import DatabaseManager  # Ensure this is implemented and functional
import logging

# Set up logging to capture errors
logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 1000, 700)

        # Base Stylesheet
        self.setStyleSheet("""
            QWidget { background-color: #FFFFFF; color: #000000; font-family: Arial; font-size: 14px; }
            QPushButton { background-color: #000000; color: #FFFFFF; padding: 10px 15px; border-radius: 5px; font-weight: bold; }
            QPushButton:hover { background-color: #303030; }
            QPushButton:pressed { background-color: #505050; }
            QLineEdit { padding: 8px; border: 1px solid #000000; border-radius: 5px; background-color: #FFFFFF; }
            QLabel { font-size: 16px; font-weight: bold; }
            QTableWidget { background-color: #FFFFFF; border: 1px solid #000000; gridline-color: #000000; font-size: 13px; }
            QHeaderView::section { background-color: #000000; color: #FFFFFF; padding: 5px; border: 1px solid #000000; }
            QStatusBar { background-color: #F0F0F0; color: #000000; padding: 5px; }
        """)

        main_layout = QVBoxLayout(self)

        # Tabs for navigation
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #000000; background-color: #FFFFFF; }
            QTabBar::tab { background-color: #D3D3D3; padding: 10px; margin: 3px; border-radius: 5px; font-weight: bold; color: #000000; }
            QTabBar::tab:selected { background-color: #000000; color: #FFFFFF; }
        """)
        main_layout.addWidget(self.tabs)

        # Initialize tabs
        self.manage_books_tab = QWidget()
        self.about_tab = QWidget()

        # Add tabs
        self.tabs.addTab(self.manage_books_tab, "Manage Books")
        self.tabs.addTab(self.about_tab, "About")

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("background-color: #F0F0F0; color: #000000;")
        main_layout.addWidget(self.status_bar)

        # Setup tabs
        self.setup_manage_books_tab()
        self.setup_about_tab()

        self.setLayout(main_layout)

    def setup_manage_books_tab(self):
        layout = QVBoxLayout()

        # Welcome Text
        welcome_label = QLabel("Welcome to Limkokwing Library Management System")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #000000;")
        layout.addWidget(welcome_label)

        # Search bar with dynamic update
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Title, Author, or ISBN...")
        self.search_button = QPushButton("Search")
        self.clear_search_button = QPushButton("Clear Search")

        self.search_button.clicked.connect(self.dynamic_search)
        self.clear_search_button.clicked.connect(self.clear_search)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.clear_search_button)
        layout.addLayout(search_layout)

        # Form for book details
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #FFFFFF; border: 2px solid #000000; border-radius: 10px; padding: 20px;")
        form_layout = QFormLayout(form_frame)

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.year_input = QLineEdit()

        form_fields = [
            ("Title:", self.title_input),
            ("Author:", self.author_input),
            ("ISBN:", self.isbn_input),
            ("Genre:", self.genre_input),
            ("Year:", self.year_input),
        ]
        for label, field in form_fields:
            form_layout.addRow(label, field)

        layout.addWidget(form_frame)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Book")
        self.update_button = QPushButton("Update Book")
        self.delete_button = QPushButton("Delete Book")
        self.clear_form_button = QPushButton("Clear Form")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_form_button)
        layout.addLayout(button_layout)

        # Table for displaying books
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Genre", "Year"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnHidden(0, True)  # Hide ID column
        layout.addWidget(self.table)

        # Highlight selected row
        self.table.itemSelectionChanged.connect(self.highlight_selected_row)

        # Connect buttons
        self.add_button.clicked.connect(self.add_book)
        self.update_button.clicked.connect(self.update_book)
        self.delete_button.clicked.connect(self.delete_book)
        self.clear_form_button.clicked.connect(self.clear_form)

        self.manage_books_tab.setLayout(layout)
        self.update_table()

    def setup_about_tab(self):
        layout = QVBoxLayout()
        about_label = QLabel("<h1>Welcome to the Library Management System</h1>")
        about_label.setAlignment(Qt.AlignCenter)
        about_label.setStyleSheet("color: #000000; font-size: 24px; font-weight: bold;")
        about_content = QLabel("Version: 1.0\n\nDeveloped by: FODAY SESAY\n\nFeatures:\n- Manage Books\n- Dynamic Search\n- Easy Navigation")
        about_content.setAlignment(Qt.AlignCenter)
        about_content.setStyleSheet("color: #505050; font-size: 18px;")
        layout.addWidget(about_label)
        layout.addWidget(about_content)
        self.about_tab.setLayout(layout)

    def dynamic_search(self):
        try:
            query = self.search_input.text().strip()
            results = self.db.search(query) if query else self.db.get_books()
            self.populate_table(results)
        except Exception as e:
            logging.error(f"Error during dynamic search: {e}")
            QMessageBox.critical(self, "Error", "An error occurred while searching the books.")

    def clear_search(self):
        self.search_input.clear()
        self.update_table()

    def highlight_selected_row(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row >= 0:
                # Fill the form with the selected row's data
                self.title_input.setText(self.table.item(selected_row, 1).text())
                self.author_input.setText(self.table.item(selected_row, 2).text())
                self.isbn_input.setText(self.table.item(selected_row, 3).text())
                self.genre_input.setText(self.table.item(selected_row, 4).text())
                self.year_input.setText(self.table.item(selected_row, 5).text())
        except Exception as e:
            logging.error(f"Error while highlighting selected row: {e}")
            QMessageBox.critical(self, "Error", "An error occurred while highlighting the row.")

    def populate_table(self, books):
        try:
            self.table.setRowCount(0)
            for row, book in enumerate(books):
                self.table.insertRow(row)
                for col, data in enumerate(book):
                    self.table.setItem(row, col, QTableWidgetItem(str(data)))
        except Exception as e:
            logging.error(f"Error while populating table: {e}")
            QMessageBox.critical(self, "Error", "An error occurred while populating the table.")

    def update_table(self):
        self.populate_table(self.db.get_books())

    def add_book(self):
        try:
            title = self.title_input.text().strip()
            author = self.author_input.text().strip()
            isbn = self.isbn_input.text().strip()
            genre = self.genre_input.text().strip()
            year = self.year_input.text().strip()

            if not title or not author or not isbn or not genre or not year:
                QMessageBox.warning(self, "Input Error", "All fields must be filled.")
                return

            self.db.add_book(title, author, isbn, genre, year)
            self.clear_form()
            self.update_table()
        except Exception as e:
            logging.error(f"Error adding book: {e}")
            QMessageBox.critical(self, "Error", "An error occurred while adding the book.")

    def update_book(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Selection Error", "Please select a book to update.")
                return

            book_id = self.table.item(selected_row, 0).text()
            title = self.title_input.text().strip()
            author = self.author_input.text().strip()
            isbn = self.isbn_input.text().strip()
            genre = self.genre_input.text().strip()
            year = self.year_input.text().strip()

            if not title or not author or not isbn or not genre or not year:
                QMessageBox.warning(self, "Input Error", "All fields must be filled.")
                return

            self.db.update_book(book_id, title, author, isbn, genre, year)
            self.clear_form()
            self.update_table()
        except Exception as e:
            logging.error(f"Error updating book: {e}")
            QMessageBox.critical(self, "Error", "An error occurred while updating the book.")

    def delete_book(self):
        try:
            selected_row = self.table.currentRow()
            if selected_row < 0:
                QMessageBox.warning(self, "Selection Error", "Please select a book to delete.")
                return

            book_id = self.table.item(selected_row, 0).text()
            self.db.delete_book(book_id)
            self.clear_form()
            self.update_table()
        except Exception as e:
            logging.error(f"Error deleting book: {e}")
            QMessageBox.critical(self, "Error", "An error occurred while deleting the book.")

    def clear_form(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.genre_input.clear()
        self.year_input.clear()
