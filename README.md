# Inventory Management System

This project is an Inventory Management System built using Django and Django REST Framework. It includes user authentication, product management, and order management functionalities.

## Features

- User Signup and Login
- Admin Login
- Product Listing, 
- Product Creation, Update, and Deletion (Admin Only)
- Order Creation
- Low Stock Report (Admin Only)
- Sales Report (Admin Only)

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework
- SQLite (or any other preferred database)

## Setup Instructions

### 1. Clone the Repository


git clone https://github.com/JoelInyang/Inventory.git

### 2. Create and Activate a Virtual Environment

- python -m venv venv
- source venv/bin/activate or if you are On Windows, use `venv\Scripts\activate`


#### 3. Install Dependencies

pip install -r requirements.txt ### There you will find all the dependencies needed.


### 4. Configure the Database
Open settings.py and update the DATABASES configuration with your database credentials. For PostgreSQL, it might look like:

if you are using postgreSQL:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'yourdbname',
                'USER': 'yourdbuser',
                'PASSWORD': 'yourdbpassword',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }

else if you are using SQLite:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }

### 5. Apply Migrations

- python manage.py makemigrations
- python manage.py migrate

### 6. Create a Superuser

- python manage.py createsuperuser (this is for creating an admin)


### 7. Run the Development Server

- python manage.py runserver

The application should now be running at http://127.0.0.1:8000/



API ENDPOINTS

Authentication
- User Signup: POST /signup/
- User Login: POST /login/
- Admin Login: POST /admin-login/
- Logout: POST /logout/

Products
- List Products: GET /products/
- Create Product: POST /products-create/ (Admin Only)
- Update Product: PUT /products-update/<id>/ (Admin Only)
- Delete Product: DELETE /products-delete/<id>/ (Admin Only)

Orders
- Create Order: POST /orders-create/
- Update Order Status: PUT /orders-update-status/<id>/ (Admin Only)

Reports (Admin Only)
- Low Stock Report: GET /low-stock-report/
- Sales Report: GET /sales-report/ (with period query parameter: day, week, month)


API DOCUMENTATION : https://documenter.getpostman.com/view/25490489/2sA3dxDXAc/ 


Running Tests

To run the tests, execute:
- python manage.py test


Project Structure

Inventory/
│
├── InventApp/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── inventory/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md

