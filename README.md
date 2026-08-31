# 📚 Mehrad's Book Shop Management System

A desktop bookstore management application built with **Python, Tkinter, and SQLite3**.

The system provides role-based access for **Administrators** and **Employees**, with dedicated functionality for library management, user management, sales, and customer management.

## ✨ Features

### 🔐 Authentication & Authorization

* User login system
* Password hashing with SHA-256
* Role-based access control
* Admin and Employee roles
* User registration and management
* Password management
* Secure logout

### 📚 Library Management

Available to both **Admin** and **Employee** users.

* Add, edit, and delete books
* Manage authors
* Manage publishers
* Manage translators
* Manage genres
* Search and filter books
* ISBN management
* Purchase and selling price management
* Inventory and stock management
* Profit calculation
* Detailed book information

### 🛒 Sales Management

Available to **Employee** users.

* Customer selection
* Shopping cart
* Real-time order total calculation
* Automatic stock deduction
* Loyalty points calculation
* Sales transaction management

### 👥 Customer Management

Available to **Employee** users.

* Register customers
* Edit customer information
* Store customer birth dates
* Manage loyalty points
* Customer information management

### 👤 User Management

Available to **Admin** users only.

* Add system users
* Edit user information
* Delete users
* Assign user roles
* Change user passwords
* Manage Admin and Employee accounts

## 🛡️ Role-Based Access Control

The application separates administrative responsibilities from day-to-day bookstore operations.

| Feature                | Admin | Employee |
| ---------------------- | :---: | :------: |
| 📚 Library Management  |   ✅   |     ✅    |
| 👤 User Management     |   ✅   |     ❌    |
| 🛒 Sales Management    |   ❌   |     ✅    |
| 👥 Customer Management |   ❌   |     ✅    |

### Admin

Administrators have access to:

* Library Management
* User Management

### Employee

Employees have access to:

* Library Management
* Sales Management
* Customer Management

## 🎨 User Interface

The application uses a custom **Olive Green** theme for a clean and consistent desktop interface.

| Element        | Color     |
| -------------- | --------- |
| Primary        | `#556B2F` |
| Primary Dark   | `#3D4F23` |
| Primary Light  | `#6B8E23` |
| Success        | `#4A7A2E` |
| Warning        | `#B8860B` |
| Danger         | `#8B3A3A` |
| Background     | `#F0F5E8` |
| Card           | `#FAFCF7` |
| Text Primary   | `#2C3A1A` |
| Text Secondary | `#7A8C5A` |

## 🛠️ Tech Stack

| Component          | Technology                  |
| ------------------ | --------------------------- |
| **Language**       | Python 3.x                  |
| **GUI Framework**  | Tkinter / ttk               |
| **Database**       | SQLite3                     |
| **Authentication** | SHA-256                     |
| **Architecture**   | Object-Oriented Programming |

## 🗄️ Database

The application uses **SQLite3** for local data persistence.

### Main Entities

* **User** — System users and roles
* **Book** — Book information, pricing, and inventory
* **Author** — Book authors
* **Publisher** — Publishing companies
* **Translator** — Book translators
* **Genre** — Book categories
* **Customer** — Customer information and loyalty points
* **Sale** — Sales transactions
* **SaleItem** — Individual items within a sale

## 📁 Project Structure

```text
Book-Shop-Management/
│
├── DataAccess/
├── Entities/
│
├── dashboard.py
├── library_panel.py
├── login.py
├── main.py
├── sales_panel.py
├── ui_theme.py
│
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Installation

### Requirements

* Python **3.8 or higher**
* Git *(optional)*

### 1. Clone the Repository

```bash
git clone https://github.com/Mehrad-47/Book-Shop-Management.git
cd Book-Shop-Management
```

### 2. Run the Application

```bash
python main.py
```

## 🔑 Default Login

```text
Username: boss
Password: Bookshopboss@123
```

> ⚠️ The default credentials are provided for demonstration purposes. Change the password before using the application in a real environment.

## 💡 Concepts Demonstrated

This project demonstrates practical concepts in:

* Object-Oriented Programming
* Desktop GUI development
* SQLite database management
* Relational database design
* CRUD operations
* Authentication and authorization
* Role-based access control
* Inventory management
* Sales processing
* Customer management
* Input validation
* Database relationships
* Application state management

## 🔮 Future Improvements

* 🔲 Sales reports and analytics
* 🔲 Advanced dashboard statistics
* 🔲 Barcode scanner integration
* 🔲 Book import/export
* 🔲 Low-stock notifications
* 🔲 Automated database backup
* 🔲 PDF invoice generation
* 🔲 Advanced reporting

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository
2. Create a feature branch:

```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes:

```bash
git commit -m "Add AmazingFeature"
```

4. Push your branch:

```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request.

## 📄 License

This project is licensed under the **MIT License**.

## 👤 Author

**Mehrad Chenari**

* GitHub: [@Mehrad-47](https://github.com/Mehrad-47)
* LinkedIn: [Mehrad Chenari](https://www.linkedin.com/in/mehrad-chenari-676585361/)

---

⭐ **If you find this project useful, consider giving it a star!**
