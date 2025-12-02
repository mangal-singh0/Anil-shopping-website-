from flask import Flask, send_from_directory, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import extensions
from extensions import db, jwt

def create_app():
    app = Flask(__name__)
    
    # Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'anilsteel.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key-change-me')
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
    
    # Ensure instance and upload folders exist
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Import models after db is initialized to avoid circular imports
    from models import User, Product, Category, Cart, CartItem, Order, OrderItem, Review, ProductImage
    
    # Register blueprints
    try:
        from routes.auth import auth_bp
        from routes.products import products_bp
        from routes.cart import cart_bp
        from routes.orders import orders_bp
        from routes.reviews import reviews_bp
        
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(products_bp, url_prefix='/api/products')
        app.register_blueprint(cart_bp, url_prefix='/api/cart')
        app.register_blueprint(orders_bp, url_prefix='/api/orders')
        app.register_blueprint(reviews_bp, url_prefix='/api/products')
        
        # Health check endpoint
        @app.route('/api/health')
        def health_check():
            return jsonify({'status': 'healthy', 'message': 'Server is running'}), 200
            
    except Exception as e:
        print(f"Error registering blueprints: {str(e)}")
        raise
    
    return app

def init_db():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("Database tables created successfully!")

app = create_app()

if __name__ == '__main__':
    # Initialize the database
    init_db()
    # Run the app
    app.run(host='0.0.0.0', port=5001, debug=True)
