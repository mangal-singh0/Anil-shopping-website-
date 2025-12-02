from app import create_app, db
from models import User, Product, Category, ProductImage
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()
    
    if User.query.first():
        print("Database already seeded.")
        exit()

    print("Seeding database...")
    
    # Users
    admin = User(
        name='Admin User',
        email='admin@example.com',
        password_hash=generate_password_hash('Admin123!'),
        phone='1234567890',
        is_admin=True
    )
    
    user = User(
        name='Normal User',
        email='user@example.com',
        password_hash=generate_password_hash('User123!'),
        phone='0987654321',
        is_admin=False
    )
    
    db.session.add(admin)
    db.session.add(user)
    
    # Categories
    cat1 = Category(name='Construction Steel', slug='construction-steel')
    cat2 = Category(name='Sheets & Plates', slug='sheets-plates')
    cat3 = Category(name='Pipes & Tubes', slug='pipes-tubes')
    
    db.session.add_all([cat1, cat2, cat3])
    db.session.commit() # Commit to get IDs
    
    # Products
    products = [
        Product(name='MS Rod 8mm', slug='ms-rod-8mm', description='High quality Mild Steel Rod, 8mm diameter.', price=450.00, category_id=cat1.id, stock=100, image_url='https://placehold.co/600x400?text=MS+Rod+8mm'),
        Product(name='TMT Bar 10mm', slug='tmt-bar-10mm', description='Thermo Mechanically Treated bars for superior strength.', price=550.00, category_id=cat1.id, stock=200, image_url='https://placehold.co/600x400?text=TMT+Bar+10mm'),
        Product(name='Steel Sheet 3mm x 4ft', slug='steel-sheet-3mm', description='Cold rolled steel sheet, 3mm thickness.', price=1200.00, category_id=cat2.id, stock=50, image_url='https://placehold.co/600x400?text=Steel+Sheet+3mm'),
        Product(name='Mild Steel Plate 6mm', slug='ms-plate-6mm', description='Heavy duty MS Plate for industrial use.', price=2500.00, category_id=cat2.id, stock=30, image_url='https://placehold.co/600x400?text=MS+Plate+6mm'),
        Product(name='Stainless Steel Coil 304', slug='ss-coil-304', description='Premium grade 304 Stainless Steel Coil.', price=5000.00, category_id=cat2.id, stock=10, image_url='https://placehold.co/600x400?text=SS+Coil+304'),
        Product(name='Angle Iron 50x50', slug='angle-iron-50x50', description='Structural steel angle iron.', price=800.00, category_id=cat1.id, stock=150, image_url='https://placehold.co/600x400?text=Angle+Iron+50x50'),
        Product(name='Channel Steel 100', slug='channel-steel-100', description='U-channel steel for construction.', price=1500.00, category_id=cat1.id, stock=80, image_url='https://placehold.co/600x400?text=Channel+Steel+100'),
        Product(name='Round Bar 12mm', slug='round-bar-12mm', description='Solid steel round bar, 12mm.', price=600.00, category_id=cat1.id, stock=120, image_url='https://placehold.co/600x400?text=Round+Bar+12mm')
    ]
    
    db.session.add_all(products)
    db.session.commit()
    
    print("Database seeded successfully!")
