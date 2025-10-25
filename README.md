# Expense Tracker Backend

A beginner-friendly backend project for tracking personal expenses, built with Python, FastAPI, and PostgreSQL. This project serves as a learning resource for understanding backend development concepts.

## Project Overview

This Expense Tracker allows users to:
- Create and manage their accounts
- Track their expenses by category
- Manage transactions
- Authenticate securely using JWT tokens

## Technical Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migration Tool**: Alembic
- **Authentication**: JWT (JSON Web Tokens)

## Project Structure

```
src/
├── app.py                  # Main application entry point
├── config/                 # Configuration settings
│   ├── db.py              # Database configuration
│   └── rate_limit.py      # Rate limiting configuration
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
│   ├── core/             # Core functionalities
│   │   ├── jwt_token.py
│   │   └── user_password_hash.py
│   └── services/         # Business logic services
└── utils/                # Utility functions
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

3. **Security Features**
   - Password hashing
   - JWT authentication
   - Rate limiting
   - Token blacklisting

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
```

5. **Run migrations**
```bash
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn src.app:app --reload
```

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

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation at: `http://localhost:8000/docs`
- ReDoc documentation at: `http://localhost:8000/redoc`
