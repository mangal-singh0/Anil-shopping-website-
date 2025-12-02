import os
from flask import Blueprint, request, jsonify, current_app
from app import db
from models import Product, Category, ProductImage, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import uuid

products_bp = Blueprint('products', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.is_admin

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
        
    data = request.form
    
    if not data.get('name') or not data.get('price'):
        return jsonify({'message': 'Missing required fields'}), 400
        
    # Handle Image Upload
    image_url = ''
    if 'image' in request.files:
        file = request.files['image']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename))
            image_url = f"{request.host_url}uploads/{unique_filename}" # Absolute URL for simplicity
    
    # Handle Category
    category_id = data.get('category_id')
    # If category_id is not provided, maybe create or find by name? For MVP assume ID or handle later.
    
    new_product = Product(
        name=data['name'],
        slug=data['name'].lower().replace(' ', '-'), # Simple slug generation
        description=data.get('description'),
        price=data['price'],
        stock=data.get('stock', 0),
        category_id=category_id,
        image_url=image_url
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({'message': 'Product created', 'id': new_product.id}), 201

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
