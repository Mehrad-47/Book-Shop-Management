from ui_theme import apply_theme
from tkinter import Tk, Label, Entry, Button, Frame, messagebox, Canvas
import re
import sqlite3
import hashlib

class LoginApp:
    def __init__(self):
        self.window = Tk()
        apply_theme(self.window)
        self.window.title("Mehrad's Book Shop - Login")
        self.window.geometry("900x600")
        self.window.resizable(False, False)
        self.window.configure(bg="#F0F5E8")

        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.primary_color = "#556B2F"
        self.primary_hover = "#3D4F23"
        self.primary_light = "#6B8E23"
        self.error_color = "#8B3A3A"
        self.success_color = "#4A7A2E"
        self.text_color = "#2C3A1A"
        self.text_secondary = "#7A8C5A"
        self.bg_color = "#F0F5E8"
        self.bg_light = "#FFFFFF"
        self.card_color = "#FAFCF7"

        self.user_role = None
        self.username = None

        self.show_login()
        self.window.mainloop()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_tables(self):
        try:
            conn = sqlite3.connect("BookShopDB.db")
            cursor = conn.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'employee',
                full_name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """)

            cursor.execute("SELECT id FROM Users WHERE username = 'boss'")
            if not cursor.fetchone():
                hashed_password = self.hash_password("Bookshopboss@123")
                cursor.execute("""
                INSERT INTO Users (username, password, role, full_name)
                VALUES (?, ?, ?, ?)
                """, ("boss", hashed_password, "admin", "Boss Manager"))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error creating tables: {e}")

    def show_login(self):
        self.clear_window()
        self.create_tables()

        main_frame = Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)

        left_frame = Frame(main_frame, bg=self.primary_color, width=400)
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.pack_propagate(False)

        canvas = Canvas(left_frame, bg=self.primary_color, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_oval(50, 100, 200, 250, outline="#8FBC8F", width=3, fill="")
        canvas.create_oval(250, 300, 380, 430, outline="#8FBC8F", width=3, fill="")
        canvas.create_oval(30, 400, 150, 520, outline="#8FBC8F", width=3, fill="")

        canvas.create_text(200, 200, text="📚", font=("Segoe UI", 80))
        canvas.create_text(200, 280, text="Mehrad's Book Shop", font=("Segoe UI", 28, "bold"), fill="white")
        canvas.create_text(200, 320, text="Management System", font=("Segoe UI", 16), fill="#D4E8C4")

        right_frame = Frame(main_frame, bg=self.card_color, width=500)
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)

        form_frame = Frame(right_frame, bg=self.card_color)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        Label(form_frame, text="Welcome Back!", font=("Segoe UI", 24, "bold"),
              bg=self.card_color, fg=self.text_color).pack(pady=(0, 5))

        Label(form_frame, text="Sign in to your account to continue",
              font=("Segoe UI", 12), bg=self.card_color, fg=self.text_secondary).pack(pady=(0, 30))

        Label(form_frame, text="Username", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color, anchor="w").pack(fill="x", pady=(0, 5))

        self.username_entry = Entry(form_frame, font=("Segoe UI", 12),
                                    bg=self.bg_light, fg=self.text_color,
                                    relief="solid", bd=1, highlightthickness=0,
                                    width=30)
        self.username_entry.pack(pady=(0, 20), ipady=8)
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())

        Label(form_frame, text="Password", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color, anchor="w").pack(fill="x", pady=(0, 5))

        self.password_entry = Entry(form_frame, font=("Segoe UI", 12),
                                    bg=self.bg_light, fg=self.text_color,
                                    relief="solid", bd=1, highlightthickness=0,
                                    width=30, show="•")
        self.password_entry.pack(pady=(0, 20), ipady=8)
        self.password_entry.bind('<Return>', lambda e: self.login())

        login_btn = Button(form_frame, text="Sign In", font=("Segoe UI", 12, "bold"),
                           bg=self.primary_color, fg="white", width=25,
                           relief="flat", cursor="hand2",
                           command=self.login)
        login_btn.pack(pady=(10, 15), ipady=10)

        login_btn.bind('<Enter>', lambda e: login_btn.config(bg=self.primary_hover))
        login_btn.bind('<Leave>', lambda e: login_btn.config(bg=self.primary_color))

        signup_frame = Frame(form_frame, bg=self.card_color)
        signup_frame.pack(pady=10)

        Label(signup_frame, text="Don't have an account?", font=("Segoe UI", 10),
              bg=self.card_color, fg=self.text_secondary).pack(side="left")

        signup_btn = Label(signup_frame, text="Sign Up", font=("Segoe UI", 10, "bold"),
                           bg=self.card_color, fg=self.primary_light, cursor="hand2")
        signup_btn.pack(side="left", padx=(5, 0))
        signup_btn.bind('<Button-1>', lambda e: self.show_signup())
        signup_btn.bind('<Enter>', lambda e: signup_btn.config(fg=self.primary_color))
        signup_btn.bind('<Leave>', lambda e: signup_btn.config(fg=self.primary_light))

    def show_signup(self):
        self.clear_window()

        main_frame = Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)

        left_frame = Frame(main_frame, bg=self.primary_color, width=400)
        left_frame.pack(side="left", fill="both", expand=True)
        left_frame.pack_propagate(False)

        canvas = Canvas(left_frame, bg=self.primary_color, highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_oval(50, 100, 200, 250, outline="#8FBC8F", width=3, fill="")
        canvas.create_oval(250, 300, 380, 430, outline="#8FBC8F", width=3, fill="")
        canvas.create_oval(30, 400, 150, 520, outline="#8FBC8F", width=3, fill="")

        canvas.create_text(200, 200, text="📖", font=("Segoe UI", 80))
        canvas.create_text(200, 280, text="Join Us", font=("Segoe UI", 28, "bold"), fill="white")
        canvas.create_text(200, 320, text="Create your account", font=("Segoe UI", 16), fill="#D4E8C4")

        right_frame = Frame(main_frame, bg=self.card_color, width=500)
        right_frame.pack(side="right", fill="both", expand=True)
        right_frame.pack_propagate(False)

        form_frame = Frame(right_frame, bg=self.card_color)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        Label(form_frame, text="Create Account", font=("Segoe UI", 24, "bold"),
              bg=self.card_color, fg=self.text_color).pack(pady=(0, 5))

        Label(form_frame, text="Sign up to get started", font=("Segoe UI", 12),
              bg=self.card_color, fg=self.text_secondary).pack(pady=(0, 20))

        Label(form_frame, text="Username", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color, anchor="w").pack(fill="x", pady=(0, 5))

        self.signup_username = Entry(form_frame, font=("Segoe UI", 12),
                                     bg=self.bg_light, fg=self.text_color,
                                     relief="solid", bd=1, highlightthickness=0,
                                     width=30)
        self.signup_username.pack(pady=(0, 15), ipady=8)
        self.signup_username.bind('<Return>', lambda e: self.signup_password.focus())

        Label(form_frame, text="Password", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color, anchor="w").pack(fill="x", pady=(0, 5))

        self.signup_password = Entry(form_frame, font=("Segoe UI", 12),
                                     bg=self.bg_light, fg=self.text_color,
                                     relief="solid", bd=1, highlightthickness=0,
                                     width=30, show="•")
        self.signup_password.pack(pady=(0, 15), ipady=8)
        self.signup_password.bind('<KeyRelease>', self.check_password_strength)
        self.signup_password.bind('<Return>', lambda e: self.signup_confirm.focus())

        Label(form_frame, text="Confirm Password", font=("Segoe UI", 10, "bold"),
              bg=self.card_color, fg=self.text_color, anchor="w").pack(fill="x", pady=(0, 5))

        self.signup_confirm = Entry(form_frame, font=("Segoe UI", 12),
                                    bg=self.bg_light, fg=self.text_color,
                                    relief="solid", bd=1, highlightthickness=0,
                                    width=30, show="•")
        self.signup_confirm.pack(pady=(0, 15), ipady=8)
        self.signup_confirm.bind('<KeyRelease>', self.check_password_match)
        self.signup_confirm.bind('<Return>', lambda e: self.signup())

        requirements_frame = Frame(form_frame, bg=self.card_color)
        requirements_frame.pack(fill="x", pady=(0, 15))

        self.req_labels = {}
        requirements = [
            ("At least 8 characters", "length"),
            ("At least one Upper character", "upper"),
            ("At least one Lower character", "lower"),
            ("At least one Special character", "special")
        ]

        for req, key in requirements:
            frame = Frame(requirements_frame, bg=self.card_color)
            frame.pack(anchor="w", pady=2)

            self.req_labels[key] = Label(frame, text="○", font=("Segoe UI", 10),
                                         bg=self.card_color, fg=self.text_secondary)
            self.req_labels[key].pack(side="left")

            Label(frame, text=req, font=("Segoe UI", 9),
                  bg=self.card_color, fg=self.text_secondary).pack(side="left", padx=(5, 0))

        self.signup_error = Label(form_frame, text="", font=("Segoe UI", 10),
                                  bg=self.card_color, fg=self.error_color)
        self.signup_error.pack(pady=(0, 5))

        signup_btn = Button(form_frame, text="Create Account", font=("Segoe UI", 12, "bold"),
                            bg=self.primary_color, fg="white", width=25,
                            relief="flat", cursor="hand2",
                            command=self.signup)
        signup_btn.pack(pady=(10, 15), ipady=10)

        signup_btn.bind('<Enter>', lambda e: signup_btn.config(bg=self.primary_hover))
        signup_btn.bind('<Leave>', lambda e: signup_btn.config(bg=self.primary_color))

        signin_frame = Frame(form_frame, bg=self.card_color)
        signin_frame.pack(pady=10)

        Label(signin_frame, text="Already have an account?", font=("Segoe UI", 10),
              bg=self.card_color, fg=self.text_secondary).pack(side="left")

        signin_btn = Label(signin_frame, text="Sign In", font=("Segoe UI", 10, "bold"),
                           bg=self.card_color, fg=self.primary_light, cursor="hand2")
        signin_btn.pack(side="left", padx=(5, 0))
        signin_btn.bind('<Button-1>', lambda e: self.show_login())
        signin_btn.bind('<Enter>', lambda e: signin_btn.config(fg=self.primary_color))
        signin_btn.bind('<Leave>', lambda e: signin_btn.config(fg=self.primary_light))

    def check_password_strength(self, event=None):
        password = self.signup_password.get()

        checks = {
            'length': len(password) >= 8,
            'upper': bool(re.search(r'[A-Z]', password)),
            'lower': bool(re.search(r'[a-z]', password)),
            'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        }

        for key, passed in checks.items():
            if passed:
                self.req_labels[key].config(text="●", fg=self.success_color)
            else:
                self.req_labels[key].config(text="○", fg=self.text_secondary)

    def check_password_match(self, event=None):
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()

        if confirm and password != confirm:
            self.signup_error.config(text="Passwords do not match!")
        elif confirm and password == confirm:
            self.signup_error.config(text="", fg=self.success_color)
        else:
            self.signup_error.config(text="")

    def check_username_exists(self, username):
        try:
            conn = sqlite3.connect("BookShopDB.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM Users WHERE username = ?", (username,))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except:
            return False

    def signup(self):
        username = self.signup_username.get().strip()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()

        if not username:
            self.signup_error.config(text="Username is required!")
            return

        if len(username) < 3:
            self.signup_error.config(text="Username must be at least 3 characters!")
            return

        if self.check_username_exists(username):
            self.signup_error.config(text="Username is already taken!")
            return

        if len(password) < 8:
            self.signup_error.config(text="Password must be at least 8 characters!")
            return

        if not re.search(r'[A-Z]', password):
            self.signup_error.config(text="Password must contain an uppercase letter!")
            return

        if not re.search(r'[a-z]', password):
            self.signup_error.config(text="Password must contain a lowercase letter!")
            return

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            self.signup_error.config(text="Password must contain a special character!")
            return

        if password != confirm:
            self.signup_error.config(text="Passwords do not match!")
            return

        try:
            conn = sqlite3.connect("BookShopDB.db")
            cursor = conn.cursor()
            hashed_password = self.hash_password(password)
            cursor.execute("""
            INSERT INTO Users (username, password, role, full_name)
            VALUES (?, ?, ?, ?)
            """, (username, hashed_password, "employee", username))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Account created successfully!\nPlease sign in.")
            self.show_login()

        except sqlite3.IntegrityError:
            self.signup_error.config(text="Username is already taken!")
        except Exception as e:
            self.signup_error.config(text=f"Error: {str(e)}")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return

        try:
            self.create_tables()
            conn = sqlite3.connect("BookShopDB.db")
            cursor = conn.cursor()
            hashed_password = self.hash_password(password)

            cursor.execute("""
            SELECT id, username, role FROM Users 
            WHERE username = ? AND password = ?
            """, (username, hashed_password))

            user = cursor.fetchone()
            conn.close()

            if user:
                user_id, username, role = user
                self.username = username
                self.user_role = role

                self.window.destroy()
                import dashboard
                dashboard.run_dashboard(username, role)
            else:
                messagebox.showerror("Error", "Invalid username or password!")

        except Exception as e:
            messagebox.showerror("Error", f"Login error: {str(e)}")

if __name__ == "__main__":
    app = LoginApp()