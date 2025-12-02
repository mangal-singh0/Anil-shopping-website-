# Anil Steel - E-commerce Application

A full-stack e-commerce application for selling steel products, built with Flask (Backend) and React (Frontend).

## Tech Stack

- **Backend**: Flask, SQLAlchemy, MySQL, Flask-JWT-Extended
- **Frontend**: React, Tailwind CSS, Framer Motion, Axios
- **Database**: MySQL 8.0
- **Containerization**: Docker, Docker Compose

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
   docker-compose up --build
   ```
   This will start:
   - MySQL Database on port 3306
   - Backend API on http://localhost:5000
   - Frontend App on http://localhost:3000

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

## Notes

- **Images**: Uploaded images are stored in `backend/uploads` and served via the `/uploads` endpoint.
- **Payment**: Checkout is simulated; no real payment gateway is integrated.
