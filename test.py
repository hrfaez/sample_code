88amirabedi
jZwW9zVJbNWB
proton.me
amir88abedi
jKTCRexGGmE8


import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# کلاس‌های مدل
class Book:
    def __init__(self, id, title, author, price, count):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.count = count

class Customer:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class BookSellReport:
    def __init__(self, id, book_FK, customer_FK, date):
        self.id = id
        self.book_FK = book_FK
        self.customer_FK = customer_FK
        self.date = date

# کلاس اصلی برنامه
class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title('فروشگاه کتاب')

        self.books = []  # لیستی برای نگهداری کتاب‌ها
        self.customers = []  # لیستی برای نگهداری مشتریان
        self.sales = []  # لیستی برای نگهداری گزارش‌های فروش

        # ایجاد ویجت‌ها
        self.create_widgets()

    def create_widgets(self):
        # نوار ابزار
        self.toolbar = tk.Frame(self.root)
        self.add_book_btn = tk.Button(self.toolbar, text='افزودن کتاب', command=self.show_add_book_form)
        self.add_book_btn.pack(side=tk.LEFT, padx=2)
        self.add_customer_btn = tk.Button(self.toolbar, text='افزودن مشتری', command=self.show_add_customer_form)
        self.add_customer_btn.pack(side=tk.LEFT, padx=2)
        self.sell_book_btn = tk.Button(self.toolbar, text='ثبت فروش', command=self.show_sell_book_form)
        self.sell_book_btn.pack(side=tk.LEFT, padx=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # لیست کتاب‌ها
        self.book_listbox = tk.Listbox(self.root)
        self.book_listbox.pack(fill=tk.BOTH, expand=True)

    def show_add_book_form(self):
        # فرم افزودن کتاب
        self.add_book_window = tk.Toplevel(self.root)
        self.add_book_window.title('افزودن کتاب')

        ttk.Label(self.add_book_window, text='عنوان:').grid(row=0, column=0)
        self.title_entry = ttk.Entry(self.add_book_window)
        self.title_entry.grid(row=0, column=1)

        ttk.Label(self.add_book_window, text='نویسنده:').grid(row=1, column=0)
        self.author_entry = ttk.Entry(self.add_book_window)
        self.author_entry.grid(row=1, column=1)

        ttk.Label(self.add_book_window, text='قیمت:').grid(row=2, column=0)
        self.price_entry = ttk.Entry(self.add_book_window)
        self.price_entry.grid(row=2, column=1)

        ttk.Label(self.add_book_window, text='تعداد:').grid(row=3, column=0)
        self.count_entry = ttk.Entry(self.add_book_window)
        self.count_entry.grid(row=3, column=1)

        ttk.Button(self.add_book_window, text='افزودن', command=self.add_book).grid(row=4, column=0, columnspan=2)

    def add_book(self):
        # اضافه کردن کتاب جدید
        new_book = Book(len(self.books) + 1, self.title_entry.get(), self.author_entry.get(), int(self.price_entry.get()), int(self.count_entry.get()))
        self.books.append(new_book)
        self.book_listbox.insert(tk.END, f"{new_book.title} - {new_book.author}")
        self.add_book_window.destroy()

    def show_add_customer_form(self):
        # فرم افزودن مشتری
        self.add_customer_window = tk.Toplevel(self.root)
        self.add_customer_window.title('افزودن مشتری')

        ttk.Label(self.add_customer_window, text='نام:').grid(row=0, column=0)
        self.customer_name_entry = ttk.Entry(self.add_customer_window)
        self.customer_name_entry.grid(row=0, column=1)

        ttk.Button(self.add_customer_window, text='افزودن', command=self.add_customer).grid(row=1, column=0, columnspan=2)

    def add_customer(self):
        # اضافه کردن مشتری جدید
        new_customer = Customer(len(self.customers) + 1, self.customer_name_entry.get())
        self.customers.append(new_customer)
        self.add_customer_window.destroy()
        messagebox.showinfo("موفق", "مشتری با موفقیت اضافه شد!")

    def show_sell_book_form(self):
        # فرم ثبت فروش
        if not self.books or not self.customers:
            messagebox.showerror("خطا", "لطفا ابتدا کتاب و مشتری اضافه کنید!")
            return

        self.sell_book_window = tk.Toplevel(self.root)
        self.sell_book_window.title('ثبت فروش')

        ttk.Label(self.sell_book_window, text='کتاب:').grid(row=0, column=0)
        self.book_combobox = ttk.Combobox(self.sell_book_window, values=[b.title for b in self.books])
        self.book_combobox.grid(row=0, column=1)

        ttk.Label(self.sell_book_window, text='مشتری:').grid(row=1, column=0)
        self.customer_combobox = ttk.Combobox(self.sell_book_window, values=[c.name for c in self.customers])
        self.customer_combobox.grid(row=1, column=1)

        ttk.Button(self.sell_book_window, text='ثبت فروش', command=self.sell_book).grid(row=2, column=0, columnspan=2)

    def sell_book(self):
        # ثبت فروش کتاب
        selected_book = next((b for b in self.books if b.title == self.book_combobox.get()), None)
        selected_customer = next((c for c in self.customers if c.name == self.customer_combobox.get()), None)
        if selected_book and selected_customer:
            new_sale = BookSellReport(len(self.sales) + 1, selected_book.id, selected_customer.id, datetime.datetime.now())
            self.sales.append(new_sale)
            selected_book.count -= 1  # کاهش تعداد کتاب
            self.sell_book_window.destroy()
            messagebox.showinfo("موفق", "فروش با موفقیت ثبت شد!")
        else:
            messagebox.showerror("خطا", "لطفا کتاب و مشتری معتبر انتخاب کنید!")

# ایجاد رابط کاربری
root = tk.Tk()
app = BookstoreApp(root)
root.mainloop()


-----------------------------------------------------------------------------------------------------------------------------------------------------
import tkinter as tk
from tkinter import simpledialog, messagebox
import datetime

class Book:
    def __init__(self, id, title, author, price, count):
        self.id = id
        self.title = title
        self.author = author
        self.price = price
        self.count = count


class Customer:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class BookSellReport:
    def __init__(self, id, book_FK, customer_FK, date):
        self.id = id
        self.book_FK = book_FK
        self.customer_FK = customer_FK
        self.date = date


class BookstoreGUI:
    def __init__(self, root):
        self.root = root
        root.title("Bookstore")

        # Initialize book list
        self.books = []
        self.load_books()  # Load initial books
        self.customers = []
        self.sales = []

        # Left side frames for buttons and search
        self.left_frame = tk.Frame(root, width=200, height=400)
        self.left_frame.grid(row=0, column=0, padx=10, pady=5)

        self.add_button = tk.Button(self.left_frame, text="Add Book", command=self.add_book)
        self.add_button.pack(fill=tk.BOTH, expand=True)

        self.sell_button = tk.Button(self.left_frame, text="Sell Book", command=self.sell_book)
        self.sell_button.pack(fill=tk.BOTH, expand=True)

        # Right side frames for book list
        self.right_frame = tk.Frame(root, width=300, height=400)
        self.right_frame.grid(row=0, column=1, padx=10, pady=5)

        self.search_entry = tk.Entry(self.right_frame)
        self.search_entry.pack()
        self.search_entry.bind('<KeyRelease>', self.search_books)

        self.book_list = tk.Listbox(self.right_frame)
        self.book_list.pack(fill=tk.BOTH, expand=True)

    def add_book(self):
        title = simpledialog.askstring("Title", "Enter the book title:")
        author = simpledialog.askstring("Author", "Enter the author's name:")
        price = simpledialog.askfloat("Price", "Enter the price of the book:")
        count = simpledialog.askinteger("Count", "Enter the number of copies:")
        if title and author and price and count:
            new_book = Book(len(self.books) + 1, title, author, price, count)
            self.books.append(new_book)
            self.update_book_list()

    def sell_book(self):
        selected_index = self.book_list.curselection()
        if selected_index:
            selected_book = self.books[selected_index[0]]
            if selected_book.count > 0:
                customer_name = simpledialog.askstring("Customer", "Enter the customer's name:")
                if customer_name:
                    # Update book count
                    selected_book.count -= 1

                    # Add customer and sale record
                    new_customer = Customer(len(self.customers) + 1, customer_name)
                    self.customers.append(new_customer)
                    new_sale = BookSellReport(len(self.sales) + 1, selected_book.id, new_customer.id,
                                              datetime.date.today())
                    self.sales.append(new_sale)

                    messagebox.showinfo("Success", f"Sold 1 copy of {selected_book.title} to {customer_name}.")
                    self.update_book_list()
            else:
                messagebox.showinfo("Unavailable", "This book is out of stock.")
        else:
            messagebox.showinfo("Selection", "Please select a book to sell.")

    def load_books(self):
        # Dummy data for book list
        sample_books = [
            Book(1, "Book1", "Author1", 10.99, 5),
            Book(2, "Book2", "Author2", 12.99, 2),
            Book(3, "Book3", "Author3", 15.99, 8),
        ]
        for book in sample_books:
            self.books.append(book)

    def update_book_list(self):
        self.book_list.delete(0, tk.END)
        for book in self.books:
            self.book_list.insert(tk.END, f"{book.title} by {book.author} - ${book.price} (Qty: {book.count})")

    def search_books(self, event):
        search_term = self.search_entry.get().lower()
        filtered_books = [book for book in self.books if search_term in book.title.lower() or search_term in book.author.lower()]
        self.book_list.delete(0, tk.END)
        for book in filtered_books:
            self.book_list.insert(tk.END, f"{book.title} by {book.author} - ${book.price} (Qty: {book.count})")


if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreGUI(root)
    root.mainloop()
