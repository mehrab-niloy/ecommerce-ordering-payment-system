# E-commerce Ordering & Payment System

A RESTful backend application built with **Django** and **Django REST Framework (DRF)** for managing users, products, orders, and payments. The project includes **JWT Authentication**, **Stripe Payment Gateway Integration**, **Role-Based Authorization**, and **Order Management** with automatic stock updates after successful payment.

---

# Features

### User Management

* User Registration
* User Login using JWT Authentication
* Email-based Login
* Secure Protected APIs

### Product & Category Management

* Product Category CRUD
* Product CRUD
* Admin-only Create, Update & Delete
* Public Product Listing
* Product Details API

### Order Management

* Create Orders
* Multiple Products per Order
* Automatic Subtotal Calculation
* Automatic Total Amount Calculation
* Order Status Management

### Payment Integration

* Stripe Payment Intent
* Stripe Webhook
* Payment Verification
* Payment Status Tracking
* Automatic Order Status Update

### Inventory Management

* Automatic Stock Reduction after Successful Payment
* Race Condition Handling using:

  * `transaction.atomic()`
  * `select_for_update()`
  * `F()` Expressions

### Security

* JWT Authentication
* Role-Based Authorization
* Admin-only Product & Category Management
* Environment Variables for Sensitive Keys

---

# Technology Stack

* Python 3.x
* Django 5.2.16
* Django REST Framework 3.17.1
* MySQL
* Stripe API
* Simple JWT
* Postman

---

# Project Structure

```text
Ecommerce_backend/
│
├── ecommerce_backend/
├── ecommerce_app/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
└── .env.example
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/mehrab-niloy/ecommerce-ordering-payment-system.git
```

```bash
cd ecommerce-ordering-payment-system
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---





---

# Database Setup

Run migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

Create Superuser

```bash
python manage.py createsuperuser
```

Run Server

```bash
python manage.py runserver
```

---

# API Endpoints

## Authentication

| Method | Endpoint     | Description   |
| ------ | ------------ | ------------- |
| POST   | `/register/` | Register User |
| POST   | `/login/`    | User Login    |

---

## Category APIs

| Method | Endpoint                      |
| ------ | ----------------------------- |
| GET    | `/add-display-main-category/` |
| POST   | `/add-display-main-category/` |
| GET    | `/main-category/<id>/`        |
| PUT    | `/main-category/<id>/`        |
| DELETE | `/main-category/<id>/`        |

---

## Product APIs

| Method | Endpoint                |
| ------ | ----------------------- |
| GET    | `/add-display-product/` |
| POST   | `/add-display-product/` |
| GET    | `/product/<id>/`        |
| PUT    | `/product/<id>/`        |
| DELETE | `/product/<id>/`        |

---

## Order APIs

| Method | Endpoint  |
| ------ | --------- |
| POST   | `/order/` |

---

## Payment APIs

| Method | Endpoint                    |
| ------ | --------------------------- |
| POST   | `/payments/create/`         |
| POST   | `/payments/webhook/stripe/` |

---

# Authentication

This project uses **JWT Authentication**.

Add the access token in the request header:

```text
Authorization: Bearer <access_token>
```

---

# User Roles

## Admin

* Manage Categories
* Manage Products
* View Products
* View Orders

## User

* Register
* Login
* View Products
* Create Orders
* Make Payments

---

# Payment Flow

1. User creates an order.
2. Order status becomes **Pending**.
3. User initiates Stripe payment.
4. Stripe creates a Payment Intent.
5. User completes payment.
6. Stripe sends a webhook event.
7. Payment status updates to **Success**.
8. Order status updates to **Paid**.
9. Product stock is automatically reduced.

---

# Race Condition Handling

To prevent overselling during concurrent purchases, the project uses:

* `transaction.atomic()`
* `select_for_update()`
* `F()` Expressions

These ensure safe inventory updates during successful payments.

---

# Testing

The project has been tested using:

* Postman
* Django Admin
* Stripe Test Mode
* Stripe Webhooks

Verified functionality includes:

* User Registration
* Login
* Category CRUD
* Product CRUD
* Order Creation
* Stripe Payment
* Payment Success
* Webhook Processing
* Stock Reduction

---

# Future Improvements

* bKash Payment Integration
* Redis Caching
* Swagger/OpenAPI Documentation
* Docker Deployment
* Unit Testing
* API Test Automation
* Cloud Deployment

---

# Author

**Md Niloy**

Backend Developer

---

# License

This project was developed as part of a Backend Engineer Assessment and is intended for educational and evaluation purposes.
