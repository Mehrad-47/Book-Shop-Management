from ui_theme import apply_theme
from tkinter import Tk, Label, Entry, Button, Toplevel, messagebox, Frame, Scrollbar
from tkinter.ttk import Treeview, Combobox
from tkinter import LabelFrame
from DataAccess.book_data_access import get_book_list, get_book_by_id, insert_book
from DataAccess.customer_data_access import get_customer_list, insert_customer
from DataAccess.author_data_access import get_author_list, insert_author
from DataAccess.publisher_data_access import get_publisher_list, insert_publisher
from DataAccess.genre_data_access import get_genre_list, insert_genre
from DataAccess.translator_data_access import get_translator_list, insert_translator
from datetime import datetime
import sqlite3
import re

class SalesPanel:
    def __init__(self, username=None, role=None):
        self.window = Tk()
        apply_theme(self.window)
        self.window.title("Sales Panel")
        self.window.geometry("1100x750")
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

        self.sale_items = []
        self.selected_customer_id = None
        self.selected_customer_name = "Unknown Customer"
        self.customers = []

        header = Frame(self.window, bg=self.header_color, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        Button(header, text="← Back to Dashboard",
               font=("Segoe UI", 11, "bold"),
               bg=self.header_color, fg="white", relief="flat",
               cursor="hand2", command=self.back_to_dashboard).pack(side="left", padx=20, pady=15)

        Label(header, text="🛒 Sales Panel",
              font=("Segoe UI", 16, "bold"), bg=self.header_color, fg="white").pack(side="left", padx=20)

        Label(header, text=f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
              font=("Segoe UI", 11), bg=self.header_color, fg="#D4E8C4").pack(side="right", padx=20)

        main_frame = Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        left_panel = Frame(main_frame, bg=self.card_color, relief="ridge", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=5)

        Label(left_panel, text="👤 Select Customer", font=("Segoe UI", 12, "bold"),
              bg=self.card_color, fg=self.text_color).pack(pady=10)

        customer_frame = Frame(left_panel, bg=self.card_color)
        customer_frame.pack(pady=5, padx=10, fill="x")

        self.refresh_customers()

        self.customer_combo = Combobox(customer_frame, values=self.customer_names,
                                       state="readonly", width=28, font=("Segoe UI", 11))
        self.customer_combo.pack(side="left", padx=5, fill="x", expand=True)
        self.customer_combo.set("Unknown Customer")
        self.customer_combo.bind('<<ComboboxSelected>>', self.select_customer)

        Button(customer_frame, text="+ New", command=self.show_new_customer_form,
               bg=self.success_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=10, pady=5, cursor="hand2").pack(side="right", padx=2)

        Button(customer_frame, text="✏️ Edit", command=self.show_edit_customer_form,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=10, pady=5, cursor="hand2").pack(side="right", padx=2)

        self.points_label = Label(left_panel, text="⭐ Customer Points: 0",
                                  font=("Segoe UI", 11), bg=self.card_color, fg=self.primary_color)
        self.points_label.pack(pady=5)

        Frame(left_panel, bg="#E2E8F0", height=2).pack(fill="x", padx=10, pady=10)

        Label(left_panel, text="📖 Select Book", font=("Segoe UI", 12, "bold"),
              bg=self.card_color, fg=self.text_color).pack(pady=10)

        self.refresh_books()

        book_frame = Frame(left_panel, bg=self.card_color)
        book_frame.pack(pady=5, padx=10, fill="x")

        self.book_combo = Combobox(book_frame, values=self.book_titles,
                                   state="readonly", width=35, font=("Segoe UI", 11))
        self.book_combo.pack(side="left", padx=5, fill="x", expand=True)

        Button(book_frame, text="+ New", command=self.show_new_book_form,
               bg=self.primary_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=10, pady=5, cursor="hand2").pack(side="right", padx=5)

        quantity_frame = Frame(left_panel, bg=self.card_color)
        quantity_frame.pack(pady=10, padx=10, fill="x")

        Label(quantity_frame, text="Quantity:", font=("Segoe UI", 11, "bold"),
              bg=self.card_color, fg=self.text_color).pack(side="left", padx=5)

        self.quantity_entry = Entry(quantity_frame, font=("Segoe UI", 12), width=10,
                                    bg="#F0F5E8", relief="solid", bd=1)
        self.quantity_entry.pack(side="left", padx=10)
        self.quantity_entry.insert(0, "1")

        add_btn = Button(left_panel, text="➕ Add to Cart",
                         command=self.add_to_cart,
                         bg=self.success_color, fg="white", font=("Segoe UI", 12, "bold"),
                         relief="flat", padx=20, pady=10, cursor="hand2")
        add_btn.pack(pady=10)

        right_panel = Frame(main_frame, bg=self.card_color, relief="ridge", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=5)

        Label(right_panel, text="🛒 Shopping Cart", font=("Segoe UI", 12, "bold"),
              bg=self.card_color, fg=self.text_color).pack(pady=10)

        cart_frame = Frame(right_panel, bg=self.card_color)
        cart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        scroll_y = Scrollbar(cart_frame)
        scroll_y.pack(side="right", fill="y")

        self.cart_treeview = Treeview(cart_frame, columns=("book", "quantity", "unit_price", "total"),
                                      show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.cart_treeview.yview)

        self.cart_treeview.heading("book", text="Book")
        self.cart_treeview.heading("quantity", text="Quantity")
        self.cart_treeview.heading("unit_price", text="Unit Price")
        self.cart_treeview.heading("total", text="Total")

        self.cart_treeview.column("book", width=250)
        self.cart_treeview.column("quantity", width=80)
        self.cart_treeview.column("unit_price", width=120)
        self.cart_treeview.column("total", width=130)

        self.cart_treeview.pack(fill="both", expand=True)

        total_frame = Frame(right_panel, bg=self.card_color)
        total_frame.pack(fill="x", pady=10, padx=10)

        self.total_label = Label(total_frame, text="💰 Total Amount: 0 USD",
                                 font=("Segoe UI", 14, "bold"), bg=self.card_color, fg=self.primary_color)
        self.total_label.pack()

        cart_btn_frame = Frame(right_panel, bg=self.card_color)
        cart_btn_frame.pack(pady=10)

        Button(cart_btn_frame, text="🗑️ Remove", command=self.remove_from_cart,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=5, cursor="hand2").pack(side="left", padx=5)

        Button(cart_btn_frame, text="🧹 Clear", command=self.clear_cart,
               bg=self.danger_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=5, cursor="hand2").pack(side="left", padx=5)

        finalize_btn = Button(right_panel, text="✅ Finalize Sale",
                              command=self.finalize_sale,
                              bg=self.primary_color, fg="white", font=("Segoe UI", 14, "bold"),
                              relief="flat", padx=30, pady=10, cursor="hand2")
        finalize_btn.pack(pady=10)

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

    def refresh_customers(self):
        self.customers = get_customer_list()
        self.customer_names = ["Unknown Customer"] + [c.get_information() for c in self.customers]
        if hasattr(self, 'customer_combo'):
            current_value = self.customer_combo.get()
            self.customer_combo['values'] = self.customer_names
            if current_value in self.customer_names:
                self.customer_combo.set(current_value)
            else:
                self.customer_combo.set("Unknown Customer")

    def refresh_books(self):
        books = get_book_list()
        self.book_titles = [f"{b.id} - {b.title} (Stock: {b.stock})" for b in books if b.stock > 0]
        if hasattr(self, 'book_combo'):
            self.book_combo['values'] = self.book_titles

    def select_customer(self, event):
        if self.customer_combo.get() != "Unknown Customer":
            try:
                self.selected_customer_id = int(self.customer_combo.get().split('-')[0])
                self.selected_customer_name = self.customer_combo.get().split('-')[1].strip()
                self.refresh_customers()
                for c in self.customers:
                    if c.id == self.selected_customer_id:
                        self.points_label.config(text=f"⭐ Customer Points: {c.points}")
                        break
            except:
                self.selected_customer_id = None
                self.selected_customer_name = "Unknown Customer"
                self.points_label.config(text="⭐ Customer Points: 0")
        else:
            self.selected_customer_id = None
            self.selected_customer_name = "Unknown Customer"
            self.points_label.config(text="⭐ Customer Points: 0")

    def validate_phone(self, phone):
        phone = phone.replace(" ", "").replace("-", "")
        return len(phone) == 11 and phone.isdigit()

    def show_new_customer_form(self):
        customer_form = Toplevel(self.window)
        customer_form.title("Register New Customer")
        customer_form.geometry("500x450")
        customer_form.configure(bg="#F0F5E8")
        customer_form.transient(self.window)
        customer_form.grab_set()
        customer_form.resizable(False, False)

        self.center_window(customer_form)

        title_frame = Frame(customer_form, bg=self.primary_color, height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        Label(title_frame, text="📝 Register New Customer",
              font=("Segoe UI", 14, "bold"), bg=self.primary_color, fg="white").pack(pady=12)

        main_frame = Frame(customer_form, bg=self.card_color, padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)

        row1 = Frame(main_frame, bg=self.card_color)
        row1.pack(fill="x", pady=8)
        Label(row1, text="First Name:", font=("Segoe UI", 10),
              bg=self.card_color, width=14, anchor="e").pack(side="left")
        first_name_entry = Entry(row1, font=("Segoe UI", 11), width=25,
                                 bg="#F0F5E8", relief="solid", bd=1)
        first_name_entry.pack(side="left", padx=5)

        row2 = Frame(main_frame, bg=self.card_color)
        row2.pack(fill="x", pady=8)
        Label(row2, text="Last Name:", font=("Segoe UI", 10),
              bg=self.card_color, width=14, anchor="e").pack(side="left")
        last_name_entry = Entry(row2, font=("Segoe UI", 11), width=25,
                                bg="#F0F5E8", relief="solid", bd=1)
        last_name_entry.pack(side="left", padx=5)

        row3 = Frame(main_frame, bg=self.card_color)
        row3.pack(fill="x", pady=8)
        Label(row3, text="Phone:", font=("Segoe UI", 10),
              bg=self.card_color, width=14, anchor="e").pack(side="left")
        phone_entry = Entry(row3, font=("Segoe UI", 11), width=25,
                            bg="#F0F5E8", relief="solid", bd=1)
        phone_entry.pack(side="left", padx=5)

        row4 = Frame(main_frame, bg=self.card_color)
        row4.pack(fill="x", pady=8)
        Label(row4, text="Birth Date:", font=("Segoe UI", 10),
              bg=self.card_color, width=14, anchor="e").pack(side="left")

        year_entry = Entry(row4, font=("Segoe UI", 11), width=6,
                           bg="#F0F5E8", relief="solid", bd=1)
        year_entry.pack(side="left", padx=2)
        year_entry.insert(0, "YYYY")
        year_entry.config(fg="#7A8C5A")

        def year_focus_in(event):
            if year_entry.get() == "YYYY":
                year_entry.delete(0, 'end')
                year_entry.config(fg="#2C3A1A")

        def year_focus_out(event):
            if year_entry.get() == "":
                year_entry.insert(0, "YYYY")
                year_entry.config(fg="#7A8C5A")

        year_entry.bind('<FocusIn>', year_focus_in)
        year_entry.bind('<FocusOut>', year_focus_out)

        Label(row4, text="/", font=("Segoe UI", 14), bg=self.card_color).pack(side="left", padx=2)

        month_entry = Entry(row4, font=("Segoe UI", 11), width=4,
                            bg="#F0F5E8", relief="solid", bd=1)
        month_entry.pack(side="left", padx=2)
        month_entry.insert(0, "MM")
        month_entry.config(fg="#7A8C5A")

        def month_focus_in(event):
            if month_entry.get() == "MM":
                month_entry.delete(0, 'end')
                month_entry.config(fg="#2C3A1A")

        def month_focus_out(event):
            if month_entry.get() == "":
                month_entry.insert(0, "MM")
                month_entry.config(fg="#7A8C5A")

        month_entry.bind('<FocusIn>', month_focus_in)
        month_entry.bind('<FocusOut>', month_focus_out)

        Label(row4, text="/", font=("Segoe UI", 14), bg=self.card_color).pack(side="left", padx=2)

        day_entry = Entry(row4, font=("Segoe UI", 11), width=4,
                          bg="#F0F5E8", relief="solid", bd=1)
        day_entry.pack(side="left", padx=2)
        day_entry.insert(0, "DD")
        day_entry.config(fg="#7A8C5A")

        def day_focus_in(event):
            if day_entry.get() == "DD":
                day_entry.delete(0, 'end')
                day_entry.config(fg="#2C3A1A")

        def day_focus_out(event):
            if day_entry.get() == "":
                day_entry.insert(0, "DD")
                day_entry.config(fg="#7A8C5A")

        day_entry.bind('<FocusIn>', day_focus_in)
        day_entry.bind('<FocusOut>', day_focus_out)

        def save_customer():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            phone = phone_entry.get().strip()
            year = year_entry.get().strip()
            month = month_entry.get().strip()
            day = day_entry.get().strip()

            if not first_name or not last_name:
                messagebox.showerror("Error", "First name and last name are required")
                return

            if not phone:
                messagebox.showerror("Error", "Phone number is required")
                return

            if not self.validate_phone(phone):
                messagebox.showerror("Error", "Phone number must be exactly 11 digits")
                return

            birth_date = ""
            if year and year != "YYYY" and month and month != "MM" and day and day != "DD":
                try:
                    if len(year) != 4 or not year.isdigit():
                        messagebox.showerror("Error", "Year must be 4 digits")
                        return
                    month_int = int(month)
                    if month_int < 1 or month_int > 12:
                        messagebox.showerror("Error", "Month must be between 1 and 12")
                        return
                    day_int = int(day)
                    if day_int < 1 or day_int > 31:
                        messagebox.showerror("Error", "Day must be between 1 and 31")
                        return
                    birth_date = f"{year}/{month.zfill(2)}/{day.zfill(2)}"
                    datetime.strptime(birth_date, '%Y/%m/%d')
                except ValueError:
                    messagebox.showerror("Error", "Invalid birth date")
                    return
            elif year or month or day:
                messagebox.showerror("Error", "Please enter complete birth date (Year, Month, Day)")
                return

            try:
                insert_customer(first_name, last_name, phone, birth_date if birth_date else None)

                self.refresh_customers()
                self.customer_combo.set(f"{self.customers[-1].id}-{first_name} {last_name}")
                self.selected_customer_id = self.customers[-1].id
                self.selected_customer_name = f"{first_name} {last_name}"
                self.points_label.config(text="⭐ Customer Points: 0")

                customer_form.destroy()
                messagebox.showinfo("Success", "Customer registered successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Error saving customer: {str(e)}")

        btn_frame = Frame(main_frame, bg=self.card_color)
        btn_frame.pack(pady=20)

        Button(btn_frame, text="✅ Register", command=save_customer,
               bg=self.success_color, fg="white", font=("Segoe UI", 11, "bold"),
               relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)

        Button(btn_frame, text="❌ Cancel", command=customer_form.destroy,
               bg=self.danger_color, fg="white", font=("Segoe UI", 11, "bold"),
               relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)

    def show_edit_customer_form(self):
        if not self.selected_customer_id:
            messagebox.showwarning("Warning", "Please select a customer to edit")
            return

        selected_customer = None
        for c in self.customers:
            if c.id == self.selected_customer_id:
                selected_customer = c
                break

        if not selected_customer:
            messagebox.showerror("Error", "Customer not found")
            return

        customer_form = Toplevel(self.window)
        customer_form.title("Edit Customer")
        customer_form.geometry("500x450")
        customer_form.configure(bg="#F0F5E8")
        customer_form.transient(self.window)
        customer_form.grab_set()
        customer_form.resizable(False, False)

        self.center_window(customer_form)

        title_frame = Frame(customer_form, bg=self.primary_color, height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        Label(title_frame, text="✏️ Edit Customer",
              font=("Segoe UI", 14, "bold"), bg=self.primary_color, fg="white").pack(pady=12)

        main_frame = Frame(customer_form, bg=self.card_color, padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)

        row1 = Frame(main_frame, bg=self.card_color)
        row1.pack(fill="x", pady=8)
        Label(row1, text="First Name:", font=("Segoe UI", 10),
              bg=self.card_color, width=14, anchor="e").pack(side="left")
        first_name_entry = Entry(row1, font=("Segoe UI", 11), width=25,
                                 bg="#F0F5E8", relief="solid", bd=1)
        first_name_entry.pack(side="left", padx=5)
        first_name_entry.insert(0, selected_customer.first_name)

        row2 = Frame(main_frame, bg=self.card_color)
        row2.pack(fill="x", pady=8)
        Label(row2, text="Last Name:", font=("Segoe UI", 10),
              bg=self.card_color, width=14, anchor="e").pack(side="left")
        last_name_entry = Entry(row2, font=("Segoe UI", 11), width=25,
                                bg="#F0F5E8", relief="solid", bd=1)
        last_name_entry.pack(side="left", padx=5)
        last_name_entry.insert(0, selected_customer.last_name)

        row3 = Frame(main_frame, bg=self.card_color)
        row3.pack(fill="x", pady=8)
        Label(row3, text="Phone:", font=("Segoe UI", 10),
              bg=self.card_color, width=14, anchor="e").pack(side="left")
        phone_entry = Entry(row3, font=("Segoe UI", 11), width=25,
                            bg="#F0F5E8", relief="solid", bd=1)
        phone_entry.pack(side="left", padx=5)
        phone_entry.insert(0, selected_customer.phone)

        row4 = Frame(main_frame, bg=self.card_color)
        row4.pack(fill="x", pady=8)
        Label(row4, text="Birth Date:", font=("Segoe UI", 10),
              bg=self.card_color, width=14, anchor="e").pack(side="left")

        year_val = ""
        month_val = ""
        day_val = ""
        if selected_customer.birth_date:
            parts = selected_customer.birth_date.split('/')
            if len(parts) == 3:
                year_val = parts[0]
                month_val = parts[1]
                day_val = parts[2]

        year_entry = Entry(row4, font=("Segoe UI", 11), width=6,
                           bg="#F0F5E8", relief="solid", bd=1)
        year_entry.pack(side="left", padx=2)
        if year_val:
            year_entry.insert(0, year_val)
            year_entry.config(fg="#2C3A1A")
        else:
            year_entry.insert(0, "YYYY")
            year_entry.config(fg="#7A8C5A")

        def year_focus_in(event):
            if year_entry.get() == "YYYY":
                year_entry.delete(0, 'end')
                year_entry.config(fg="#2C3A1A")

        def year_focus_out(event):
            if year_entry.get() == "":
                year_entry.insert(0, "YYYY")
                year_entry.config(fg="#7A8C5A")

        year_entry.bind('<FocusIn>', year_focus_in)
        year_entry.bind('<FocusOut>', year_focus_out)

        Label(row4, text="/", font=("Segoe UI", 14), bg=self.card_color).pack(side="left", padx=2)

        month_entry = Entry(row4, font=("Segoe UI", 11), width=4,
                            bg="#F0F5E8", relief="solid", bd=1)
        month_entry.pack(side="left", padx=2)
        if month_val:
            month_entry.insert(0, month_val)
            month_entry.config(fg="#2C3A1A")
        else:
            month_entry.insert(0, "MM")
            month_entry.config(fg="#7A8C5A")

        def month_focus_in(event):
            if month_entry.get() == "MM":
                month_entry.delete(0, 'end')
                month_entry.config(fg="#2C3A1A")

        def month_focus_out(event):
            if month_entry.get() == "":
                month_entry.insert(0, "MM")
                month_entry.config(fg="#7A8C5A")

        month_entry.bind('<FocusIn>', month_focus_in)
        month_entry.bind('<FocusOut>', month_focus_out)

        Label(row4, text="/", font=("Segoe UI", 14), bg=self.card_color).pack(side="left", padx=2)

        day_entry = Entry(row4, font=("Segoe UI", 11), width=4,
                          bg="#F0F5E8", relief="solid", bd=1)
        day_entry.pack(side="left", padx=2)
        if day_val:
            day_entry.insert(0, day_val)
            day_entry.config(fg="#2C3A1A")
        else:
            day_entry.insert(0, "DD")
            day_entry.config(fg="#7A8C5A")

        def day_focus_in(event):
            if day_entry.get() == "DD":
                day_entry.delete(0, 'end')
                day_entry.config(fg="#2C3A1A")

        def day_focus_out(event):
            if day_entry.get() == "":
                day_entry.insert(0, "DD")
                day_entry.config(fg="#7A8C5A")

        day_entry.bind('<FocusIn>', day_focus_in)
        day_entry.bind('<FocusOut>', day_focus_out)

        def update_customer():
            first_name = first_name_entry.get().strip()
            last_name = last_name_entry.get().strip()
            phone = phone_entry.get().strip()
            year = year_entry.get().strip()
            month = month_entry.get().strip()
            day = day_entry.get().strip()

            if not first_name or not last_name:
                messagebox.showerror("Error", "First name and last name are required")
                return

            if not phone:
                messagebox.showerror("Error", "Phone number is required")
                return

            if not self.validate_phone(phone):
                messagebox.showerror("Error", "Phone number must be exactly 11 digits")
                return

            birth_date = ""
            if year and year != "YYYY" and month and month != "MM" and day and day != "DD":
                try:
                    if len(year) != 4 or not year.isdigit():
                        messagebox.showerror("Error", "Year must be 4 digits")
                        return
                    month_int = int(month)
                    if month_int < 1 or month_int > 12:
                        messagebox.showerror("Error", "Month must be between 1 and 12")
                        return
                    day_int = int(day)
                    if day_int < 1 or day_int > 31:
                        messagebox.showerror("Error", "Day must be between 1 and 31")
                        return
                    birth_date = f"{year}/{month.zfill(2)}/{day.zfill(2)}"
                    datetime.strptime(birth_date, '%Y/%m/%d')
                except ValueError:
                    messagebox.showerror("Error", "Invalid birth date")
                    return
            elif year or month or day:
                messagebox.showerror("Error", "Please enter complete birth date (Year, Month, Day)")
                return

            try:
                conn = sqlite3.connect("BookShopDB.db")
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE Customer 
                SET first_name=?, last_name=?, phone=?, birth_date=?
                WHERE id=?
                """, (first_name, last_name, phone, birth_date if birth_date else None, selected_customer.id))
                conn.commit()
                conn.close()

                self.refresh_customers()
                self.customer_combo.set(f"{selected_customer.id}-{first_name} {last_name}")
                self.selected_customer_name = f"{first_name} {last_name}"
                self.points_label.config(text=f"⭐ Customer Points: {selected_customer.points}")

                customer_form.destroy()
                messagebox.showinfo("Success", "Customer updated successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Error updating customer: {str(e)}")

        btn_frame = Frame(main_frame, bg=self.card_color)
        btn_frame.pack(pady=20)

        Button(btn_frame, text="💾 Update", command=update_customer,
               bg=self.warning_color, fg="white", font=("Segoe UI", 11, "bold"),
               relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)

        Button(btn_frame, text="❌ Cancel", command=customer_form.destroy,
               bg=self.danger_color, fg="white", font=("Segoe UI", 11, "bold"),
               relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)

    def show_new_book_form(self):
        book_form = Toplevel(self.window)
        book_form.title("Add New Book")
        book_form.geometry("750x800")
        book_form.configure(bg="#F0F5E8")
        book_form.transient(self.window)
        book_form.grab_set()

        self.center_window(book_form)

        widgets = {}

        header_frame = Frame(book_form, bg=self.primary_color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        Label(header_frame, text="📝 Add New Book", font=("Segoe UI", 14, "bold"),
              bg=self.primary_color, fg="white").pack(pady=12)

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

        Label(form_frame, text="Genre (Optional):", font=("Segoe UI", 10, "bold"),
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

        profit_frame = LabelFrame(form_frame, text="💰 Profit Calculation",
                                  fg=self.primary_color, font=("Segoe UI", 10, "bold"))
        profit_frame.grid(row=11, column=0, columnspan=3, pady=10, padx=10, sticky="ew")

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

                insert_book(book_data)

                self.refresh_books()
                self.book_combo['values'] = self.book_titles

                book_form.destroy()
                messagebox.showinfo("Success", "Book added successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Error saving book: {str(e)}")

        Button(book_form, text="💾 Submit Book", command=submit_book,
               bg=self.primary_color, fg="white", font=("Segoe UI", 12, "bold"),
               relief="flat", padx=40, pady=10, cursor="hand2").pack(pady=20)

    def add_to_cart(self):
        if not self.book_combo.get():
            messagebox.showerror("Error", "Please select a book")
            return

        try:
            book_id = int(self.book_combo.get().split('-')[0])
            quantity = int(self.quantity_entry.get())

            if quantity <= 0:
                messagebox.showerror("Error", "Quantity must be greater than zero")
                return

            book = get_book_by_id(book_id)
            if not book:
                messagebox.showerror("Error", "Book not found")
                return

            if quantity > book.stock:
                messagebox.showerror("Error", f"Insufficient stock. Available: {book.stock}")
                return

            for item in self.sale_items:
                if item['book_id'] == book_id:
                    messagebox.showerror("Error", "This book is already in the cart")
                    return

            self.sale_items.append({
                'book_id': book_id,
                'book_title': book.title,
                'quantity': quantity,
                'unit_price': book.price
            })

            self.update_cart_display()
            self.book_combo.set('')
            self.quantity_entry.delete(0, 'end')
            self.quantity_entry.insert(0, '1')
            self.update_total()

            messagebox.showinfo("Success", f"{book.title} added to cart!")

        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")

    def update_cart_display(self):
        for child in self.cart_treeview.get_children():
            self.cart_treeview.delete(child)

        for item in self.sale_items:
            self.cart_treeview.insert(
                "",
                "end",
                values=(
                    item['book_title'],
                    item['quantity'],
                    f"{item['unit_price']:,.2f}",
                    f"{item['quantity'] * item['unit_price']:,.2f}"
                )
            )

    def update_total(self):
        total = sum(item['quantity'] * item['unit_price'] for item in self.sale_items)
        self.total_label.config(text=f"💰 Total Amount: {total:,.2f} USD")

    def remove_from_cart(self):
        selected = self.cart_treeview.selection()
        if selected:
            idx = int(self.cart_treeview.index(selected[0]))
            self.sale_items.pop(idx)
            self.update_cart_display()
            self.update_total()
            messagebox.showinfo("Success", "Item removed from cart!")
        else:
            messagebox.showwarning("Warning", "Please select an item to remove")

    def clear_cart(self):
        if self.sale_items:
            if messagebox.askyesno("Confirm", "Are you sure you want to clear the cart?"):
                self.sale_items = []
                self.update_cart_display()
                self.update_total()
                messagebox.showinfo("Success", "Cart cleared!")

    def create_sale(self, customer_id, items):
        with sqlite3.connect("BookShopDB.db") as connection:
            cursor = connection.cursor()

            total_amount = sum(item['quantity'] * item['unit_price'] for item in items)

            cursor.execute("""
            INSERT INTO Sale (customer_id, sale_date, total_amount)
            VALUES (?, ?, ?)
            """, (
                customer_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total_amount
            ))

            sale_id = cursor.lastrowid

            for item in items:
                cursor.execute("""
                INSERT INTO SaleItem (sale_id, book_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
                """, (
                    sale_id,
                    item['book_id'],
                    item['quantity'],
                    item['unit_price']
                ))

                cursor.execute("""
                UPDATE Book SET stock = stock - ? WHERE id = ?
                """, (item['quantity'], item['book_id']))

            if customer_id:
                points = int(total_amount / 10)
                if points > 0:
                    cursor.execute("""
                    UPDATE Customer SET points = points + ? WHERE id = ?
                    """, (points, customer_id))

            connection.commit()
            return sale_id

    def finalize_sale(self):
        if not self.sale_items:
            messagebox.showerror("Error", "Cart is empty")
            return

        try:
            total = sum(item['quantity'] * item['unit_price'] for item in self.sale_items)

            points_to_earn = int(total / 10)
            points_msg = f"\n\n⭐ Points to earn: {points_to_earn}" if points_to_earn > 0 else ""

            if not messagebox.askyesno(
                "Confirm Sale",
                f"👤 Customer: {self.selected_customer_name}\n"
                f"💰 Total Amount: {total:,.2f} USD{points_msg}\n\n"
                f"📦 Items: {len(self.sale_items)} book(s)\n"
                f"Are you sure you want to finalize this sale?"
            ):
                return

            sale_id = self.create_sale(self.selected_customer_id, self.sale_items)

            self.refresh_customers()
            if self.selected_customer_id:
                for c in self.customers:
                    if c.id == self.selected_customer_id:
                        self.points_label.config(text=f"⭐ Customer Points: {c.points}")
                        self.customer_combo.set(c.get_information())
                        break

            messagebox.showinfo(
                "✅ Success",
                f"Sale invoice #{sale_id} created successfully!\n\n"
                f"👤 Customer: {self.selected_customer_name}\n"
                f"💰 Total Amount: {total:,.2f} USD\n"
                f"⭐ Points Earned: {points_to_earn}"
            )

            self.sale_items = []
            self.update_cart_display()
            self.update_total()
            self.refresh_books()
            self.book_combo['values'] = self.book_titles

        except Exception as e:
            messagebox.showerror("Error", f"Error finalizing sale: {str(e)}")

def run_sales_panel(username=None, role=None):
    SalesPanel(username, role)

if __name__ == "__main__":
    run_sales_panel()