# Anil Steel - E-commerce Application

A full-stack e-commerce application for selling steel products, built with Flask (Backend) and React (Frontend).

## Tech Stack

- **Backend**: Flask, SQLAlchemy, MySQL, Flask-JWT-Extended
- **Frontend**: React, Tailwind CSS, Framer Motion, Axios
- **Database**: MySQL 8.0
- **Containerization**: Docker, Docker Compose

## Admin Access

### Default Admin Credentials
- **Email**: adminpiyush123@gmail.com
- **Password**: RamShyam@123

### Admin Commands

#### Create/Update Admin User
To create or update an admin user, run:

```bash
# Navigate to backend directory
cd backend

# Create/Update admin user
python create_admin.py
```

This script will:
- Create a new admin user if one doesn't exist
- Update the password if the admin user already exists
- Ensure the admin flag is set to True

#### Reset Admin Password
To reset the admin password, you can either:
1. Run the `create_admin.py` script which will reset the password to 'RamShyam@123'
2. Or update the password directly in the database by setting the `password_hash` field for the admin user

## Prerequisites

- Docker and Docker Compose installed on your machine.

## Setup & Running

1. **Clone the repository** (if not already done).

2. **Environment Variables**:
   The project comes with default configuration for development in `docker-compose.yml`.
   - Database: `anilsteel`
   - User: `root`
   - Password: `root123`
   - JWT Secret: `super-secret-key-change-me`

3. **Run with Docker Compose**:
   ```bash
   # Start all services (MySQL, Backend, Frontend)
   docker-compose up --build
   ```
   This will start:
   - MySQL Database on port 3306
   - Backend API on http://localhost:5000
   - Frontend App on http://localhost:3000

### Running Services Separately

#### Backend (Flask)

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Run the Flask development server
flask run --port=5000
```

#### Frontend (React)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm start
# This will start the frontend on http://localhost:3000
```

#### Database (MySQL)

If you're not using Docker, you'll need to set up MySQL manually:

1. Install MySQL 8.0
2. Create a database named `anilsteel`
3. Update the database configuration in `backend/config.py` if needed

4. **Database Initialization**:
   The `mysql-init.sql` script is automatically executed on the first run of the database container. It creates the schema and seeds sample data.

   **Sample Users**:
   - Admin: `admin@example.com` / `Admin123!` (Note: Password hash in seed might need update if login fails, register a new user for testing)
   - User: `user@example.com` / `User123!`

## API Documentation

### Auth
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user profile
- `GET /api/auth/users` - List all users (Admin only)
- `PUT /api/auth/users/<id>/role` - Update user role (Admin only)
- `DELETE /api/auth/users/<id>` - Delete user (Admin only)

### Products
- `GET /api/products` - List products (filters: search, category, min_price, max_price)
- `GET /api/products/<id>` - Get product details
- `POST /api/products` - Create product (Admin only, multipart/form-data)
- `PUT /api/products/<id>` - Update product (Admin only)
- `DELETE /api/products/<id>` - Delete product (Admin only)

### Cart
- `GET /api/cart` - Get user cart
- `POST /api/cart` - Add item to cart
- `PUT /api/cart/<item_id>` - Update item quantity
- `DELETE /api/cart/<item_id>` - Remove item

### Orders
- `POST /api/orders` - Place an order
- `GET /api/orders` - List user orders
- `GET /api/orders/<id>` - Get order details

### Reviews
- `POST /api/products/<id>/reviews` - Add a review
- `GET /api/products/<id>/reviews` - List reviews

## Project Structure

```
/
├── backend/            # Flask Application
│   ├── app.py         # App factory & config
│   ├── models.py      # Database models
│   ├── routes/        # API endpoints
│   └── uploads/       # Image storage
├── frontend/           # React Application
│   ├── src/
│   │   ├── components/# UI Components
│   │   ├── context/   # Auth & Cart Context
│   │   └── pages/     # Application Pages
├── docker-compose.yml # Docker orchestration
└── mysql-init.sql     # Database schema & seed
```

## Admin Features

1. **User Management**
   - View all registered users
   - Update user roles (admin/user)
   - Delete users

2. **Product Management**
   - Add/Edit/Delete products
   - Manage product categories
   - Update product inventory

3. **Order Management**
   - View all orders
   - Update order status
   - Process refunds

## Notes

- **Images**: Uploaded images are stored in `backend/uploads` and served via the `/uploads` endpoint.
- **Payment**: Checkout is simulated; no real payment gateway is integrated.
- **Security**: Admin routes are protected and require admin privileges to access.
