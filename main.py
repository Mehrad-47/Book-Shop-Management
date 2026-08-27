# main.py
from tkinter import Tk, Label, Button, Frame, messagebox
import sys


class BookShopApp:
    def __init__(self):
        self.window = Tk()
        self.window.title("Book Shop Management System")
        self.window.geometry("600x400")
        self.window.resizable(False, False)
        self.window.configure(bg="#f0f4f8")

        title_label = Label(
            self.window,
            text="Book Shop Management System",
            font=("Arial", 20, "bold"),
            bg="#f0f4f8",
            fg="#2c3e50"
        )
        title_label.pack(pady=40)

        subtitle_label = Label(
            self.window,
            text="Please select one of the options below:",
            font=("Arial", 12),
            bg="#f0f4f8",
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=10)

        button_frame = Frame(self.window, bg="#f0f4f8")
        button_frame.pack(pady=50)

        library_btn = Button(
            button_frame,
            text="Library Management",
            font=("Arial", 14),
            width=20,
            height=2,
            bg="#3498db",
            fg="white",
            relief="raised",
            bd=3,
            cursor="hand2",
            command=self.open_library_panel
        )
        library_btn.pack(pady=15)

        sales_btn = Button(
            button_frame,
            text="Sales Panel",
            font=("Arial", 14),
            width=20,
            height=2,
            bg="#2ecc71",
            fg="white",
            relief="raised",
            bd=3,
            cursor="hand2",
            command=self.open_sales_panel
        )
        sales_btn.pack(pady=15)

        exit_btn = Button(
            self.window,
            text="Exit",
            font=("Arial", 10),
            width=10,
            bg="#e74c3c",
            fg="white",
            relief="raised",
            bd=2,
            cursor="hand2",
            command=self.exit_app
        )
        exit_btn.pack(pady=30)

        footer_label = Label(
            self.window,
            text="Version 2.0",
            font=("Arial", 8),
            bg="#f0f4f8",
            fg="#bdc3c7"
        )
        footer_label.pack(side="bottom", pady=10)

        self.window.mainloop()

    def open_library_panel(self):
        try:
            self.window.destroy()
            import library_panel
            library_panel.run_library_panel()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening library panel: {str(e)}")

    def open_sales_panel(self):
        try:
            self.window.destroy()
            import sales_panel
            sales_panel.run_sales_panel()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening sales panel: {str(e)}")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.window.quit()
            self.window.destroy()
            sys.exit()


if __name__ == "__main__":
    # اجرای login اولیه
    import login

    login.LoginApp()