from tkinter.ttk import Style

def apply_theme(window):
    window.option_add("*Font", ("Segoe UI", 10))
    window.option_add("*Button.Cursor", "hand2")
    window.option_add("*Entry.Font", ("Segoe UI", 10))

    style = Style(window)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    olive_green = "#556B2F"
    olive_card = "#FAFCF7"
    olive_text = "#2C3A1A"

    style.configure(
        "Treeview",
        background=olive_card,
        foreground=olive_text,
        fieldbackground=olive_card,
        rowheight=32,
        borderwidth=0,
        font=("Segoe UI", 10),
    )
    style.configure(
        "Treeview.Heading",
        background=olive_green,
        foreground="#FFFFFF",
        relief="flat",
        font=("Segoe UI Semibold", 10),
        padding=(8, 8),
    )
    style.map("Treeview", background=[("selected", "#D4E8C4")], foreground=[("selected", olive_text)])
    style.configure("TCombobox", fieldbackground=olive_card, background=olive_card,
                    foreground=olive_text, padding=6, arrowsize=14)
    style.map("TCombobox", fieldbackground=[("readonly", olive_card)])