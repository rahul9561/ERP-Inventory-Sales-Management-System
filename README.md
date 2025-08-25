# ERP Inventory & Sales Management System  

An open-source **ERP Inventory & Sales Management System** built with **Django** and **Django REST Framework**.  
This project provides an all-in-one solution for managing **Products, Customers, and Sales**, along with **User Authentication, Role-based Access, and APIs**.  

---

## ✨ Features  

✅ **Product Management** – Add, update, delete, and list products with stock tracking.  
✅ **Customer Management** – Manage customer records with name, email, and phone.  
✅ **Sales Management** – Track sales with product, quantity, total price, and date.  
✅ **User Authentication** – Register, Login with **JWT Tokens**.  
✅ **Role-based Access Control (RBAC)** – Admin, Manager, and Staff roles.  
✅ **REST API** – CRUD APIs for products, customers, and sales.  
✅ **Admin Dashboard** – Manage everything with Django Admin.  
✅ **Open Source** – Free to use, extend, and customize.  

---

## 🛠️ Tech Stack  

- **Backend:** Django, Django REST Framework  
- **Database:** SQLite (default), supports PostgreSQL/MySQL  
- **Authentication:** JWT (JSON Web Tokens)  
- **Deployment Ready:** Gunicorn + Nginx (Linux)  

---

## 📂 Project Structure  


ERP-Inventory-Sales-Management-System/
│── ERP_app/ # Main application (models, views, serializers, urls)
│ ├── models.py # Product, Customer, Sales models
│ ├── views.py # API Views (CRUD + Auth)
│ ├── serializers.py # DRF serializers
│ ├── urls.py # API routes
│ ├── admin.py # Admin panel customization
│── ERP_project/ # Django project configs (settings, urls, wsgi)
│── manage.py # Django management script
│── requirements.txt # Dependencies
│── README.md # Project documentation



---

## 🚀 Installation & Setup  

### 1️⃣ Clone the Repository  
```bash

git clone https://github.com/rahul9561/ERP-Inventory-Sales-Management-System.git
cd ERP-Inventory-Sales-Management-System


2️⃣ Create Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt


3️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate

4️⃣ Create Superuser
python manage.py createsuperuser

Server will start at: http://127.0.0.1:8000/
