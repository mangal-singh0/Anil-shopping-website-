from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash

def create_admin_user():
    app = create_app()
    with app.app_context():
        # Check if admin already exists
        # First, check if the new admin email already exists
        admin = User.query.filter_by(email='adminpiyush123@gmail.com').first()
        if not admin:
            admin = User(
                name='Admin Piyush',
                email='adminpiyush123@gmail.com',
                password_hash=generate_password_hash('RamShyam@123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
            print("Email: adminpiyush123@gmail.com")
            print("Password: RamShyam@123")
        else:
            # If admin exists, update the password and ensure is_admin is True
            admin.password_hash = generate_password_hash('RamShyam@123')
            admin.is_admin = True
            db.session.commit()
            print("Admin user updated with new credentials!")
            print("Email: adminpiyush123@gmail.com")
            print("Password: RamShyam@123")

if __name__ == '__main__':
    create_admin_user()
