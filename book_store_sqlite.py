sk-r6qYZsjUjqHAvZAnmPV0T3BlbkFJScSp5VQvgeYWrkkmQM

https://chat.openai.com/share/9208cea3-d063-4d59-97d8-3ecebb8da980

import sqlite3
print(sqlite3.version)


CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL NOT NULL
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    # ... existing methods ...

    def view_all_books(self):
        self.cur.execute("SELECT * FROM books")
        rows = self.cur.fetchall()
        return rows

    def search_book(self, title="", author="", price=""):
        self.cur.execute("SELECT * FROM books WHERE title=? OR author=? OR price=?", (title, author, price))
        rows = self.cur.fetchall()
        return rows

    def update_book(self, id, title, author, price):
        self.cur.execute("UPDATE books SET title=?, author=?, price=? WHERE id=?", (title, author, price, id))
        self.conn.commit()

    def delete_book(self, id):
        self.cur.execute("DELETE FROM books WHERE id=?", (id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()


# Initialize the database
db = Database('bookstore.db')

# View all books
books = db.view_all_books()
for book in books:
    print(book)

# Search for a book
search_results = db.search_book(title="1984")
for result in search_results:
    print(result)

# Update a book
db.update_book(1, "1984", "George Orwell", 9.99)

# Delete a book
db.delete_book(2)

ALTER TABLE books ADD COLUMN inventory_count INTEGER NOT NULL DEFAULT 0;

CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    customer_id INTEGER,
    quantity INTEGER,
    purchase_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

class Book:
    # ... existing methods ...

    def decrement_inventory(self, quantity):
        if self.inventory_count >= quantity:
            self.inventory_count -= quantity
            # Update the database accordingly
        else:
            raise ValueError("Not enough inventory for the requested purchase.")


class Database:
    # ... existing methods ...

    def purchase_book(self, book_id, customer_id, quantity):
        # Check if enough inventory exists
        self.cur.execute("SELECT inventory_count FROM books WHERE id=?", (book_id,))
        inventory_count = self.cur.fetchone()[0]

        if inventory_count >= quantity:
            # Update book inventory
            new_inventory = inventory_count - quantity
            self.cur.execute("UPDATE books SET inventory_count=? WHERE id=?", (new_inventory, book_id))

            # Record the sale
            self.cur.execute("INSERT INTO sales (book_id, customer_id, quantity) VALUES (?, ?, ?)", (book_id, customer_id, quantity))
            self.conn.commit()
        else:
            raise ValueError("Not enough books in inventory to complete this purchase.")

    def get_sales_report(self):
        self.cur.execute("""SELECT books.title, sales.quantity, sales.purchase_time, customers.name 
                            FROM sales 
                            JOIN books ON books.id = sales.book_id 
                            JOIN customers ON customers.id = sales.customer_id""")
        rows = self.cur.fetchall()
        return rows



# Example: Handling a purchase request
try:
    db.purchase_book(book_id=1, customer_id=1, quantity=2)
    print("Purchase successful!")
except ValueError as e:
    print(str(e))  # Prints the error message if not enough inventory

# Example: Getting a sales report
sales_report = db.get_sales_report()
for record in sales_report:
    print(record)
------------------------------------------
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL NOT NULL,
    inventory_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    book_id INTEGER,
    customer_id INTEGER,
    quantity INTEGER NOT NULL,
    purchase_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);


class Book:
    def __init__(self, title, author, price, inventory_count):
        self.title = title
        self.author = author
        self.price = price
        self.inventory_count = inventory_count

class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email


import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()

    def insert_book(self, title, author, price, inventory_count):
        self.cur.execute("INSERT INTO books (title, author, price, inventory_count) VALUES (?, ?, ?, ?)", (title, author, price, inventory_count))
        self.conn.commit()

    def insert_customer(self, name, email):
        self.cur.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
        self.conn.commit()

    def purchase_book(self, book_id, customer_id, quantity):
        self.cur.execute("SELECT inventory_count FROM books WHERE id=?", (book_id,))
        inventory_count = self.cur.fetchone()[0]

        if inventory_count >= quantity:
            new_inventory = inventory_count - quantity
            self.cur.execute("UPDATE books SET inventory_count=? WHERE id=?", (new_inventory, book_id))
            self.cur.execute("INSERT INTO sales (book_id, customer_id, quantity) VALUES (?, ?, ?)", (book_id, customer_id, quantity))
            self.conn.commit()
        else:
            raise ValueError("Not enough books in inventory to complete this purchase.")

    def get_sales_report(self):
        self.cur.execute("""SELECT books.title, sales.quantity, sales.purchase_time, customers.name 
                            FROM sales 
                            JOIN books ON books.id = sales.book_id 
                            JOIN customers ON customers.id = sales.customer_id""")
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()


from db import Database
from models import Book, Customer

# Initialize the database
db = Database('bookstore.db')

# Add a new book
new_book = Book("1984", "George Orwell", 9.99, 5)
db.insert_book(new_book.title, new_book.author, new_book.price, new_book.inventory_count)

# Add a new customer
new_customer = Customer("John Doe", "johndoe@example.com")
db.insert_customer(new_customer.name, new_customer.email)

# Handle a purchase request
try:
    db.purchase_book(book_id=1, customer_id=1, quantity=2)
    print("Purchase successful!")
except ValueError as e:
    print(str(e))  # Not enough inventory

# Print the sales report
sales_report = db.get_sales_report()
for record in sales_report:
    print(record)
