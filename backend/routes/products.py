import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from extensions import db
from models import Product, Category, ProductImage, User
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.utils import secure_filename
import uuid
import os

products_bp = Blueprint('products', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_admin():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        return user and user.is_admin
    except:
        return False

@products_bp.route('', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    search = request.args.get('search', '')
    category_slug = request.args.get('category', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    query = Product.query
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    if category_slug:
        query = query.join(Category).filter(Category.slug == category_slug)
        
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
        
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    pagination = query.paginate(page=page, per_page=limit, error_out=False)
    products = pagination.items
    
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'name': p.name,
            'slug': p.slug,
            'price': float(p.price),
            'image_url': p.image_url,
            'category': p.category_rel.name if p.category_rel else None,
            'rating': 4.5 # Placeholder, implement avg rating calculation
        })
        
    return jsonify({
        'products': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    
    images = [{'id': img.id, 'url': img.image_url} for img in product.images]
    reviews = [{'id': r.id, 'user': r.user.name, 'rating': r.rating, 'comment': r.comment} for r in product.reviews]
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'description': product.description,
        'price': float(product.price),
        'stock': product.stock,
        'specs': product.specs,
        'category': product.category_rel.name if product.category_rel else None,
        'images': images,
        'reviews': reviews,
        'image_url': product.image_url
    })

@products_bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
        
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'price', 'description', 'category']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    try:
        # Find or create category
        category = Category.query.filter_by(name=data['category']).first()
        if not category:
            category = Category(name=data['category'], slug=data['category'].lower().replace(' ', '_'))
            db.session.add(category)
            db.session.flush()  # Get the category ID
        
        product = Product(
            name=data['name'],
            price=float(data['price']),
            description=data['description'],
            category_id=category.id,
            stock=int(data.get('stock', 0)),
            image_url=data.get('image_url', '')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@products_bp.route('/admin/add', methods=['POST'])
@jwt_required()
def admin_add_product():
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    
    if 'image' not in request.files:
        return jsonify({'message': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not allowed'}), 400
    
    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        # Get form data
        name = request.form.get('name')
        price = float(request.form.get('price', 0))
        description = request.form.get('description', '')
        category = request.form.get('category', 'uncategorized')
        stock = int(request.form.get('stock', 0))
        
        # Find or create category
        category_obj = Category.query.filter_by(slug=category).first()
        if not category_obj:
            category_name = ' '.join(word.capitalize() for word in category.split('_'))
            category_obj = Category(name=category_name, slug=category)
            db.session.add(category_obj)
            db.session.flush()
        
        # Create product
        product = Product(
            name=name,
            slug=name.lower().replace(' ', '-'),
            price=price,
            description=description,
            category_id=category_obj.id,
            stock=stock,
            image_url=f"/uploads/{unique_filename}"
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product added successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'category': category_obj.name,
                'stock': product.stock,
                'image_url': product.image_url
            }
        }), 201
        
    except Exception as e:
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

@products_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
        
    product = Product.query.get_or_404(id)
    data = request.form # Or json if no file upload
    
    if 'name' in data:
        product.name = data['name']
        product.slug = data['name'].lower().replace(' ', '-')
    if 'price' in data:
        product.price = data['price']
    if 'stock' in data:
        product.stock = data['stock']
    if 'description' in data:
        product.description = data['description']
        
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            product.image_url = f"{request.host_url}uploads/{unique_filename}"
            
    db.session.commit()
    return jsonify({'message': 'Product updated'})

@products_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
        
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})
