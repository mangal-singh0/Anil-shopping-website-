from app import create_app, db
from models import User
from werkzeug.security import generate_password_hash

def update_admin_password():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(email='adminpiyush123@gmail.com').first()
        if admin:
            # Update the password
            admin.password_hash = generate_password_hash('RamShyam@123')
            admin.is_admin = True
            db.session.commit()
            print("Admin password has been updated successfully!")
            print("Email: adminpiyush123@gmail.com")
            print("Password: RamShyam@123")
        else:
            print("Admin user not found. Creating a new admin user...")
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

if __name__ == '__main__':
    update_admin_password()
