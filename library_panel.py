from ui_theme import apply_theme
from tkinter import Tk, Label, Entry, Button, Toplevel, messagebox, Frame, Scrollbar
from tkinter.ttk import Treeview, Combobox
from tkinter import LabelFrame
from DataAccess.book_data_access import get_book_list, insert_book, update_book, delete_book, get_book_by_id
from DataAccess.author_data_access import get_author_list, insert_author, update_author, delete_author
from DataAccess.publisher_data_access import get_publisher_list, insert_publisher, update_publisher, delete_publisher
from DataAccess.genre_data_access import get_genre_list, insert_genre, update_genre, delete_genre
from DataAccess.translator_data_access import get_translator_list, insert_translator, update_translator, delete_translator
from datetime import datetime

class LibraryPanel:
    def __init__(self, username=None, role=None):
        self.window = Tk()
        apply_theme(self.window)
        self.window.title("Mehrad's Book Shop - Library Management")
        self.window.geometry("1300x750")
        self.window.configure(bg="#F0F5E8")
        self.username = username
        self.role = role

        self.primary_color = "#556B2F"
        self.primary_dark = "#3D4F23"
        self.primary_light = "#6B8E23"
        self.secondary_color = "#6B8E23"
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

        self.selected_row = None
        self.details_text = None

        self.create_header()

        main_frame = Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tree_frame = Frame(main_frame, bg=self.card_color, relief="solid", bd=1)
        tree_frame.pack(side="left", fill="both", expand=True)

        tree_container = Frame(tree_frame, bg=self.card_color)
        tree_container.pack(fill="both", expand=True, padx=5, pady=5)

        scroll_y = Scrollbar(tree_container)
        scroll_y.pack(side="right", fill="y")

        scroll_x = Scrollbar(tree_container, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        self.tree = Treeview(tree_container, columns=("id", "title", "isbn", "price", "stock", "genre", "author", "publisher"),
                             show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("isbn", text="ISBN")
        self.tree.heading("price", text="Price")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("genre", text="Genre")
        self.tree.heading("author", text="Author")
        self.tree.heading("publisher", text="Publisher")

        self.tree.column("id", width=50)
        self.tree.column("title", width=180)
        self.tree.column("isbn", width=120)
        self.tree.column("price", width=100)
        self.tree.column("stock", width=60)
        self.tree.column("genre", width=100)
        self.tree.column("author", width=150)
        self.tree.column("publisher", width=150)

        self.tree.pack(fill="both", expand=True)

        right_frame = Frame(main_frame, bg=self.bg_color, width=350)
        right_frame.pack(side="right", fill="y", padx=(10, 0))
        right_frame.pack_propagate(False)

        details_panel = Frame(right_frame, bg=self.card_color, relief="solid", bd=1)
        details_panel.pack(fill="x", pady=(0, 10))

        Label(details_panel, text="📋 Book Details", font=("Segoe UI", 12, "bold"),
              bg=self.card_color, fg=self.text_color).pack(pady=10)

        self.details_text = Label(details_panel, text="Select a book to view details",
                                  font=("Segoe UI", 10), bg=self.card_color, fg=self.text_secondary,
                                  wraplength=300, justify="left")
        self.details_text.pack(pady=10, padx=10)

        btn_frame = Frame(right_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=5)

        Button(btn_frame, text="➕ Add Book", command=self.show_book_form,
               bg=self.success_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=10, pady=8, cursor="hand2").pack(fill="x", pady=2)

        Button(btn_frame, text="✏️ Edit Book", command=self.update_book,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=10, pady=8, cursor="hand2").pack(fill="x", pady=2)

        Button(btn_frame, text="🗑️ Delete Book", command=self.delete_book,
               bg=self.danger_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=10, pady=8, cursor="hand2").pack(fill="x", pady=2)

        Button(btn_frame, text="🔄 Refresh", command=self.load_books,
               bg=self.primary_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=10, pady=8, cursor="hand2").pack(fill="x", pady=2)

        search_frame = Frame(right_frame, bg=self.card_color, relief="solid", bd=1)
        search_frame.pack(fill="x", pady=10)

        Label(search_frame, text="🔍 Search", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).pack(pady=5)

        self.search_entry = Entry(search_frame, font=("Segoe UI", 11),
                                  bg="#F0F5E8", fg=self.text_color,
                                  relief="solid", bd=1)
        self.search_entry.pack(fill="x", padx=10, pady=5)
        self.search_entry.bind('<Return>', lambda e: self.load_books())

        Button(search_frame, text="Search", command=self.load_books,
               bg=self.primary_color, fg="white", font=("Segoe UI", 10),
               relief="flat", padx=10, pady=5, cursor="hand2").pack(pady=5)

        manage_btn = Button(right_frame, text="⚙️ Manage Authors, Publishers,\nTranslators & Genres",
                            command=self.show_manage_window,
                            bg=self.secondary_color, fg="white", font=("Segoe UI", 10, "bold"),
                            relief="flat", padx=10, pady=10, cursor="hand2")
        manage_btn.pack(fill="x", pady=10)

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        self.load_books()

        self.window.mainloop()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_header(self):
        header = Frame(self.window, bg=self.primary_color, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        Button(header, text="← Back to Dashboard",
               font=("Segoe UI", 11, "bold"),
               bg=self.primary_color, fg="white", relief="flat",
               cursor="hand2", command=self.back_to_dashboard).pack(side="left", padx=20, pady=15)

        Label(header, text="📚 Mehrad's Book Shop - Library",
              font=("Segoe UI", 16, "bold"), bg=self.primary_color, fg="white").pack(side="left", padx=20)

        Label(header, text=f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
              font=("Segoe UI", 11), bg=self.primary_color, fg="#D4E8C4").pack(side="right", padx=20)

    def back_to_dashboard(self):
        self.window.destroy()
        import dashboard
        dashboard.run_dashboard(self.username, self.role)

    def load_books(self, search_term=""):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not search_term:
            search_term = self.search_entry.get().strip()

        books = get_book_list(search_term)

        for book in books:
            genre_name = book.genre.name if book.genre else "-"
            self.tree.insert("", "end", iid=book.id, values=(
                book.id,
                book.title,
                book.isbn or "-",
                f"${book.price:,.2f}" if book.price else "$0.00",
                book.stock,
                genre_name,
                book.author.get_fullname(),
                book.publisher.title
            ))

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            if values:
                details = f"""ID: {values[0]}
Title: {values[1]}
ISBN: {values[2]}
Price: {values[3]}
Stock: {values[4]}
Genre: {values[5]}
Author: {values[6]}
Publisher: {values[7]}"""
                self.details_text.config(text=details, fg=self.text_color)
                self.selected_row = values
        else:
            self.details_text.config(text="Select a book to view details", fg=self.text_secondary)
            self.selected_row = None

    def validate_phone(self, phone):
        if phone:
            phone = phone.replace(" ", "").replace("-", "")
            return len(phone) == 11 and phone.isdigit()
        return True

    def show_book_form(self, book_id=None):
        book_form = Toplevel(self.window)
        book_form.title("Update Book" if book_id else "Add New Book")
        book_form.geometry("750x850")
        book_form.configure(bg="#F0F5E8")
        book_form.transient(self.window)
        book_form.grab_set()

        self.center_window(book_form)

        widgets = {}

        header_frame = Frame(book_form, bg=self.primary_color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        Label(header_frame, text="📝 Add New Book" if not book_id else "✏️ Edit Book",
              font=("Segoe UI", 14, "bold"), bg=self.primary_color, fg="white").pack(pady=12)

        form_frame = Frame(book_form, bg=self.card_color)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)

        Label(form_frame, text="Title:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=0, column=0, pady=5, padx=10, sticky="e")
        widgets['title'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                 bg="#F0F5E8", relief="solid", bd=1)
        widgets['title'].grid(row=0, column=1, pady=5, padx=10, sticky="w")

        Label(form_frame, text="ISBN:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=1, column=0, pady=5, padx=10, sticky="e")
        widgets['isbn'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                bg="#F0F5E8", relief="solid", bd=1)
        widgets['isbn'].grid(row=1, column=1, pady=5, padx=10, sticky="w")

        Label(form_frame, text="Author:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=2, column=0, pady=5, padx=10, sticky="e")
        author_data = [(a.id, a.get_information()) for a in get_author_list()]
        widgets['author'] = Combobox(form_frame, values=[a[1] for a in author_data],
                                     state="readonly", font=("Segoe UI", 11), width=40)
        widgets['author'].grid(row=2, column=1, pady=5, padx=10, sticky="w")

        def add_new_author():
            add_form = Toplevel(book_form)
            add_form.title("Add New Author")
            add_form.geometry("400x280")
            add_form.configure(bg="#F0F5E8")
            add_form.transient(book_form)
            add_form.grab_set()
            self.center_window(add_form)

            Label(add_form, text="First Name:", font=("Segoe UI", 10),
                  bg=self.card_color).grid(row=0, column=0, pady=5, padx=10)
            first_name_entry = Entry(add_form, font=("Segoe UI", 11), width=30,
                                     bg="#F0F5E8", relief="solid", bd=1)
            first_name_entry.grid(row=0, column=1, pady=5, padx=10)

            Label(add_form, text="Last Name:", font=("Segoe UI", 10),
                  bg=self.card_color).grid(row=1, column=0, pady=5, padx=10)
            last_name_entry = Entry(add_form, font=("Segoe UI", 11), width=30,
                                    bg="#F0F5E8", relief="solid", bd=1)
            last_name_entry.grid(row=1, column=1, pady=5, padx=10)

            Label(add_form, text="Phone (Optional):", font=("Segoe UI", 10),
                  bg=self.card_color).grid(row=2, column=0, pady=5, padx=10)
            phone_entry = Entry(add_form, font=("Segoe UI", 11), width=30,
                                bg="#F0F5E8", relief="solid", bd=1)
            phone_entry.grid(row=2, column=1, pady=5, padx=10)

            def save_author():
                first_name = first_name_entry.get().strip()
                last_name = last_name_entry.get().strip()
                phone = phone_entry.get().strip()

                if not first_name or not last_name:
                    messagebox.showerror("Error", "First name and last name are required")
                    return

                if phone and not self.validate_phone(phone):
                    messagebox.showerror("Error", "Phone number must be exactly 11 digits")
                    return

                insert_author(first_name, last_name, phone if phone else None)
                author_data = [(a.id, a.get_information()) for a in get_author_list()]
                widgets['author']['values'] = [a[1] for a in author_data]
                widgets['author'].set(f"{author_data[-1][0]}-{first_name} {last_name}")
                add_form.destroy()
                messagebox.showinfo("Success", "Author added successfully!")

            Button(add_form, text="Save", command=save_author,
                   bg=self.success_color, fg="white", font=("Segoe UI", 10),
                   relief="flat", padx=20, pady=5).grid(row=3, column=0, columnspan=2, pady=20)
            Button(add_form, text="Cancel", command=add_form.destroy,
                   bg=self.danger_color, fg="white", font=("Segoe UI", 10),
                   relief="flat", padx=20, pady=5).grid(row=4, column=0, columnspan=2)

        Button(form_frame, text="+ New Author", command=add_new_author,
               bg=self.success_color, fg="white", font=("Segoe UI", 9),
               relief="flat", padx=10, pady=2).grid(row=2, column=2, pady=5, padx=5)

        Label(form_frame, text="Publisher:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=3, column=0, pady=5, padx=10, sticky="e")
        publisher_data = [(p.id, p.get_information()) for p in get_publisher_list()]
        widgets['publisher'] = Combobox(form_frame, values=[p[1] for p in publisher_data],
                                        state="readonly", font=("Segoe UI", 11), width=40)
        widgets['publisher'].grid(row=3, column=1, pady=5, padx=10, sticky="w")

        def add_new_publisher():
            add_form = Toplevel(book_form)
            add_form.title("Add New Publisher")
            add_form.geometry("400x150")
            add_form.configure(bg="#F0F5E8")
            add_form.transient(book_form)
            add_form.grab_set()
            self.center_window(add_form)

            Label(add_form, text="Publisher Name:", font=("Segoe UI", 10),
                  bg=self.card_color).grid(row=0, column=0, pady=5, padx=10)
            name_entry = Entry(add_form, font=("Segoe UI", 11), width=30,
                               bg="#F0F5E8", relief="solid", bd=1)
            name_entry.grid(row=0, column=1, pady=5, padx=10)

            def save_publisher():
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Publisher name is required")
                    return
                insert_publisher(name)
                publisher_data = [(p.id, p.get_information()) for p in get_publisher_list()]
                widgets['publisher']['values'] = [p[1] for p in publisher_data]
                widgets['publisher'].set(f"{publisher_data[-1][0]}-{name}")
                add_form.destroy()
                messagebox.showinfo("Success", "Publisher added successfully!")

            Button(add_form, text="Save", command=save_publisher,
                   bg=self.success_color, fg="white", font=("Segoe UI", 10),
                   relief="flat", padx=20, pady=5).grid(row=1, column=0, columnspan=2, pady=20)
            Button(add_form, text="Cancel", command=add_form.destroy,
                   bg=self.danger_color, fg="white", font=("Segoe UI", 10),
                   relief="flat", padx=20, pady=5).grid(row=2, column=0, columnspan=2)

        Button(form_frame, text="+ New Publisher", command=add_new_publisher,
               bg=self.success_color, fg="white", font=("Segoe UI", 9),
               relief="flat", padx=10, pady=2).grid(row=3, column=2, pady=5, padx=5)

        Label(form_frame, text="Translator (Optional):", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=4, column=0, pady=5, padx=10, sticky="e")
        translator_data = [(t.id, t.get_information()) for t in get_translator_list()]
        translator_values = ["No Translator"] + [t[1] for t in translator_data]
        widgets['translator'] = Combobox(form_frame, values=translator_values,
                                         state="readonly", font=("Segoe UI", 11), width=40)
        widgets['translator'].set("No Translator")
        widgets['translator'].grid(row=4, column=1, pady=5, padx=10, sticky="w")

        def add_new_translator():
            add_form = Toplevel(book_form)
            add_form.title("Add New Translator")
            add_form.geometry("400x250")
            add_form.configure(bg="#F0F5E8")
            add_form.transient(book_form)
            add_form.grab_set()
            self.center_window(add_form)

            Label(add_form, text="First Name:", font=("Segoe UI", 10),
                  bg=self.card_color).grid(row=0, column=0, pady=5, padx=10)
            first_name_entry = Entry(add_form, font=("Segoe UI", 11), width=30,
                                     bg="#F0F5E8", relief="solid", bd=1)
            first_name_entry.grid(row=0, column=1, pady=5, padx=10)

            Label(add_form, text="Last Name:", font=("Segoe UI", 10),
                  bg=self.card_color).grid(row=1, column=0, pady=5, padx=10)
            last_name_entry = Entry(add_form, font=("Segoe UI", 11), width=30,
                                    bg="#F0F5E8", relief="solid", bd=1)
            last_name_entry.grid(row=1, column=1, pady=5, padx=10)

            Label(add_form, text="Phone (Optional):", font=("Segoe UI", 10),
                  bg=self.card_color).grid(row=2, column=0, pady=5, padx=10)
            phone_entry = Entry(add_form, font=("Segoe UI", 11), width=30,
                                bg="#F0F5E8", relief="solid", bd=1)
            phone_entry.grid(row=2, column=1, pady=5, padx=10)

            def save_translator():
                first_name = first_name_entry.get().strip()
                last_name = last_name_entry.get().strip()
                phone = phone_entry.get().strip()

                if not first_name or not last_name:
                    messagebox.showerror("Error", "First name and last name are required")
                    return

                if phone and not self.validate_phone(phone):
                    messagebox.showerror("Error", "Phone number must be exactly 11 digits")
                    return

                insert_translator(first_name, last_name, phone if phone else None)
                translator_data = [(t.id, t.get_information()) for t in get_translator_list()]
                translator_values = ["No Translator"] + [t[1] for t in translator_data]
                widgets['translator']['values'] = translator_values
                widgets['translator'].set(f"{translator_data[-1][0]}-{first_name} {last_name}")
                add_form.destroy()
                messagebox.showinfo("Success", "Translator added successfully!")

            Button(add_form, text="Save", command=save_translator,
                   bg=self.success_color, fg="white", font=("Segoe UI", 10),
                   relief="flat", padx=20, pady=5).grid(row=3, column=0, columnspan=2, pady=20)
            Button(add_form, text="Cancel", command=add_form.destroy,
                   bg=self.danger_color, fg="white", font=("Segoe UI", 10),
                   relief="flat", padx=20, pady=5).grid(row=4, column=0, columnspan=2)

        Button(form_frame, text="+ New Translator", command=add_new_translator,
               bg=self.success_color, fg="white", font=("Segoe UI", 9),
               relief="flat", padx=10, pady=2).grid(row=4, column=2, pady=5, padx=5)

        Label(form_frame, text="Genre:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=5, column=0, pady=5, padx=10, sticky="e")
        genre_data = [(g.id, g.name) for g in get_genre_list()]
        genre_values = ["No Genre"] + [g[1] for g in genre_data]
        widgets['genre'] = Combobox(form_frame, values=genre_values,
                                    state="readonly", font=("Segoe UI", 11), width=40)
        widgets['genre'].set("No Genre")
        widgets['genre'].grid(row=5, column=1, pady=5, padx=10, sticky="w")

        def add_new_genre():
            add_form = Toplevel(book_form)
            add_form.title("Add New Genre")
            add_form.geometry("400x150")
            add_form.configure(bg="#F0F5E8")
            add_form.transient(book_form)
            add_form.grab_set()
            self.center_window(add_form)

            Label(add_form, text="Genre Name:", font=("Segoe UI", 10),
                  bg=self.card_color).grid(row=0, column=0, pady=5, padx=10)
            name_entry = Entry(add_form, font=("Segoe UI", 11), width=30,
                               bg="#F0F5E8", relief="solid", bd=1)
            name_entry.grid(row=0, column=1, pady=5, padx=10)

            def save_genre():
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Genre name is required")
                    return
                insert_genre(name)
                genre_data = [(g.id, g.name) for g in get_genre_list()]
                genre_values = ["No Genre"] + [g[1] for g in genre_data]
                widgets['genre']['values'] = genre_values
                widgets['genre'].set(name)
                add_form.destroy()
                messagebox.showinfo("Success", "Genre added successfully!")

            Button(add_form, text="Save", command=save_genre,
                   bg=self.success_color, fg="white", font=("Segoe UI", 10),
                   relief="flat", padx=20, pady=5).grid(row=1, column=0, columnspan=2, pady=20)
            Button(add_form, text="Cancel", command=add_form.destroy,
                   bg=self.danger_color, fg="white", font=("Segoe UI", 10),
                   relief="flat", padx=20, pady=5).grid(row=2, column=0, columnspan=2)

        Button(form_frame, text="+ New Genre", command=add_new_genre,
               bg=self.success_color, fg="white", font=("Segoe UI", 9),
               relief="flat", padx=10, pady=2).grid(row=5, column=2, pady=5, padx=5)

        Label(form_frame, text="Publication Year:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=6, column=0, pady=5, padx=10, sticky="e")
        widgets['publication_year'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                            bg="#F0F5E8", relief="solid", bd=1)
        widgets['publication_year'].grid(row=6, column=1, pady=5, padx=10, sticky="w")

        Label(form_frame, text="Edition Number:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=7, column=0, pady=5, padx=10, sticky="e")
        widgets['edition_number'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                          bg="#F0F5E8", relief="solid", bd=1)
        widgets['edition_number'].insert(0, "1")
        widgets['edition_number'].grid(row=7, column=1, pady=5, padx=10, sticky="w")

        Label(form_frame, text="Purchase Price (USD):", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=8, column=0, pady=5, padx=10, sticky="e")
        widgets['purchase_price'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                          bg="#F0F5E8", relief="solid", bd=1)
        widgets['purchase_price'].grid(row=8, column=1, pady=5, padx=10, sticky="w")

        Label(form_frame, text="Selling Price (USD):", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=9, column=0, pady=5, padx=10, sticky="e")
        widgets['price'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                 bg="#F0F5E8", relief="solid", bd=1)
        widgets['price'].grid(row=9, column=1, pady=5, padx=10, sticky="w")

        Label(form_frame, text="Stock:", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color).grid(row=10, column=0, pady=5, padx=10, sticky="e")
        widgets['stock'] = Entry(form_frame, font=("Segoe UI", 11), width=50,
                                 bg="#F0F5E8", relief="solid", bd=1)
        widgets['stock'].insert(0, "0")
        widgets['stock'].grid(row=10, column=1, pady=5, padx=10, sticky="w")

        profit_frame = LabelFrame(form_frame, text="Profit Calculation",
                                  fg=self.primary_color, font=("Segoe UI", 10, "bold"))
        profit_frame.grid(row=11, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

        widgets['profit_display'] = Label(profit_frame, text="Profit: $0.00 (0%)",
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
                        text=f"Profit: ${profit:,.2f} ({percentage}%)",
                        fg=self.success_color if profit >= 0 else self.danger_color
                    )
                else:
                    widgets['profit_display'].config(text=f"Profit: ${profit:,.2f}")
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
                if book.genre:
                    widgets['genre'].set(book.genre.name)

                widgets['publication_year'].insert(0, str(book.publication_year or ""))
                widgets['edition_number'].delete(0, 'end')
                widgets['edition_number'].insert(0, str(book.edition_number))
                widgets['purchase_price'].insert(0, str(book.purchase_price or ""))
                widgets['price'].insert(0, str(book.price or ""))
                widgets['stock'].insert(0, str(book.stock or "0"))
                calculate_profit()

        def submit_book():
            try:
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
                    'title': widgets['title'].get(),
                    'isbn': widgets['isbn'].get(),
                    'price': float(widgets['price'].get()),
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

                self.load_books()
                book_form.destroy()
                messagebox.showinfo("Success", "Book saved successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Error saving book: {str(e)}")

        Button(book_form, text="💾 Submit", command=submit_book,
               bg=self.primary_color, fg="white", font=("Segoe UI", 12, "bold"),
               relief="flat", padx=40, pady=10, cursor="hand2").pack(pady=20)

    def update_book(self):
        if not self.selected_row:
            messagebox.showwarning("Warning", "Please select a book to update")
            return
        book_id = self.selected_row[0]
        self.show_book_form(book_id)

    def delete_book(self):
        if not self.selected_row:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
            book_id = self.selected_row[0]
            delete_book(book_id)
            self.load_books()
            self.selected_row = None
            self.details_text.config(text="Select a book to view details", fg=self.text_secondary)
            messagebox.showinfo("Success", "Book deleted successfully!")

    def show_manage_window(self):
        manage_window = Toplevel(self.window)
        manage_window.title("Manage Entities")
        manage_window.geometry("1100x600")
        manage_window.configure(bg="#F0F5E8")
        manage_window.transient(self.window)
        manage_window.grab_set()

        self.center_window(manage_window)

        Label(manage_window, text="⚙️ Manage Authors, Publishers, Translators & Genres",
              font=("Segoe UI", 16, "bold"), bg="#FFFFFF", fg="#2C3A1A").pack(pady=15)

        main_frame = Frame(manage_window, bg="#FFFFFF")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        author_panel = Frame(main_frame, relief="solid", bd=1, bg="#FFFFFF")
        author_panel.pack(side="left", fill="both", expand=True, padx=5)

        Label(author_panel, text="👨‍💼 Authors", font=("Segoe UI", 12, "bold"),
              bg="#FFFFFF", fg="#556B2F").pack(pady=5)

        author_tree = Treeview(author_panel, columns=("id", "name", "phone"),
                               show="headings", height=10)
        author_tree.heading("id", text="ID")
        author_tree.heading("name", text="Name")
        author_tree.heading("phone", text="Phone")
        author_tree.column("id", width=40)
        author_tree.column("name", width=130)
        author_tree.column("phone", width=100)
        author_tree.pack(fill="both", expand=True, padx=5, pady=5)

        author_btn_frame = Frame(author_panel, bg="#FFFFFF")
        author_btn_frame.pack(pady=5)

        def refresh_authors():
            for item in author_tree.get_children():
                author_tree.delete(item)
            for author in get_author_list():
                author_tree.insert("", "end", iid=author.id, values=(author.id, author.get_fullname(), author.phone or "-"))

        def add_author():
            form = Toplevel(manage_window)
            form.title("Add Author")
            form.geometry("400x280")
            form.configure(bg="#F0F5E8")
            form.transient(manage_window)
            form.grab_set()
            self.center_window(form)

            Label(form, text="First Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
            first_name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            first_name_entry.grid(row=0, column=1, pady=5, padx=10)

            Label(form, text="Last Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
            last_name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            last_name_entry.grid(row=1, column=1, pady=5, padx=10)

            Label(form, text="Phone (Optional):", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
            phone_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            phone_entry.grid(row=2, column=1, pady=5, padx=10)

            def save():
                first_name = first_name_entry.get().strip()
                last_name = last_name_entry.get().strip()
                phone = phone_entry.get().strip()

                if not first_name or not last_name:
                    messagebox.showerror("Error", "First name and last name are required")
                    return

                if phone and not self.validate_phone(phone):
                    messagebox.showerror("Error", "Phone number must be exactly 11 digits")
                    return

                insert_author(first_name, last_name, phone if phone else None)
                refresh_authors()
                form.destroy()
                messagebox.showinfo("Success", "Author added!")

            Button(form, text="Save", command=save, bg=self.success_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=3, column=0, columnspan=2, pady=20)
            Button(form, text="Cancel", command=form.destroy, bg=self.danger_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=4, column=0, columnspan=2)

        def edit_author():
            selected = author_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an author")
                return

            item = author_tree.item(selected[0])
            values = item['values']
            if not values:
                messagebox.showerror("Error", "No data found")
                return

            author_id = values[0]

            author = None
            for a in get_author_list():
                if a.id == author_id:
                    author = a
                    break
            if not author:
                messagebox.showerror("Error", f"Author with ID {author_id} not found")
                return

            form = Toplevel(manage_window)
            form.title("Edit Author")
            form.geometry("400x280")
            form.configure(bg="#F0F5E8")
            form.transient(manage_window)
            form.grab_set()
            self.center_window(form)

            Label(form, text="First Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
            first_name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            first_name_entry.grid(row=0, column=1, pady=5, padx=10)
            first_name_entry.insert(0, author.first_name)

            Label(form, text="Last Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
            last_name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            last_name_entry.grid(row=1, column=1, pady=5, padx=10)
            last_name_entry.insert(0, author.last_name)

            Label(form, text="Phone:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
            phone_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            phone_entry.grid(row=2, column=1, pady=5, padx=10)
            phone_entry.insert(0, author.phone or "")

            def save():
                first_name = first_name_entry.get().strip()
                last_name = last_name_entry.get().strip()
                phone = phone_entry.get().strip()

                if not first_name or not last_name:
                    messagebox.showerror("Error", "First name and last name are required")
                    return

                if phone and not self.validate_phone(phone):
                    messagebox.showerror("Error", "Phone number must be exactly 11 digits")
                    return

                update_author(author_id, first_name, last_name, phone if phone else None)
                refresh_authors()
                form.destroy()
                messagebox.showinfo("Success", "Author updated!")

            Button(form, text="Save", command=save, bg=self.warning_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=3, column=0, columnspan=2, pady=20)
            Button(form, text="Cancel", command=form.destroy, bg=self.danger_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=4, column=0, columnspan=2)

        def delete_author_handler():
            selected = author_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select an author")
                return
            if messagebox.askyesno("Confirm", "Delete this author?"):
                item = author_tree.item(selected[0])
                values = item['values']
                if values:
                    delete_author(values[0])
                    refresh_authors()
                    messagebox.showinfo("Success", "Author deleted!")

        Button(author_btn_frame, text="Add", command=add_author, bg=self.success_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)
        Button(author_btn_frame, text="Edit", command=edit_author, bg=self.warning_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)
        Button(author_btn_frame, text="Delete", command=delete_author_handler, bg=self.danger_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)

        refresh_authors()

        publisher_panel = Frame(main_frame, relief="solid", bd=1, bg="#FFFFFF")
        publisher_panel.pack(side="left", fill="both", expand=True, padx=5)

        Label(publisher_panel, text="🏢 Publishers", font=("Segoe UI", 12, "bold"),
              bg="#FFFFFF", fg="#556B2F").pack(pady=5)

        publisher_tree = Treeview(publisher_panel, columns=("id", "name"),
                                  show="headings", height=10)
        publisher_tree.heading("id", text="ID")
        publisher_tree.heading("name", text="Name")
        publisher_tree.column("id", width=40)
        publisher_tree.column("name", width=130)
        publisher_tree.pack(fill="both", expand=True, padx=5, pady=5)

        publisher_btn_frame = Frame(publisher_panel, bg="#FFFFFF")
        publisher_btn_frame.pack(pady=5)

        def refresh_publishers():
            for item in publisher_tree.get_children():
                publisher_tree.delete(item)
            for publisher in get_publisher_list():
                publisher_tree.insert("", "end", iid=publisher.id, values=(publisher.id, publisher.title))

        def add_publisher():
            form = Toplevel(manage_window)
            form.title("Add Publisher")
            form.geometry("400x150")
            form.configure(bg="#F0F5E8")
            form.transient(manage_window)
            form.grab_set()
            self.center_window(form)

            Label(form, text="Publisher Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
            name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            name_entry.grid(row=0, column=1, pady=5, padx=10)

            def save():
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Publisher name is required")
                    return
                insert_publisher(name)
                refresh_publishers()
                form.destroy()
                messagebox.showinfo("Success", "Publisher added!")

            Button(form, text="Save", command=save, bg=self.success_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=1, column=0, columnspan=2, pady=20)
            Button(form, text="Cancel", command=form.destroy, bg=self.danger_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=2, column=0, columnspan=2)

        def edit_publisher():
            selected = publisher_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a publisher")
                return

            item = publisher_tree.item(selected[0])
            values = item['values']
            if not values:
                messagebox.showerror("Error", "No data found")
                return

            publisher_id = values[0]

            publisher = None
            for p in get_publisher_list():
                if p.id == publisher_id:
                    publisher = p
                    break
            if not publisher:
                messagebox.showerror("Error", f"Publisher with ID {publisher_id} not found")
                return

            form = Toplevel(manage_window)
            form.title("Edit Publisher")
            form.geometry("400x150")
            form.configure(bg="#F0F5E8")
            form.transient(manage_window)
            form.grab_set()
            self.center_window(form)

            Label(form, text="Publisher Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
            name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            name_entry.grid(row=0, column=1, pady=5, padx=10)
            name_entry.insert(0, publisher.title)

            def save():
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Publisher name is required")
                    return
                update_publisher(publisher_id, name)
                refresh_publishers()
                form.destroy()
                messagebox.showinfo("Success", "Publisher updated!")

            Button(form, text="Save", command=save, bg=self.warning_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=1, column=0, columnspan=2, pady=20)
            Button(form, text="Cancel", command=form.destroy, bg=self.danger_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=2, column=0, columnspan=2)

        def delete_publisher_handler():
            selected = publisher_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a publisher")
                return
            if messagebox.askyesno("Confirm", "Delete this publisher?"):
                item = publisher_tree.item(selected[0])
                values = item['values']
                if values:
                    delete_publisher(values[0])
                    refresh_publishers()
                    messagebox.showinfo("Success", "Publisher deleted!")

        Button(publisher_btn_frame, text="Add", command=add_publisher, bg=self.success_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)
        Button(publisher_btn_frame, text="Edit", command=edit_publisher, bg=self.warning_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)
        Button(publisher_btn_frame, text="Delete", command=delete_publisher_handler, bg=self.danger_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)

        refresh_publishers()

        translator_panel = Frame(main_frame, relief="solid", bd=1, bg="#FFFFFF")
        translator_panel.pack(side="left", fill="both", expand=True, padx=5)

        Label(translator_panel, text="🔄 Translators", font=("Segoe UI", 12, "bold"),
              bg="#FFFFFF", fg="#556B2F").pack(pady=5)

        translator_tree = Treeview(translator_panel, columns=("id", "name", "phone"),
                                   show="headings", height=10)
        translator_tree.heading("id", text="ID")
        translator_tree.heading("name", text="Name")
        translator_tree.heading("phone", text="Phone")
        translator_tree.column("id", width=40)
        translator_tree.column("name", width=130)
        translator_tree.column("phone", width=100)
        translator_tree.pack(fill="both", expand=True, padx=5, pady=5)

        translator_btn_frame = Frame(translator_panel, bg="#FFFFFF")
        translator_btn_frame.pack(pady=5)

        def refresh_translators():
            for item in translator_tree.get_children():
                translator_tree.delete(item)
            for translator in get_translator_list():
                translator_tree.insert("", "end", iid=translator.id, values=(translator.id, translator.get_fullname(), translator.phone or "-"))

        def add_translator():
            form = Toplevel(manage_window)
            form.title("Add Translator")
            form.geometry("400x250")
            form.configure(bg="#F0F5E8")
            form.transient(manage_window)
            form.grab_set()
            self.center_window(form)

            Label(form, text="First Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
            first_name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            first_name_entry.grid(row=0, column=1, pady=5, padx=10)

            Label(form, text="Last Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
            last_name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            last_name_entry.grid(row=1, column=1, pady=5, padx=10)

            Label(form, text="Phone (Optional):", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
            phone_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            phone_entry.grid(row=2, column=1, pady=5, padx=10)

            def save():
                first_name = first_name_entry.get().strip()
                last_name = last_name_entry.get().strip()
                phone = phone_entry.get().strip()

                if not first_name or not last_name:
                    messagebox.showerror("Error", "First name and last name are required")
                    return

                if phone and not self.validate_phone(phone):
                    messagebox.showerror("Error", "Phone number must be exactly 11 digits")
                    return

                insert_translator(first_name, last_name, phone if phone else None)
                refresh_translators()
                form.destroy()
                messagebox.showinfo("Success", "Translator added!")

            Button(form, text="Save", command=save, bg=self.success_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=3, column=0, columnspan=2, pady=20)
            Button(form, text="Cancel", command=form.destroy, bg=self.danger_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=4, column=0, columnspan=2)

        def edit_translator():
            selected = translator_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a translator")
                return

            item = translator_tree.item(selected[0])
            values = item['values']
            if not values:
                messagebox.showerror("Error", "No data found for selected item")
                return

            translator_id = values[0]

            translator = None
            for t in get_translator_list():
                if t.id == translator_id:
                    translator = t
                    break

            if not translator:
                messagebox.showerror("Error", f"Translator with ID {translator_id} not found")
                return

            form = Toplevel(manage_window)
            form.title("Edit Translator")
            form.geometry("400x250")
            form.configure(bg="#F0F5E8")
            form.transient(manage_window)
            form.grab_set()
            self.center_window(form)

            Label(form, text="First Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
            first_name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            first_name_entry.grid(row=0, column=1, pady=5, padx=10)
            first_name_entry.insert(0, translator.first_name)

            Label(form, text="Last Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=1, column=0, pady=5, padx=10)
            last_name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            last_name_entry.grid(row=1, column=1, pady=5, padx=10)
            last_name_entry.insert(0, translator.last_name)

            Label(form, text="Phone:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=2, column=0, pady=5, padx=10)
            phone_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            phone_entry.grid(row=2, column=1, pady=5, padx=10)
            phone_entry.insert(0, translator.phone or "")

            def save():
                first_name = first_name_entry.get().strip()
                last_name = last_name_entry.get().strip()
                phone = phone_entry.get().strip()

                if not first_name or not last_name:
                    messagebox.showerror("Error", "First name and last name are required")
                    return

                if phone and not self.validate_phone(phone):
                    messagebox.showerror("Error", "Phone number must be exactly 11 digits")
                    return

                update_translator(translator_id, first_name, last_name, phone if phone else None)
                refresh_translators()
                form.destroy()
                messagebox.showinfo("Success", "Translator updated!")

            Button(form, text="Save", command=save, bg=self.warning_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=3, column=0, columnspan=2, pady=20)
            Button(form, text="Cancel", command=form.destroy, bg=self.danger_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=4, column=0, columnspan=2)

        def delete_translator_handler():
            selected = translator_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a translator")
                return
            if messagebox.askyesno("Confirm", "Delete this translator?"):
                item = translator_tree.item(selected[0])
                values = item['values']
                if values:
                    delete_translator(values[0])
                    refresh_translators()
                    messagebox.showinfo("Success", "Translator deleted!")

        Button(translator_btn_frame, text="Add", command=add_translator, bg=self.success_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)
        Button(translator_btn_frame, text="Edit", command=edit_translator, bg=self.warning_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)
        Button(translator_btn_frame, text="Delete", command=delete_translator_handler, bg=self.danger_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)

        refresh_translators()

        genre_panel = Frame(main_frame, relief="solid", bd=1, bg="#FFFFFF")
        genre_panel.pack(side="left", fill="both", expand=True, padx=5)

        Label(genre_panel, text="🎭 Genres", font=("Segoe UI", 12, "bold"),
              bg="#FFFFFF", fg="#556B2F").pack(pady=5)

        genre_tree = Treeview(genre_panel, columns=("id", "name"),
                              show="headings", height=10)
        genre_tree.heading("id", text="ID")
        genre_tree.heading("name", text="Name")
        genre_tree.column("id", width=40)
        genre_tree.column("name", width=130)
        genre_tree.pack(fill="both", expand=True, padx=5, pady=5)

        genre_btn_frame = Frame(genre_panel, bg="#FFFFFF")
        genre_btn_frame.pack(pady=5)

        def refresh_genres():
            for item in genre_tree.get_children():
                genre_tree.delete(item)
            for genre in get_genre_list():
                genre_tree.insert("", "end", iid=genre.id, values=(genre.id, genre.name))

        def add_genre():
            form = Toplevel(manage_window)
            form.title("Add Genre")
            form.geometry("400x150")
            form.configure(bg="#F0F5E8")
            form.transient(manage_window)
            form.grab_set()
            self.center_window(form)

            Label(form, text="Genre Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
            name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            name_entry.grid(row=0, column=1, pady=5, padx=10)

            def save():
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Genre name is required")
                    return
                insert_genre(name)
                refresh_genres()
                form.destroy()
                messagebox.showinfo("Success", "Genre added!")

            Button(form, text="Save", command=save, bg=self.success_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=1, column=0, columnspan=2, pady=20)
            Button(form, text="Cancel", command=form.destroy, bg=self.danger_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=2, column=0, columnspan=2)

        def edit_genre():
            selected = genre_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a genre")
                return

            item = genre_tree.item(selected[0])
            values = item['values']
            if not values:
                messagebox.showerror("Error", "No data found")
                return

            genre_id = values[0]

            genre = None
            for g in get_genre_list():
                if g.id == genre_id:
                    genre = g
                    break
            if not genre:
                messagebox.showerror("Error", f"Genre with ID {genre_id} not found")
                return

            form = Toplevel(manage_window)
            form.title("Edit Genre")
            form.geometry("400x150")
            form.configure(bg="#F0F5E8")
            form.transient(manage_window)
            form.grab_set()
            self.center_window(form)

            Label(form, text="Genre Name:", font=("Segoe UI", 10), bg="#FFFFFF").grid(row=0, column=0, pady=5, padx=10)
            name_entry = Entry(form, font=("Segoe UI", 11), width=30, bg="#F0F5E8", relief="solid", bd=1)
            name_entry.grid(row=0, column=1, pady=5, padx=10)
            name_entry.insert(0, genre.name)

            def save():
                name = name_entry.get().strip()
                if not name:
                    messagebox.showerror("Error", "Genre name is required")
                    return
                update_genre(genre_id, name)
                refresh_genres()
                form.destroy()
                messagebox.showinfo("Success", "Genre updated!")

            Button(form, text="Save", command=save, bg=self.warning_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=1, column=0, columnspan=2, pady=20)
            Button(form, text="Cancel", command=form.destroy, bg=self.danger_color, fg="white",
                   relief="flat", padx=20, pady=5).grid(row=2, column=0, columnspan=2)

        def delete_genre_handler():
            selected = genre_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a genre")
                return
            if messagebox.askyesno("Confirm", "Delete this genre?"):
                item = genre_tree.item(selected[0])
                values = item['values']
                if values:
                    delete_genre(values[0])
                    refresh_genres()
                    messagebox.showinfo("Success", "Genre deleted!")

        Button(genre_btn_frame, text="Add", command=add_genre, bg=self.success_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)
        Button(genre_btn_frame, text="Edit", command=edit_genre, bg=self.warning_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)
        Button(genre_btn_frame, text="Delete", command=delete_genre_handler, bg=self.danger_color, fg="white",
               relief="flat", padx=10, pady=2).pack(side="left", padx=2)

        refresh_genres()

def run_library_panel(username=None, role=None):
    LibraryPanel(username, role)

if __name__ == "__main__":
    run_library_panel()