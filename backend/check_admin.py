from app import create_app, db
from models import User

def check_admin():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin:
            print(f"Admin user found!")
            print(f"Name: {admin.name}")
            print(f"Email: {admin.email}")
            print(f"Is Admin: {admin.is_admin}")
            return True
        else:
            print("No admin user found with email 'admin@example.com'")
            return False

if __name__ == "__main__":
    check_admin()
