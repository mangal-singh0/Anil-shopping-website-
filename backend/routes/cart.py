from flask import Blueprint, request, jsonify
from app import db
from models import Cart, CartItem, Product
from flask_jwt_extended import jwt_required, get_jwt_identity

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart:
        return jsonify({'items': [], 'total': 0})
        
    items = []
    total = 0
    for item in cart.items:
        items.append({
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'image_url': item.product.image_url
        })
        total += float(item.product.price) * item.quantity
        
    return jsonify({'items': items, 'total': total})

@cart_bp.route('', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({'message': 'Product ID required'}), 400
        
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
        
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        
    db.session.commit()
    return jsonify({'message': 'Item added to cart'})

@cart_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404
        
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not cart_item:
        return jsonify({'message': 'Item not found in cart'}), 404
        
    data = request.get_json()
    quantity = data.get('quantity')
    
    if quantity is not None:
        if quantity > 0:
            cart_item.quantity = quantity
        else:
            db.session.delete(cart_item)
            
    db.session.commit()
    return jsonify({'message': 'Cart updated'})

@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    user_id = get_jwt_identity()
    cart = Cart.query.filter_by(user_id=user_id).first()
    
    if not cart:
        return jsonify({'message': 'Cart not found'}), 404
        
    cart_item = CartItem.query.filter_by(id=item_id, cart_id=cart.id).first()
    if not cart_item:
        return jsonify({'message': 'Item not found in cart'}), 404
        
    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({'message': 'Item removed'})
