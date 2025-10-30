# Expense Tracker Backend

A beginner-friendly backend project for tracking personal expenses, built with Python, FastAPI, and PostgreSQL. This project serves as a learning resource for understanding backend development concepts.

## Project Overview

This Expense Tracker allows users to:
- Create and manage their accounts
- Track their expenses by category
- Manage transactions with attached items
- Upload and manage transaction images via ImgBB
- Authenticate securely using JWT tokens

## Technical Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migration Tool**: Alembic
- **Authentication**: JWT (JSON Web Tokens)
- **Image Storage**: ImgBB API

## Project Structure

```
src/
├── config/                 # Configuration settings
│   ├── db.py              # Database configuration
│   └── rate_limit.py      # Rate limiting configuration
├── images/                # Image management
│   ├── image_controller.py
│   ├── image_model.py
│   ├── image_route.py
│   ├── image_schema.py
│   └── imgbb_service.py   # ImgBB API integration
├── transaction_items/     # Transaction items management
│   ├── transaction_items_controller.py
│   ├── transaction_items_model.py
│   ├── transaction_items_schema.py
│   └── transaction_items_routes.py
├── transactions/          # Transaction management
│   ├── transaction_controller.py
│   ├── transaction_model.py
│   ├── transaction_routes.py
│   └── transaction_schema.py
├── users/                 # User management
│   ├── user_controller.py
│   ├── user_model.py
│   ├── user_routes.py
│   └── user_schema.py
└── app.py                 # Main application entry point
```

## Key Features

1. **User Management**
   - User registration and authentication
   - Secure password hashing
   - JWT-based authentication
   - Token refresh mechanism
   - Token blacklisting for logout

2. **Transaction Management**
   - Create, read, update, and delete transactions
   - Categorize expenses
   - Track transaction amounts
   - Link transactions to specific users
   - Attach multiple items to transactions
   - Upload and associate images with transactions

3. **Image Management**
   - Upload images to ImgBB cloud storage
   - Upload images from URLs
   - Associate images with transactions
   - Delete images
   - Automatic image expiration support

4. **Security Features**
   - Password hashing
   - JWT authentication
   - Rate limiting
   - Token blacklisting
   - All endpoints require JWT authentication

## Database Models

### User Model
```python
class User:
    - user_id (UUID, primary key)
    - name (String)
    - email (String, unique)
    - password (String, hashed)
    - age (Integer, optional)
```

### Transaction Model
```python
class Transaction:
    - transaction_id (UUID, primary key)
    - name (String)
    - amount (Integer)
    - category (String)
    - user_id (UUID, foreign key)
    - items (relationship to TransactionItems)
    - images (relationship to Images)
```

### Transaction Items Model
```python
class TransactionItems:
    - item_id (UUID, primary key)
    - transaction_id (UUID, foreign key)
    - item_name (String)
    - item_quantity (Integer)
    - item_price (Float)
```

### Image Model
```python
class Image:
    - image_id (UUID, primary key)
    - transaction_id (UUID, foreign key)
    - imgbb_image_id (String)
    - display_url (String)
    - delete_url (String)
    - filename (String)
    - mime (String)
    - size (Integer)
    - expiration (Integer, optional)
```

## Getting Started

1. **Clone the repository**
```bash
git clone [repository-url]
cd ExpenseTracker
```

2. **Set up virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file with:
```
DATABASE_URL=postgresql://[username]:[password]@localhost:5432/expense_tracker
JWT_SECRET_KEY=[your-secret-key]
IMAGE_API_KEY=[your-imgbb-api-key]
```

To get an ImgBB API key, visit: https://imgbb.com/api

5. **Run migrations**
```bash
alembic upgrade head
```

6. **Start the server**
```bash
python server.py
```
or
```bash
uvicorn src.app:app --reload
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `POST /api/v1/auth/logout` - Logout user

### Transactions
- `POST /api/v1/transactions/` - Create transaction (supports multipart/form-data with images)
- `GET /api/v1/transactions/` - Get all transactions
- `GET /api/v1/transactions/{transaction_id}` - Get specific transaction
- `PUT /api/v1/transactions/{transaction_id}` - Update transaction
- `DELETE /api/v1/transactions/{transaction_id}` - Delete transaction

### Transaction Items
- `POST /api/v1/transaction-items/` - Create transaction item
- `GET /api/v1/transaction-items/` - Get all items
- `GET /api/v1/transaction-items/{item_id}` - Get specific item
- `PUT /api/v1/transaction-items/{item_id}` - Update item
- `DELETE /api/v1/transaction-items/{item_id}` - Delete item

### Images
- `POST /api/v1/images/upload` - Upload image file
- `POST /api/v1/images/upload-url` - Upload image from URL
- `GET /api/v1/images/{image_id}` - Get image details
- `GET /api/v1/images/transaction/{transaction_id}` - Get all images for a transaction
- `DELETE /api/v1/images/{image_id}` - Delete image

## Learning Objectives

This project demonstrates:
- RESTful API design principles
- Database modeling and relationships
- Authentication and authorization
- Password security
- Migration management
- Rate limiting
- Error handling
- Service layer architecture
- Third-party API integration (ImgBB)
- Multipart form data handling

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation at: `http://localhost:8000/docs`
- ReDoc documentation at: `http://localhost:8000/redoc`
