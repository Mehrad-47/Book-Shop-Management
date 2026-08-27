from ui_theme import apply_theme
from tkinter import Tk, Label, Button, Frame, messagebox, Toplevel, Entry
from tkinter.ttk import Treeview, Combobox
from datetime import datetime
import sqlite3
import hashlib

class DashboardApp:
    def __init__(self, username, role):
        self.window = Tk()
        apply_theme(self.window)
        self.window.title("Mehrad's Book Shop")
        self.window.geometry("1050x600")
        self.window.configure(bg="#F0F5E8")
        self.username = username
        self.role = role

        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

        self.primary_color = "#556B2F"
        self.primary_dark = "#3D4F23"
        self.primary_light = "#6B8E23"
        self.blue_color = "#2563EB"
        self.blue_hover = "#1D4ED8"
        self.brick_color = "#B22222"
        self.brick_hover = "#8B1A1A"
        self.success_color = "#4A7A2E"
        self.warning_color = "#B8860B"
        self.danger_color = "#8B3A3A"
        self.sales_color = "#4A7A2E"
        self.sales_hover = "#3D6B23"
        self.bg_color = "#F0F5E8"
        self.card_color = "#FAFCF7"
        self.text_color = "#2C3A1A"
        self.text_secondary = "#7A8C5A"

        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        header = Frame(self.window, bg=self.primary_color, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        Label(header, text="📚 Mehrad's Book Shop",
              font=("Segoe UI", 18, "bold"), bg=self.primary_color, fg="white").pack(side="left", padx=30, pady=20)

        role_text = "👑 Admin" if self.role == "admin" else "👤 Employee"
        Label(header, text=f"{role_text} | {self.username} | {datetime.now().strftime('%H:%M')}",
              font=("Segoe UI", 11), bg=self.primary_color, fg="#D4E8C4").pack(side="right", padx=30, pady=20)

        welcome_frame = Frame(self.window, bg=self.bg_color)
        welcome_frame.pack(fill="x", pady=20)

        welcome_text = "Welcome Admin!" if self.role == "admin" else "Welcome Employee!"
        Label(welcome_frame, text=welcome_text,
              font=("Segoe UI", 20, "bold"), bg=self.bg_color, fg=self.text_color).pack()
        Label(welcome_frame, text="Please select an option below to continue",
              font=("Segoe UI", 12), bg=self.bg_color, fg=self.text_secondary).pack(pady=5)

        main_frame = Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)

        screen_width = self.window.winfo_width()
        card_width = 320
        card_height = 320
        spacing = 50

        if self.role == "admin":
            total_width = (card_width * 2) + spacing
            start_x = (screen_width - total_width) // 2
            y_position = 20

            user_frame = self.create_card(
                main_frame,
                "👥",
                "User Management",
                "Manage employees, users and change passwords",
                self.blue_color,
                self.blue_hover,
                self.open_user_management,
                card_width,
                card_height
            )
            user_frame.place(x=start_x, y=y_position)

            library_frame = self.create_card(
                main_frame,
                "📚",
                "Library Management",
                "Manage books, authors, publishers, translators and genres",
                self.brick_color,
                self.brick_hover,
                self.open_library_panel,
                card_width,
                card_height
            )
            library_frame.place(x=start_x + card_width + spacing, y=y_position)

        else:
            total_width = (card_width * 2) + spacing
            start_x = (screen_width - total_width) // 2
            y_position = 20

            sales_frame = self.create_card(
                main_frame,
                "🛒",
                "Sales Panel",
                "Process customer sales, manage orders and handle transactions",
                self.sales_color,
                self.sales_hover,
                self.open_sales_panel,
                card_width,
                card_height
            )
            sales_frame.place(x=start_x, y=y_position)

            library_frame = self.create_card(
                main_frame,
                "📚",
                "Library Management",
                "Manage books, authors, publishers, translators and genres",
                self.brick_color,
                self.brick_hover,
                self.open_library_panel,
                card_width,
                card_height
            )
            library_frame.place(x=start_x + card_width + spacing, y=y_position)

        footer = Frame(self.window, bg=self.primary_color, height=40)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)

        Label(footer, text="© 2026 Mehrad's Book Shop | All rights reserved",
              font=("Segoe UI", 9), bg=self.primary_color, fg="#D4E8C4").pack(pady=10)

        logout_btn = Button(footer, text="🚪 Logout", font=("Segoe UI", 9),
                            bg=self.primary_color, fg="white", relief="flat",
                            cursor="hand2", command=self.logout)
        logout_btn.pack(side="right", padx=20)
        logout_btn.bind('<Enter>', lambda e: logout_btn.config(fg="#E8C4C4"))
        logout_btn.bind('<Leave>', lambda e: logout_btn.config(fg="white"))

    def create_card(self, parent, icon, title, description, color, hover_color, command, width, height):
        frame = Frame(parent, bg=self.card_color, relief="raised", bd=2, width=width, height=height)
        frame.pack_propagate(False)

        content = Frame(frame, bg=self.card_color)
        content.pack(fill="both", expand=True, padx=15, pady=15)

        icon_label = Label(content, text=icon, font=("Segoe UI", 45), bg=self.card_color)
        icon_label.pack(pady=(5, 2))

        title_label = Label(content, text=title, font=("Segoe UI", 18, "bold"),
                            bg=self.card_color, fg=color)
        title_label.pack(pady=(5, 5))

        desc_label = Label(content, text=description, font=("Segoe UI", 10),
                           bg=self.card_color, fg=self.text_secondary, justify="center", wraplength=280)
        desc_label.pack(pady=(5, 10))

        btn = Button(content, text=f"Open {title}",
                     font=("Segoe UI", 12, "bold"),
                     bg=color, fg="white",
                     relief="flat", padx=30, pady=10,
                     cursor="hand2",
                     command=command)
        btn.pack(pady=(5, 5))
        btn.bind('<Enter>', lambda e, b=btn: b.config(bg=hover_color))
        btn.bind('<Leave>', lambda e, b=btn: b.config(bg=color))

        return frame

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def open_user_management(self):
        if self.role != "admin":
            messagebox.showerror("Error", "Access denied! Only admin can manage users.")
            return

        user_window = Toplevel(self.window)
        user_window.title("User Management")
        user_window.geometry("900x550")
        user_window.configure(bg="#F0F5E8")
        user_window.transient(self.window)
        user_window.grab_set()

        user_window.update_idletasks()
        width = user_window.winfo_width()
        height = user_window.winfo_height()
        x = (user_window.winfo_screenwidth() // 2) - (width // 2)
        y = (user_window.winfo_screenheight() // 2) - (height // 2)
        user_window.geometry(f"{width}x{height}+{x}+{y}")

        header = Frame(user_window, bg=self.primary_color, height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        Label(header, text="👥 User Management", font=("Segoe UI", 14, "bold"),
              bg=self.primary_color, fg="white").pack(pady=12)

        main_frame = Frame(user_window, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tree_frame = Frame(main_frame, bg="white", relief="solid", bd=1)
        tree_frame.pack(fill="both", expand=True)

        from tkinter import Scrollbar
        scroll_y = Scrollbar(tree_frame)
        scroll_y.pack(side="right", fill="y")

        tree = Treeview(tree_frame, columns=("id", "username", "role", "full_name", "created_at"),
                        show="headings", yscrollcommand=scroll_y.set)
        scroll_y.config(command=tree.yview)

        tree.heading("id", text="ID")
        tree.heading("username", text="Username")
        tree.heading("role", text="Role")
        tree.heading("full_name", text="Full Name")
        tree.heading("created_at", text="Created At")

        tree.column("id", width=50)
        tree.column("username", width=150)
        tree.column("role", width=100)
        tree.column("full_name", width=200)
        tree.column("created_at", width=180)

        tree.pack(fill="both", expand=True, padx=5, pady=5)

        def load_users():
            for item in tree.get_children():
                tree.delete(item)

            conn = sqlite3.connect("BookShopDB.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role, full_name, created_at FROM Users ORDER BY id")
            rows = cursor.fetchall()
            conn.close()

            for row in rows:
                tree.insert("", "end", values=row)

        load_users()

        btn_frame = Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=10)

        def add_user():
            form = Toplevel(user_window)
            form.title("Add New User")
            form.geometry("450x400")
            form.configure(bg="#F0F5E8")
            form.transient(user_window)
            form.grab_set()

            form.update_idletasks()
            w = form.winfo_width()
            h = form.winfo_height()
            x = (form.winfo_screenwidth() // 2) - (w // 2)
            y = (form.winfo_screenheight() // 2) - (h // 2)
            form.geometry(f"{w}x{h}+{x}+{y}")

            hdr = Frame(form, bg=self.primary_color, height=45)
            hdr.pack(fill="x")
            hdr.pack_propagate(False)
            Label(hdr, text="➕ Add New User", font=("Segoe UI", 14, "bold"),
                  bg=self.primary_color, fg="white").pack(pady=10)

            main_f = Frame(form, bg="white")
            main_f.pack(fill="both", expand=True, padx=30, pady=20)

            Label(main_f, text="Username:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=0, column=0, pady=10, sticky="e")
            username_entry = Entry(main_f, font=("Segoe UI", 11), width=25,
                                   bg="#F8FAFC", relief="solid", bd=1)
            username_entry.grid(row=0, column=1, pady=10, padx=10)

            Label(main_f, text="Password:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=1, column=0, pady=10, sticky="e")
            password_entry = Entry(main_f, font=("Segoe UI", 11), width=25, show="•",
                                   bg="#F8FAFC", relief="solid", bd=1)
            password_entry.grid(row=1, column=1, pady=10, padx=10)

            Label(main_f, text="Full Name:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=2, column=0, pady=10, sticky="e")
            full_name_entry = Entry(main_f, font=("Segoe UI", 11), width=25,
                                    bg="#F8FAFC", relief="solid", bd=1)
            full_name_entry.grid(row=2, column=1, pady=10, padx=10)

            Label(main_f, text="Role:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=3, column=0, pady=10, sticky="e")
            role_combo = Combobox(main_f, values=["employee", "admin"],
                                  state="readonly", width=23, font=("Segoe UI", 11))
            role_combo.set("employee")
            role_combo.grid(row=3, column=1, pady=10, padx=10)

            def save_user():
                username = username_entry.get().strip()
                password = password_entry.get()
                full_name = full_name_entry.get().strip()
                role = role_combo.get()

                if not username or not password:
                    messagebox.showerror("Error", "Username and password are required!")
                    return

                if len(password) < 8:
                    messagebox.showerror("Error", "Password must be at least 8 characters!")
                    return

                try:
                    conn = sqlite3.connect("BookShopDB.db")
                    cursor = conn.cursor()
                    hashed = self.hash_password(password)
                    cursor.execute("""
                    INSERT INTO Users (username, password, role, full_name)
                    VALUES (?, ?, ?, ?)
                    """, (username, hashed, role, full_name if full_name else username))
                    conn.commit()
                    conn.close()

                    load_users()
                    form.destroy()
                    messagebox.showinfo("Success", "User added successfully!")
                except sqlite3.IntegrityError:
                    messagebox.showerror("Error", "Username already exists!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            btn_f = Frame(main_f, bg="white")
            btn_f.grid(row=4, column=0, columnspan=2, pady=20)

            Button(btn_f, text="💾 Save", command=save_user,
                   bg=self.success_color, fg="white", font=("Segoe UI", 11, "bold"),
                   relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)
            Button(btn_f, text="❌ Cancel", command=form.destroy,
                   bg=self.danger_color, fg="white", font=("Segoe UI", 11, "bold"),
                   relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)

        def edit_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a user to edit")
                return

            values = tree.item(selected[0], 'values')
            user_id = values[0]
            username = values[1]
            current_role = values[2]
            full_name = values[3] if values[3] else ""

            if username == "boss":
                messagebox.showerror("Error", "Cannot edit the admin user!")
                return

            form = Toplevel(user_window)
            form.title("Edit User")
            form.geometry("450x350")
            form.configure(bg="#F0F5E8")
            form.transient(user_window)
            form.grab_set()

            form.update_idletasks()
            w = form.winfo_width()
            h = form.winfo_height()
            x = (form.winfo_screenwidth() // 2) - (w // 2)
            y = (form.winfo_screenheight() // 2) - (h // 2)
            form.geometry(f"{w}x{h}+{x}+{y}")

            hdr = Frame(form, bg=self.primary_color, height=45)
            hdr.pack(fill="x")
            hdr.pack_propagate(False)
            Label(hdr, text="✏️ Edit User", font=("Segoe UI", 14, "bold"),
                  bg=self.primary_color, fg="white").pack(pady=10)

            main_f = Frame(form, bg="white")
            main_f.pack(fill="both", expand=True, padx=30, pady=20)

            Label(main_f, text="Username:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=0, column=0, pady=10, sticky="e")
            username_label = Label(main_f, text=username, font=("Segoe UI", 11, "bold"),
                                   bg="white", fg="#2C3A1A")
            username_label.grid(row=0, column=1, pady=10, padx=10, sticky="w")

            Label(main_f, text="Full Name:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=1, column=0, pady=10, sticky="e")
            full_name_entry = Entry(main_f, font=("Segoe UI", 11), width=25,
                                    bg="#F8FAFC", relief="solid", bd=1)
            full_name_entry.grid(row=1, column=1, pady=10, padx=10)
            full_name_entry.insert(0, full_name)

            Label(main_f, text="Role:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=2, column=0, pady=10, sticky="e")
            role_combo = Combobox(main_f, values=["employee", "admin"],
                                  state="readonly", width=23, font=("Segoe UI", 11))
            role_combo.set(current_role)
            role_combo.grid(row=2, column=1, pady=10, padx=10)

            def save_edit():
                full_name = full_name_entry.get().strip()
                role = role_combo.get()

                try:
                    conn = sqlite3.connect("BookShopDB.db")
                    cursor = conn.cursor()
                    cursor.execute("""
                    UPDATE Users SET full_name = ?, role = ? WHERE id = ?
                    """, (full_name if full_name else username, role, user_id))
                    conn.commit()
                    conn.close()

                    load_users()
                    form.destroy()
                    messagebox.showinfo("Success", "User updated successfully!")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

            btn_f = Frame(main_f, bg="white")
            btn_f.grid(row=3, column=0, columnspan=2, pady=20)

            Button(btn_f, text="💾 Save", command=save_edit,
                   bg=self.warning_color, fg="white", font=("Segoe UI", 11, "bold"),
                   relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)
            Button(btn_f, text="❌ Cancel", command=form.destroy,
                   bg=self.danger_color, fg="white", font=("Segoe UI", 11, "bold"),
                   relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)

        def delete_user():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a user to delete")
                return

            values = tree.item(selected[0], 'values')
            user_id = values[0]
            username = values[1]

            if username == "boss":
                messagebox.showerror("Error", "Cannot delete the admin user!")
                return

            if messagebox.askyesno("Confirm", f"Delete user '{username}'?"):
                conn = sqlite3.connect("BookShopDB.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
                conn.commit()
                conn.close()
                load_users()
                messagebox.showinfo("Success", "User deleted successfully!")

        def change_password():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a user")
                return

            values = tree.item(selected[0], 'values')
            user_id = values[0]
            username = values[1]

            form = Toplevel(user_window)
            form.title("Change Password")
            form.geometry("450x280")
            form.configure(bg="#F0F5E8")
            form.transient(user_window)
            form.grab_set()

            form.update_idletasks()
            w = form.winfo_width()
            h = form.winfo_height()
            x = (form.winfo_screenwidth() // 2) - (w // 2)
            y = (form.winfo_screenheight() // 2) - (h // 2)
            form.geometry(f"{w}x{h}+{x}+{y}")

            hdr = Frame(form, bg=self.primary_color, height=45)
            hdr.pack(fill="x")
            hdr.pack_propagate(False)
            Label(hdr, text=f"🔑 Change Password - {username}", font=("Segoe UI", 14, "bold"),
                  bg=self.primary_color, fg="white").pack(pady=10)

            main_f = Frame(form, bg="white")
            main_f.pack(fill="both", expand=True, padx=30, pady=20)

            Label(main_f, text="New Password:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=0, column=0, pady=10, sticky="e")
            password_entry = Entry(main_f, font=("Segoe UI", 11), width=25, show="•",
                                   bg="#F8FAFC", relief="solid", bd=1)
            password_entry.grid(row=0, column=1, pady=10, padx=10)

            Label(main_f, text="Confirm Password:", font=("Segoe UI", 10, "bold"),
                  bg="white", fg="#2C3A1A").grid(row=1, column=0, pady=10, sticky="e")
            confirm_entry = Entry(main_f, font=("Segoe UI", 11), width=25, show="•",
                                  bg="#F8FAFC", relief="solid", bd=1)
            confirm_entry.grid(row=1, column=1, pady=10, padx=10)

            def save_password():
                password = password_entry.get()
                confirm = confirm_entry.get()

                if not password:
                    messagebox.showerror("Error", "Password is required!")
                    return

                if len(password) < 8:
                    messagebox.showerror("Error", "Password must be at least 8 characters!")
                    return

                if password != confirm:
                    messagebox.showerror("Error", "Passwords do not match!")
                    return

                conn = sqlite3.connect("BookShopDB.db")
                cursor = conn.cursor()
                hashed = self.hash_password(password)
                cursor.execute("UPDATE Users SET password = ? WHERE id = ?", (hashed, user_id))
                conn.commit()
                conn.close()

                form.destroy()
                messagebox.showinfo("Success", "Password changed successfully!")

            btn_f = Frame(main_f, bg="white")
            btn_f.grid(row=2, column=0, columnspan=2, pady=20)

            Button(btn_f, text="💾 Save", command=save_password,
                   bg=self.success_color, fg="white", font=("Segoe UI", 11, "bold"),
                   relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)
            Button(btn_f, text="❌ Cancel", command=form.destroy,
                   bg=self.danger_color, fg="white", font=("Segoe UI", 11, "bold"),
                   relief="flat", padx=25, pady=8, cursor="hand2").pack(side="left", padx=10)

        Button(btn_frame, text="➕ Add User", command=add_user,
               bg=self.success_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="✏️ Edit User", command=edit_user,
               bg=self.warning_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="🗑️ Delete User", command=delete_user,
               bg=self.danger_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="🔑 Change Password", command=change_password,
               bg=self.primary_light, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

        Button(btn_frame, text="🔄 Refresh", command=load_users,
               bg=self.primary_color, fg="white", font=("Segoe UI", 10, "bold"),
               relief="flat", padx=15, pady=6, cursor="hand2").pack(side="left", padx=3)

    def open_sales_panel(self):
        self.window.destroy()
        import sales_panel
        sales_panel.run_sales_panel(self.username, self.role)

    def open_library_panel(self):
        self.window.destroy()
        import library_panel
        library_panel.run_library_panel(self.username, self.role)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.window.destroy()
            import login
            login.LoginApp()

def run_dashboard(username, role):
    DashboardApp(username, role)

if __name__ == "__main__":
    run_dashboard("admin", "admin")