import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from googletrans import Translator
import sqlite3

# Connect to the database
conn = sqlite3.connect('spanish_words.db')
c = conn.cursor()

# Create the database table
c.execute('''CREATE TABLE IF NOT EXISTS words
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             spanish TEXT NOT NULL,
             english TEXT NOT NULL,
             count INTEGER DEFAULT 0);''')
conn.commit()

# Create the translator object
translator = Translator()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle('Spanish Dictionary')

        # Create the search box and search button
        self.search_box = QLineEdit()
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search)

        # Create the add box, add button, and add label
        self.add_box = QLineEdit()
        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_word)
        self.add_label = QLabel('')

        # Create the table widget and set its properties
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Spanish', 'English'])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.doubleClicked.connect(self.edit_word)

        # Create the learn button and set its properties
        self.learn_button = QPushButton('Learn')
        self.learn_button.setEnabled(False)
        self.learn_button.clicked.connect(self.learn_word)

        # Create the layout for the search box and search button
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_box)
        search_layout.addWidget(self.search_button)

        # Create the layout for the add box, add button, and add label
        add_layout = QHBoxLayout()
        add_layout.addWidget(self.add_box)
        add_layout.addWidget(self.add_button)
        add_layout.addWidget(self.add_label)

        # Create the layout for the table widget and learn button
        table_layout = QVBoxLayout()
        table_layout.addWidget(self.table)
        table_layout.addWidget(self.learn_button)

        # Create the main layout and add the search and table layouts
        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addLayout(add_layout)
        main_layout.addLayout(table_layout)

        # Create a widget to hold the main layout and set it as the central widget
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Populate the table with data from the database
        self.populate_table()

    def search(self):
        # Get the search term from the search box
        search_term = self.search_box.text()

        # Clear the search box
        self.search_box.setText('')

        # Translate the search term to English
        translation = translator.translate(search_term, dest='en')
        search_term_english = translation.text

        # Search for the term in the database
