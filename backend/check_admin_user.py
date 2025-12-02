from app import create_app, db
from models import User

def check_admin_user():
    app = create_app()
    with app.app_context():
        admin = User.query.filter_by(email='adminpiyush123@gmail.com').first()
        if admin:
            print("Admin user found in database:")
            print(f"Email: {admin.email}")
            print(f"Is Admin: {admin.is_admin}")
            # Verify the password hash can be verified (we'll need to test login to verify the actual password)
            print("\nTo verify login, try these steps:")
            print("1. Make sure backend is running on http://localhost:5001")
            print("2. Try logging in with:")
            print("   Email: adminpiyush123@gmail.com")
            print("   Password: RamShyam@123")
            print("\nIf login still fails, you may need to:")
            print("1. Delete the database file (instance/anilsteel.db)")
            print("2. Run `python init_db.py` to recreate the database")
            print("3. Run `python create_admin.py` to create the admin user")
        else:
            print("No admin user found with email 'adminpiyush123@gmail.com'")
            print("\nPlease run 'python create_admin.py' to create the admin user")

if __name__ == '__main__':
    check_admin_user()
