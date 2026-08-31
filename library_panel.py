from ui_theme import apply_theme
from tkinter import Tk, Label, Entry, Button, Toplevel, messagebox, Frame
from tkinter.ttk import Treeview, Combobox
from tkinter import LabelFrame
from DataAccess.book_data_access import get_book_list, insert_book, update_book, delete_book, get_book_by_id
from DataAccess.author_data_access import get_author_list, insert_author, update_author, delete_author, get_author_by_id
from DataAccess.publisher_data_access import get_publisher_list, insert_publisher, update_publisher, delete_publisher, get_publisher_by_id
from DataAccess.genre_data_access import get_genre_list, insert_genre, update_genre, delete_genre, get_genre_by_id
from DataAccess.translator_data_access import get_translator_list, insert_translator, update_translator, delete_translator, get_translator_by_id
from datetime import datetime

class LibraryPanel:
    def __init__(self, username=None, role=None):
        self.window = Tk()
        apply_theme(self.window)
        self.window.title("Library Management")
        self.window.geometry("1200x700")
        self.window.configure(bg="#F0F5E8")
        self.username = username
        self.role = role

        self.primary_color = "#556B2F"
        self.primary_dark = "#3D4F23"
        self.primary_light = "#6B8E23"
        self.success_color = "#4A7A2E"
        self.warning_color = "#B8860B"
        self.danger_color = "#8B3A3A"
        self.bg_color = "#F0F5E8"
        self.card_color = "#FAFCF7"
        self.text_color = "#2C3A1A"
        self.text_secondary = "#7A8C5A"
        self.header_color = "#556B2F"

        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        header = Frame(self.window, bg=self.header_color, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        Button(header, text="← Back to Dashboard",
               font=("Segoe UI", 11, "bold"),
               bg=self.header_color, fg="white", relief="flat",
               cursor="hand2", command=self.back_to_dashboard).pack(side="left", padx=20, pady=15)

        Label(header, text="📚 Library Management",
              font=("Segoe UI", 16, "bold"), bg=self.header_color, fg="white").pack(side="left", padx=20)

        Label(header, text=f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
              font=("Segoe UI", 11), bg=self.header_color, fg="#D4E8C4").pack(side="right", padx=20)

        main_frame = Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        notebook_frame = Frame(main_frame, bg=self.bg_color)
        notebook_frame.pack(fill="both", expand=True)

        button_frame = Frame(notebook_frame, bg=self.bg_color)
        button_frame.pack(fill="x", pady=5)

        self.books_btn = Button(button_frame, text="📚 Books", command=self.show_books_tab,
                                bg=self.primary_color, fg="white", font=("Segoe UI", 10, "bold"),
                                relief="flat", padx=20, pady=6, cursor="hand2")
        self.books_btn.pack(side="left", padx=2)

        self.authors_btn = Button(button_frame, text="✍️ Authors", command=self.show_authors_tab,
                                  bg=self.primary_light, fg="white", font=("Segoe UI", 10, "bold"),
                                  relief="flat", padx=20, pady=6, cursor="hand2")
        self.authors_btn.pack(side="left", padx=2)

        self.publishers_btn = Button(button_frame, text="🏢 Publishers", command=self.show_publishers_tab,
                                     bg=self.primary_light, fg="white", font=("Segoe UI", 10, "bold"),
                                     relief="flat", padx=20, pady=6, cursor="hand2")
        self.publishers_btn.pack(side="left", padx=2)

        self.genres_btn = Button(button_frame, text="🏷️ Genres", command=self.show_genres_tab,
                                 bg=self.primary_light, fg="white", font=("Segoe UI", 10, "bold"),
                                 relief="flat", padx=20, pady=6, cursor="hand2")
        self.genres_btn.pack(side="left", padx=2)

        self.translators_btn = Button(button_frame, text="🌐 Translators", command=self.show_translators_tab,
                                      bg=self.primary_light, fg="white", font=("Segoe UI", 10, "bold"),
                                      relief="flat", padx=20, pady=6, cursor="hand2")
        self.translators_btn.pack(side="left", padx=2)

        self.content_frame = Frame(notebook_frame, bg=self.card_color, relief="ridge", bd=2)
        self.content_frame.pack(fill="both", expand=True, pady=5)

        self.current_tab = "books"
        self.show_books_tab()

        self.window.mainloop()

    def back_to_dashboard(self):
        self.window.destroy()
        import dashboard
        dashboard.run_dashboard(self.username, self.role)

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def validate_phone(self, phone):
        phone = phone.replace(" ", "").replace("-", "")
        return len(phone) == 11 and phone.isdigit()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_tab_buttons(self, active_tab):
        buttons = {
            "books": self.books_btn,
            "authors": self.authors_btn,
            "publishers": self.publishers_btn,
            "genres": self.genres_btn,
            "translators": self.translators_btn
        }
        for tab, btn in buttons.items():
            if tab == active_tab:
                btn.config(bg=self.primary_color)
            else:
                btn.config(bg=self.primary_light)

    def show_books_tab(self):
        self.clear_content()
        self.current_tab = "books"
        self.update_tab_buttons("books")
        self.create_books_tab()

    def show_authors_tab(self):
        self.clear_content()
        self.current_tab = "authors"
        self.update_tab_buttons("authors")
        self.create_authors_tab()

    def show_publishers_tab(self):
        self.clear_content()
        self.current_tab = "publishers"
        self.update_tab_buttons("publishers")
        self.create_publishers_tab()

    def show_genres_tab(self):
        self.clear_content()
        self.current_tab = "genres"
        self.update_tab_buttons("genres")
        self.create_genres_tab()

    def show_translators_tab(self):
        self.clear_content()
        self.current_tab = "translators"
        self.update_tab_buttons("translators")
        self.create_translators_tab()

    def create_books_tab(self):
        main_frame = Frame(self.content_frame, bg=self.card_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        search_frame = Frame(main_frame, bg=self.card_color)
        search_frame.pack(fill="x", pady=5)

        Label(search_frame, text="Search:", font=("Segoe UI", 11, "bold"),
              bg=self.card_color, fg=self.text_color).pack(side="left", padx=10)

        self.book_search_entry = Entry(search_frame, font=("Segoe UI", 11), width=40,
                                       bg="#F0F5E8", relief="solid", bd=1)
        self.book_search_entry.pack(side="left", padx=10)
        self.book_search_entry.bind('<Return>', self.search_books)

        Button(search_frame, text="🔍 Search", command=self.search_books,
               bg=self.primary_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=5, cursor="hand2").pack(side="left", padx=5)

        Button(search_frame, text="🔄 Show All", command=self.load_books_treeview,
               bg=self.primary_light, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=5, cursor="hand2").pack(side="left", padx=5)

        btn_frame = Frame(main_frame, bg=self.card_color)
        btn_frame.pack(fill="x", pady=5)

        Button(btn_frame, text="➕ Create Book", command=self.show_book_form,
               bg=self.success_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="✏️ Edit Book", command=self.edit_book,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="🗑️ Delete Book", command=self.delete_book,
               bg=self.danger_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        tree_frame = Frame(main_frame, bg="white", relief="solid", bd=1)
        tree_frame.pack(fill="both", expand=True, pady=5)

        from tkinter import Scrollbar
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")

        self.book_treeview = Treeview(
            tree_frame,
            columns=("id", "title", "isbn", "price", "purchase_price", "stock", "profit", "author", "publisher", "year", "edition"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.book_treeview.yview)

        self.book_treeview.heading("id", text="ID")
        self.book_treeview.heading("title", text="Title")
        self.book_treeview.heading("isbn", text="ISBN")
        self.book_treeview.heading("price", text="Sell Price")
        self.book_treeview.heading("purchase_price", text="Buy Price")
        self.book_treeview.heading("stock", text="Stock")
        self.book_treeview.heading("profit", text="Profit")
        self.book_treeview.heading("author", text="Author")
        self.book_treeview.heading("publisher", text="Publisher")
        self.book_treeview.heading("year", text="Year")
        self.book_treeview.heading("edition", text="Edition")

        self.book_treeview.column("id", width=50)
        self.book_treeview.column("title", width=180)
        self.book_treeview.column("isbn", width=120)
        self.book_treeview.column("price", width=90)
        self.book_treeview.column("purchase_price", width=90)
        self.book_treeview.column("stock", width=60)
        self.book_treeview.column("profit", width=90)
        self.book_treeview.column("author", width=120)
        self.book_treeview.column("publisher", width=120)
        self.book_treeview.column("year", width=60)
        self.book_treeview.column("edition", width=60)

        self.book_treeview.pack(fill="both", expand=True, padx=5, pady=5)

        self.load_books_treeview()

    def load_books_treeview(self):
        for child in self.book_treeview.get_children():
            self.book_treeview.delete(child)

        search_term = self.book_search_entry.get().strip() if hasattr(self, 'book_search_entry') else ""
        book_list = get_book_list(search_term)

        for book in book_list:
            self.book_treeview.insert(
                "",
                "end",
                iid=book.id,
                values=(
                    book.id,
                    book.title,
                    book.isbn or "-",
                    f"{book.price:,.0f}" if book.price else "0",
                    f"{book.purchase_price:,.0f}" if book.purchase_price else "0",
                    book.stock,
                    f"{book.profit:,.0f}" if book.profit else "0",
                    book.author.get_fullname(),
                    book.publisher.title,
                    book.publication_year or "-",
                    book.edition_number or "1"
                )
            )

    def search_books(self, event=None):
        self.load_books_treeview()

    def show_book_form(self, book_id=None):
        book_form = Toplevel(self.window)
        book_form.title("Edit Book" if book_id else "Create New Book")
        book_form.geometry("750x820")
        book_form.configure(bg="#F0F5E8")
        book_form.transient(self.window)
        book_form.grab_set()

        self.center_window(book_form)

        widgets = {}

        header_frame = Frame(book_form, bg=self.primary_color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        Label(header_frame, text="📝 Edit Book" if book_id else "📝 Create New Book",
              font=("Segoe UI", 14, "bold"), bg=self.primary_color, fg="white").pack(pady=12)

        form_frame = Frame(book_form, bg=self.card_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        row = 0

        Label(form_frame, text="Title:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        widgets['title'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                 bg="#F0F5E8", relief="solid", bd=1)
        widgets['title'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="ISBN:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        widgets['isbn'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                bg="#F0F5E8", relief="solid", bd=1)
        widgets['isbn'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Author:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        author_data = [(a.id, a.get_information()) for a in get_author_list()]
        widgets['author'] = Combobox(form_frame, values=[a[1] for a in author_data],
                                     state="readonly", font=("Segoe UI", 11), width=40)
        widgets['author'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Publisher:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        publisher_data = [(p.id, p.get_information()) for p in get_publisher_list()]
        widgets['publisher'] = Combobox(form_frame, values=[p[1] for p in publisher_data],
                                        state="readonly", font=("Segoe UI", 11), width=40)
        widgets['publisher'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Translator (Optional):", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        translator_data = [(t.id, t.get_information()) for t in get_translator_list()]
        translator_values = ["No Translator"] + [t[1] for t in translator_data]
        widgets['translator'] = Combobox(form_frame, values=translator_values,
                                         state="readonly", font=("Segoe UI", 11), width=40)
        widgets['translator'].set("No Translator")
        widgets['translator'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Genre (Optional):", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        genre_data = [(g.id, g.name) for g in get_genre_list()]
        genre_values = ["No Genre"] + [g[1] for g in genre_data]
        widgets['genre'] = Combobox(form_frame, values=genre_values,
                                    state="readonly", font=("Segoe UI", 11), width=40)
        widgets['genre'].set("No Genre")
        widgets['genre'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Publication Year:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        widgets['publication_year'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                            bg="#F0F5E8", relief="solid", bd=1)
        widgets['publication_year'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Edition Number:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        widgets['edition_number'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                          bg="#F0F5E8", relief="solid", bd=1)
        widgets['edition_number'].insert(0, "1")
        widgets['edition_number'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Purchase Price:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        widgets['purchase_price'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                          bg="#F0F5E8", relief="solid", bd=1)
        widgets['purchase_price'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Selling Price:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        widgets['price'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                 bg="#F0F5E8", relief="solid", bd=1)
        widgets['price'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        Label(form_frame, text="Stock:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=row, column=0, pady=5, padx=10, sticky="e")
        widgets['stock'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                 bg="#F0F5E8", relief="solid", bd=1)
        widgets['stock'].insert(0, "0")
        widgets['stock'].grid(row=row, column=1, pady=5, padx=10, sticky="w")
        row += 1

        profit_frame = LabelFrame(form_frame, text="💰 Profit Calculation",
                                  fg=self.primary_color, font=("Segoe UI", 10, "bold"))
        profit_frame.grid(row=row, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

        widgets['profit_display'] = Label(profit_frame, text="Profit: 0 USD (0%)",
                                          font=("Segoe UI", 12, "bold"), fg=self.text_color)
        widgets['profit_display'].pack(pady=5)

        def calculate_profit(event=None):
            try:
                purchase = float(widgets['purchase_price'].get()) if widgets['purchase_price'].get() else 0
                sell = float(widgets['price'].get()) if widgets['price'].get() else 0
                profit = sell - purchase
                if purchase > 0:
                    percentage = round((profit / purchase) * 100, 1)
                    widgets['profit_display'].config(
                        text=f"Profit: {profit:,.2f} USD ({percentage}%)",
                        fg=self.success_color if profit >= 0 else self.danger_color
                    )
                else:
                    widgets['profit_display'].config(text=f"Profit: {profit:,.2f} USD")
            except:
                pass

        widgets['purchase_price'].bind('<KeyRelease>', calculate_profit)
        widgets['price'].bind('<KeyRelease>', calculate_profit)

        if book_id:
            book = get_book_by_id(book_id)
            if book:
                widgets['title'].insert(0, book.title)
                widgets['isbn'].insert(0, book.isbn or "")
                widgets['author'].set(book.author.get_information())
                widgets['publisher'].set(book.publisher.get_information())

                if book.translator:
                    widgets['translator'].set(book.translator.get_information())
                else:
                    widgets['translator'].set("No Translator")

                if book.genre:
                    widgets['genre'].set(book.genre.name)
                else:
                    widgets['genre'].set("No Genre")

                widgets['publication_year'].insert(0, str(book.publication_year or ""))
                widgets['edition_number'].delete(0, 'end')
                widgets['edition_number'].insert(0, str(book.edition_number))
                widgets['purchase_price'].insert(0, str(book.purchase_price or ""))
                widgets['price'].insert(0, str(book.price or ""))
                widgets['stock'].insert(0, str(book.stock or "0"))
                calculate_profit()

        def submit_book():
            try:
                if not widgets['title'].get().strip():
                    messagebox.showerror("Error", "Title is required")
                    return

                if not widgets['author'].get():
                    messagebox.showerror("Error", "Please select an author")
                    return

                if not widgets['publisher'].get():
                    messagebox.showerror("Error", "Please select a publisher")
                    return

                author_id = int(widgets['author'].get().split('-')[0])
                publisher_id = int(widgets['publisher'].get().split('-')[0])

                translator_id = None
                if widgets['translator'].get() != "No Translator":
                    translator_id = int(widgets['translator'].get().split('-')[0])

                genre_id = None
                if widgets['genre'].get() != "No Genre":
                    for g in get_genre_list():
                        if g.name == widgets['genre'].get():
                            genre_id = g.id
                            break

                book_data = {
                    'title': widgets['title'].get().strip(),
                    'isbn': widgets['isbn'].get().strip(),
                    'price': float(widgets['price'].get()) if widgets['price'].get() else 0,
                    'purchase_price': float(widgets['purchase_price'].get()) if widgets['purchase_price'].get() else 0,
                    'stock': int(widgets['stock'].get()) if widgets['stock'].get() else 0,
                    'publication_year': int(widgets['publication_year'].get()) if widgets['publication_year'].get() else None,
                    'edition_number': int(widgets['edition_number'].get()) if widgets['edition_number'].get() else 1,
                    'author_id': author_id,
                    'publisher_id': publisher_id,
                    'genre_id': genre_id,
                    'translator_id': translator_id
                }

                if book_id:
                    update_book(book_id, book_data)
                else:
                    insert_book(book_data)

                self.load_books_treeview()
                book_form.destroy()
                messagebox.showinfo("Success", "Book saved successfully!")

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving book: {str(e)}")

        Button(book_form, text="💾 Submit", command=submit_book,
               bg=self.primary_color, fg="white", font=("Segoe UI", 12, "bold"),
               relief="flat", padx=40, pady=10, cursor="hand2").pack(pady=20)

    def edit_book(self):
        selected = self.book_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to edit")
            return
        book_id = int(selected[0])
        self.show_book_form(book_id)

    def delete_book(self):
        selected = self.book_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete selected book?"):
            for book_id in selected:
                delete_book(book_id)
            self.load_books_treeview()
            messagebox.showinfo("Success", "Book deleted successfully!")

    def create_authors_tab(self):
        main_frame = Frame(self.content_frame, bg=self.card_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = Frame(main_frame, bg=self.card_color)
        btn_frame.pack(fill="x", pady=5)

        Button(btn_frame, text="➕ Create Author", command=self.show_author_form,
               bg=self.success_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="✏️ Edit Author", command=self.edit_author,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="🗑️ Delete Author", command=self.delete_author,
               bg=self.danger_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        tree_frame = Frame(main_frame, bg="white", relief="solid", bd=1)
        tree_frame.pack(fill="both", expand=True, pady=5)

        from tkinter import Scrollbar
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")

        self.author_treeview = Treeview(
            tree_frame,
            columns=("id", "first_name", "last_name", "phone"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.author_treeview.yview)

        self.author_treeview.heading("id", text="ID")
        self.author_treeview.heading("first_name", text="First Name")
        self.author_treeview.heading("last_name", text="Last Name")
        self.author_treeview.heading("phone", text="Phone")

        self.author_treeview.column("id", width=50)
        self.author_treeview.column("first_name", width=200)
        self.author_treeview.column("last_name", width=200)
        self.author_treeview.column("phone", width=150)

        self.author_treeview.pack(fill="both", expand=True, padx=5, pady=5)

        self.load_authors_treeview()

    def load_authors_treeview(self):
        for child in self.author_treeview.get_children():
            self.author_treeview.delete(child)

        author_list = get_author_list()
        for author in author_list:
            self.author_treeview.insert(
                "",
                "end",
                iid=author.id,
                values=(
                    author.id,
                    author.first_name,
                    author.last_name,
                    author.phone or "-"
                )
            )

    def show_author_form(self, author_id=None):
        form = Toplevel(self.window)
        form.title("Edit Author" if author_id else "Create New Author")
        form.geometry("450x300")
        form.configure(bg="#F0F5E8")
        form.transient(self.window)
        form.grab_set()
        self.center_window(form)

        header_frame = Frame(form, bg=self.primary_color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        Label(header_frame, text="✍️ Edit Author" if author_id else "✍️ Create New Author",
              font=("Segoe UI", 14, "bold"), bg=self.primary_color, fg="white").pack(pady=12)

        form_frame = Frame(form, bg=self.card_color)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)

        Label(form_frame, text="First Name:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=0, column=0, pady=5, padx=10, sticky="e")
        first_name_entry = Entry(form_frame, font=("Segoe UI", 11), width=30,
                                 bg="#F0F5E8", relief="solid", bd=1)
        first_name_entry.grid(row=0, column=1, pady=5, padx=10)

        Label(form_frame, text="Last Name:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=1, column=0, pady=5, padx=10, sticky="e")
        last_name_entry = Entry(form_frame, font=("Segoe UI", 11), width=30,
                                bg="#F0F5E8", relief="solid", bd=1)
        last_name_entry.grid(row=1, column=1, pady=5, padx=10)

        Label(form_frame, text="Phone (Optional):", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=2, column=0, pady=5, padx=10, sticky="e")
        phone_entry = Entry(form_frame, font=("Segoe UI", 11), width=30,
                            bg="#F0F5E8", relief="solid", bd=1)
        phone_entry.grid(row=2, column=1, pady=5, padx=10)

        if author_id:
            author = get_author_by_id(author_id)
            if author:
                first_name_entry.insert(0, author.first_name)
                last_name_entry.insert(0, author.last_name)
                if author.phone:
                    phone_entry.insert(0, author.phone)

        def submit():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            phone = phone_entry.get().strip()

            if not first_name or not last_name:
                messagebox.showerror("Error", "First name and last name are required")
                return

            if phone and not self.validate_phone(phone):
                messagebox.showerror("Error", "Phone must be 11 digits")
                return

            if author_id:
                update_author(author_id, first_name, last_name, phone if phone else None)
            else:
                insert_author(first_name, last_name, phone if phone else None)

            self.load_authors_treeview()
            form.destroy()
            messagebox.showinfo("Success", "Author saved successfully!")

        Button(form_frame, text="💾 Submit", command=submit,
               bg=self.primary_color, fg="white", font=("Segoe UI", 11, "bold"),
               relief="flat", padx=30, pady=8, cursor="hand2").grid(row=3, column=0, columnspan=2, pady=20)

    def edit_author(self):
        selected = self.author_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an author to edit")
            return
        author_id = int(selected[0])
        self.show_author_form(author_id)

    def delete_author(self):
        selected = self.author_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an author to delete")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete selected author?"):
            for author_id in selected:
                delete_author(author_id)
            self.load_authors_treeview()
            messagebox.showinfo("Success", "Author deleted successfully!")

    def create_publishers_tab(self):
        main_frame = Frame(self.content_frame, bg=self.card_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = Frame(main_frame, bg=self.card_color)
        btn_frame.pack(fill="x", pady=5)

        Button(btn_frame, text="➕ Create Publisher", command=self.show_publisher_form,
               bg=self.success_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="✏️ Edit Publisher", command=self.edit_publisher,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="🗑️ Delete Publisher", command=self.delete_publisher,
               bg=self.danger_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        tree_frame = Frame(main_frame, bg="white", relief="solid", bd=1)
        tree_frame.pack(fill="both", expand=True, pady=5)

        from tkinter import Scrollbar
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")

        self.publisher_treeview = Treeview(
            tree_frame,
            columns=("id", "title"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.publisher_treeview.yview)

        self.publisher_treeview.heading("id", text="ID")
        self.publisher_treeview.heading("title", text="Publisher Name")

        self.publisher_treeview.column("id", width=50)
        self.publisher_treeview.column("title", width=400)

        self.publisher_treeview.pack(fill="both", expand=True, padx=5, pady=5)

        self.load_publishers_treeview()

    def load_publishers_treeview(self):
        for child in self.publisher_treeview.get_children():
            self.publisher_treeview.delete(child)

        publisher_list = get_publisher_list()
        for publisher in publisher_list:
            self.publisher_treeview.insert(
                "",
                "end",
                iid=publisher.id,
                values=(publisher.id, publisher.title)
            )

    def show_publisher_form(self, publisher_id=None):
        form = Toplevel(self.window)
        form.title("Edit Publisher" if publisher_id else "Create New Publisher")
        form.geometry("450x200")
        form.configure(bg="#F0F5E8")
        form.transient(self.window)
        form.grab_set()
        self.center_window(form)

        header_frame = Frame(form, bg=self.primary_color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        Label(header_frame, text="🏢 Edit Publisher" if publisher_id else "🏢 Create New Publisher",
              font=("Segoe UI", 14, "bold"), bg=self.primary_color, fg="white").pack(pady=12)

        form_frame = Frame(form, bg=self.card_color)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)

        Label(form_frame, text="Publisher Name:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=0, column=0, pady=5, padx=10, sticky="e")
        title_entry = Entry(form_frame, font=("Segoe UI", 11), width=30,
                            bg="#F0F5E8", relief="solid", bd=1)
        title_entry.grid(row=0, column=1, pady=5, padx=10)

        if publisher_id:
            publisher = get_publisher_by_id(publisher_id)
            if publisher:
                title_entry.insert(0, publisher.title)

        def submit():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("Error", "Publisher name is required")
                return

            if publisher_id:
                update_publisher(publisher_id, title)
            else:
                insert_publisher(title)

            self.load_publishers_treeview()
            form.destroy()
            messagebox.showinfo("Success", "Publisher saved successfully!")

        Button(form_frame, text="💾 Submit", command=submit,
               bg=self.primary_color, fg="white", font=("Segoe UI", 11, "bold"),
               relief="flat", padx=30, pady=8, cursor="hand2").grid(row=1, column=0, columnspan=2, pady=20)

    def edit_publisher(self):
        selected = self.publisher_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a publisher to edit")
            return
        publisher_id = int(selected[0])
        self.show_publisher_form(publisher_id)

    def delete_publisher(self):
        selected = self.publisher_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a publisher to delete")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete selected publisher?"):
            for publisher_id in selected:
                delete_publisher(publisher_id)
            self.load_publishers_treeview()
            messagebox.showinfo("Success", "Publisher deleted successfully!")

    def create_genres_tab(self):
        main_frame = Frame(self.content_frame, bg=self.card_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = Frame(main_frame, bg=self.card_color)
        btn_frame.pack(fill="x", pady=5)

        Button(btn_frame, text="➕ Create Genre", command=self.show_genre_form,
               bg=self.success_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="✏️ Edit Genre", command=self.edit_genre,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="🗑️ Delete Genre", command=self.delete_genre,
               bg=self.danger_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        tree_frame = Frame(main_frame, bg="white", relief="solid", bd=1)
        tree_frame.pack(fill="both", expand=True, pady=5)

        from tkinter import Scrollbar
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")

        self.genre_treeview = Treeview(
            tree_frame,
            columns=("id", "name"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.genre_treeview.yview)

        self.genre_treeview.heading("id", text="ID")
        self.genre_treeview.heading("name", text="Genre Name")

        self.genre_treeview.column("id", width=50)
        self.genre_treeview.column("name", width=400)

        self.genre_treeview.pack(fill="both", expand=True, padx=5, pady=5)

        self.load_genres_treeview()

    def load_genres_treeview(self):
        for child in self.genre_treeview.get_children():
            self.genre_treeview.delete(child)

        genre_list = get_genre_list()
        for genre in genre_list:
            self.genre_treeview.insert(
                "",
                "end",
                iid=genre.id,
                values=(genre.id, genre.name)
            )

    def show_genre_form(self, genre_id=None):
        form = Toplevel(self.window)
        form.title("Edit Genre" if genre_id else "Create New Genre")
        form.geometry("450x200")
        form.configure(bg="#F0F5E8")
        form.transient(self.window)
        form.grab_set()
        self.center_window(form)

        header_frame = Frame(form, bg=self.primary_color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        Label(header_frame, text="🏷️ Edit Genre" if genre_id else "🏷️ Create New Genre",
              font=("Segoe UI", 14, "bold"), bg=self.primary_color, fg="white").pack(pady=12)

        form_frame = Frame(form, bg=self.card_color)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)

        Label(form_frame, text="Genre Name:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=0, column=0, pady=5, padx=10, sticky="e")
        name_entry = Entry(form_frame, font=("Segoe UI", 11), width=30,
                           bg="#F0F5E8", relief="solid", bd=1)
        name_entry.grid(row=0, column=1, pady=5, padx=10)

        if genre_id:
            genre = get_genre_by_id(genre_id)
            if genre:
                name_entry.insert(0, genre.name)

        def submit():
            name = name_entry.get().strip()
            if not name:
                messagebox.showerror("Error", "Genre name is required")
                return

            if genre_id:
                update_genre(genre_id, name)
            else:
                insert_genre(name)

            self.load_genres_treeview()
            form.destroy()
            messagebox.showinfo("Success", "Genre saved successfully!")

        Button(form_frame, text="💾 Submit", command=submit,
               bg=self.primary_color, fg="white", font=("Segoe UI", 11, "bold"),
               relief="flat", padx=30, pady=8, cursor="hand2").grid(row=1, column=0, columnspan=2, pady=20)

    def edit_genre(self):
        selected = self.genre_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a genre to edit")
            return
        genre_id = int(selected[0])
        self.show_genre_form(genre_id)

    def delete_genre(self):
        selected = self.genre_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a genre to delete")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete selected genre?"):
            for genre_id in selected:
                delete_genre(genre_id)
            self.load_genres_treeview()
            messagebox.showinfo("Success", "Genre deleted successfully!")

    def create_translators_tab(self):
        main_frame = Frame(self.content_frame, bg=self.card_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = Frame(main_frame, bg=self.card_color)
        btn_frame.pack(fill="x", pady=5)

        Button(btn_frame, text="➕ Create Translator", command=self.show_translator_form,
               bg=self.success_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="✏️ Edit Translator", command=self.edit_translator,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="🗑️ Delete Translator", command=self.delete_translator,
               bg=self.danger_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        tree_frame = Frame(main_frame, bg="white", relief="solid", bd=1)
        tree_frame.pack(fill="both", expand=True, pady=5)

        from tkinter import Scrollbar
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")

        self.translator_treeview = Treeview(
            tree_frame,
            columns=("id", "first_name", "last_name", "phone"),
            show="headings",
            yscrollcommand=scroll_y.set
        )
        scroll_y.config(command=self.translator_treeview.yview)

        self.translator_treeview.heading("id", text="ID")
        self.translator_treeview.heading("first_name", text="First Name")
        self.translator_treeview.heading("last_name", text="Last Name")
        self.translator_treeview.heading("phone", text="Phone")

        self.translator_treeview.column("id", width=50)
        self.translator_treeview.column("first_name", width=200)
        self.translator_treeview.column("last_name", width=200)
        self.translator_treeview.column("phone", width=150)

        self.translator_treeview.pack(fill="both", expand=True, padx=5, pady=5)

        self.load_translators_treeview()

    def load_translators_treeview(self):
        for child in self.translator_treeview.get_children():
            self.translator_treeview.delete(child)

        translator_list = get_translator_list()
        for translator in translator_list:
            self.translator_treeview.insert(
                "",
                "end",
                iid=translator.id,
                values=(
                    translator.id,
                    translator.first_name,
                    translator.last_name,
                    translator.phone or "-"
                )
            )

    def show_translator_form(self, translator_id=None):
        form = Toplevel(self.window)
        form.title("Edit Translator" if translator_id else "Create New Translator")
        form.geometry("450x300")
        form.configure(bg="#F0F5E8")
        form.transient(self.window)
        form.grab_set()
        self.center_window(form)

        header_frame = Frame(form, bg=self.primary_color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        Label(header_frame, text="🌐 Edit Translator" if translator_id else "🌐 Create New Translator",
              font=("Segoe UI", 14, "bold"), bg=self.primary_color, fg="white").pack(pady=12)

        form_frame = Frame(form, bg=self.card_color)
        form_frame.pack(pady=20, padx=30, fill="both", expand=True)

        Label(form_frame, text="First Name:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=0, column=0, pady=5, padx=10, sticky="e")
        first_name_entry = Entry(form_frame, font=("Segoe UI", 11), width=30,
                                 bg="#F0F5E8", relief="solid", bd=1)
        first_name_entry.grid(row=0, column=1, pady=5, padx=10)

        Label(form_frame, text="Last Name:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=1, column=0, pady=5, padx=10, sticky="e")
        last_name_entry = Entry(form_frame, font=("Segoe UI", 11), width=30,
                                bg="#F0F5E8", relief="solid", bd=1)
        last_name_entry.grid(row=1, column=1, pady=5, padx=10)

        Label(form_frame, text="Phone (Optional):", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=2, column=0, pady=5, padx=10, sticky="e")
        phone_entry = Entry(form_frame, font=("Segoe UI", 11), width=30,
                            bg="#F0F5E8", relief="solid", bd=1)
        phone_entry.grid(row=2, column=1, pady=5, padx=10)

        if translator_id:
            translator = get_translator_by_id(translator_id)
            if translator:
                first_name_entry.insert(0, translator.first_name)
                last_name_entry.insert(0, translator.last_name)
                if translator.phone:
                    phone_entry.insert(0, translator.phone)

        def submit():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            phone = phone_entry.get().strip()

            if not first_name or not last_name:
                messagebox.showerror("Error", "First name and last name are required")
                return

            if phone and not self.validate_phone(phone):
                messagebox.showerror("Error", "Phone must be 11 digits")
                return

            if translator_id:
                update_translator(translator_id, first_name, last_name, phone if phone else None)
            else:
                insert_translator(first_name, last_name, phone if phone else None)

            self.load_translators_treeview()
            form.destroy()
            messagebox.showinfo("Success", "Translator saved successfully!")

        Button(form_frame, text="💾 Submit", command=submit,
               bg=self.primary_color, fg="white", font=("Segoe UI", 11, "bold"),
               relief="flat", padx=30, pady=8, cursor="hand2").grid(row=3, column=0, columnspan=2, pady=20)

    def edit_translator(self):
        selected = self.translator_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a translator to edit")
            return
        translator_id = int(selected[0])
        self.show_translator_form(translator_id)

    def delete_translator(self):
        selected = self.translator_treeview.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a translator to delete")
            return
        if messagebox.askyesno("Confirm", "Are you sure you want to delete selected translator?"):
            for translator_id in selected:
                delete_translator(translator_id)
            self.load_translators_treeview()
            messagebox.showinfo("Success", "Translator deleted successfully!")

def run_library_panel(username=None, role=None):
    LibraryPanel(username, role)

if __name__ == "__main__":
    run_library_panel()