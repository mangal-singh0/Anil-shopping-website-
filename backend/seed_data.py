from app import create_app
from extensions import db
from models import User, Product, Order, OrderItem, Cart, CartItem, Category
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # 0. Create Category
    category = Category.query.filter_by(name='Construction').first()
    if not category:
        category = Category(name='Construction', slug='construction')
        db.session.add(category)
        db.session.commit()
        print(f"Created category: {category.name}")

    # 1. Create a Product
    product = Product.query.first()
    if not product:
        product = Product(
            name='Test Steel Beam',
            description='High quality steel beam',
            price=1000.00,
            stock=100,
            category_id=category.id,
            image_url='/uploads/test.jpg',
            slug='test-steel-beam'
        )
        db.session.add(product)
        db.session.commit()
        print(f"Created product: {product.name}")
    else:
        print(f"Product exists: {product.name}")

    # 2. Create a User
    user = User.query.filter_by(email='customer@test.com').first()
    if not user:
        user = User(
            name='Test Customer',
            email='customer@test.com',
            password_hash=generate_password_hash('password123'),
            phone='1234567890'
        )
        db.session.add(user)
        db.session.commit()
        print(f"Created user: {user.email}")
    else:
        print(f"User exists: {user.email}")

    # 3. Create an Order
    order = Order(
        user_id=user.id,
        total_amount=2000.00,
        shipping_name='Test Customer',
        shipping_phone='1234567890',
        shipping_address='123 Test St, Test City',
        status='Placed'
    )
    db.session.add(order)
    db.session.flush()

    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=2,
        unit_price=1000.00
    )
    db.session.add(order_item)
    db.session.commit()
    print(f"Created order #{order.id}")
