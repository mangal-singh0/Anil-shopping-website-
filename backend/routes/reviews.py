from flask import Blueprint, request, jsonify
from extensions import db
from models import Review, Product
from flask_jwt_extended import jwt_required, get_jwt_identity

reviews_bp = Blueprint('reviews', __name__)

# Note: The prefix in app.py is /api/products, so these routes are relative to that.
# We want /api/products/<id>/reviews

@reviews_bp.route('/<int:product_id>/reviews', methods=['GET'])
def get_reviews(product_id):
    product = Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    
    result = []
    for r in reviews:
        result.append({
            'id': r.id,
            'user': r.user.name,
            'rating': r.rating,
            'comment': r.comment,
            'created_at': r.created_at.isoformat()
        })
        
    return jsonify(result)

@reviews_bp.route('/<int:product_id>/reviews', methods=['POST'])
@jwt_required()
def add_review(product_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    rating = data.get('rating')
    comment = data.get('comment')
    
    if not rating:
        return jsonify({'message': 'Rating is required'}), 400
        
    review = Review(
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({'message': 'Review added', 'id': review.id}), 201
