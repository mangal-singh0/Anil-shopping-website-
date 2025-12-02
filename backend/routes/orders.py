from flask import Blueprint, request, jsonify
from app import db
from models import Order, OrderItem, Cart, CartItem, Product, User
from flask_jwt_extended import jwt_required, get_jwt_identity

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    shipping = data.get('shipping', {})
    
    # Get user cart
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        return jsonify({'message': 'Cart is empty'}), 400
        
    total_amount = 0
    order_items = []
    
    # Calculate total and prepare items
    for item in cart.items:
        price = item.product.price
        total_amount += float(price) * item.quantity
        order_items.append({
            'product_id': item.product_id,
            'quantity': item.quantity,
            'unit_price': price
        })
        
    # Create Order
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        shipping_name=shipping.get('name'),
        shipping_phone=shipping.get('phone'),
        shipping_address=shipping.get('address'),
        status='Placed'
    )
    db.session.add(order)
    db.session.flush() # Get ID
    
    # Create Order Items
    for item in order_items:
        oi = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            unit_price=item['unit_price']
        )
        db.session.add(oi)
        
    # Clear Cart
    CartItem.query.filter_by(cart_id=cart.id).delete()
    
    db.session.commit()
    
    return jsonify({'message': 'Order placed successfully', 'order_id': order.id}), 201

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        result.append({
            'id': order.id,
            'total_amount': float(order.total_amount),
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'item_count': len(order.items)
        })
        
    return jsonify(result)

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = Order.query.get_or_404(order_id)
    
    if order.user_id != user_id:
        # Check if admin
        user = User.query.get(user_id)
        if not user.is_admin:
            return jsonify({'message': 'Access denied'}), 403
            
    items = []
    for item in order.items:
        items.append({
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': float(item.unit_price),
            'total': float(item.unit_price) * item.quantity,
            'image_url': item.product.image_url
        })
        
    return jsonify({
        'id': order.id,
        'total_amount': float(order.total_amount),
        'status': order.status,
        'shipping': {
            'name': order.shipping_name,
            'phone': order.shipping_phone,
            'address': order.shipping_address
        },
        'items': items,
        'created_at': order.created_at.isoformat()
    })

@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user or not user.is_admin:
        return jsonify({'message': 'Admin access required'}), 403
        
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    if 'status' in data:
        order.status = data['status']
        db.session.commit()
        return jsonify({'message': 'Order status updated'})
        
    return jsonify({'message': 'No status provided'}), 400
