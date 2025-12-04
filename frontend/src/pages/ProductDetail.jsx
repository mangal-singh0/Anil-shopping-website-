import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { Star, ShoppingCart, Truck, ShieldCheck } from 'lucide-react';
import { motion } from 'framer-motion';

const ProductDetail = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [quantity, setQuantity] = useState(1);
    const { addToCart } = useCart();
    const { isAuthenticated } = useAuth();
    const [reviewForm, setReviewForm] = useState({ rating: 5, comment: '' });

    useEffect(() => {
        const fetchProduct = async () => {
            try {
                const response = await axios.get(`http://localhost:5001/api/products/${id}`);
                setProduct(response.data);
            } catch (error) {
                console.error('Failed to fetch product', error);
            } finally {
                setLoading(false);
            }
        };
        fetchProduct();
    }, [id]);

    const handleAddToCart = async () => {
        await addToCart(product.id, quantity);
        alert('Added to cart!');
    };

    const submitReview = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`http://localhost:5001/api/products/${id}/reviews`, reviewForm);
            // Refresh product to see new review
            const response = await axios.get(`http://localhost:5001/api/products/${id}`);
            setProduct(response.data);
            setReviewForm({ rating: 5, comment: '' });
        } catch (error) {
            alert('Failed to submit review');
        }
    };

    if (loading) return <div className="text-center py-20">Loading...</div>;
    if (!product) return <div className="text-center py-20">Product not found</div>;

    return (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 p-8">
                {/* Image Gallery */}
                <div className="space-y-4">
                    <div className="aspect-w-4 aspect-h-3 rounded-lg overflow-hidden bg-gray-100">
                        <img
                            src={product.image_url ? (product.image_url.startsWith('http') ? product.image_url : `http://localhost:5001${product.image_url}`) : 'https://placehold.co/600x400?text=No+Image'}
                            alt={product.name}
                            className="object-cover w-full h-full"
                        />
                    </div>
                    {/* Thumbnails could go here */}
                </div>

                {/* Product Info */}
                <div>
                    <div className="mb-4">
                        <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
                        <div className="flex items-center space-x-4">
                            <div className="flex items-center text-yellow-400">
                                <Star className="fill-current h-5 w-5" />
                                <span className="ml-1 text-gray-600 font-medium">4.5 (12 reviews)</span>
                            </div>
                            <span className="text-gray-300">|</span>
                            <span className="text-green-600 font-medium">{product.stock > 0 ? 'In Stock' : 'Out of Stock'}</span>
                        </div>
                    </div>

                    <div className="text-4xl font-bold text-primary-600 mb-6">₹{product.price}</div>

                    <p className="text-gray-600 mb-8 leading-relaxed">
                        {product.description}
                    </p>

                    <div className="border-t border-b border-gray-100 py-6 mb-8 space-y-4">
                        <div className="flex items-center text-gray-700">
                            <Truck className="h-5 w-5 mr-3 text-primary-500" />
                            <span>Free delivery on orders over ₹10,000</span>
                        </div>
                        <div className="flex items-center text-gray-700">
                            <ShieldCheck className="h-5 w-5 mr-3 text-primary-500" />
                            <span>Quality certified steel products</span>
                        </div>
                    </div>

                    <div className="flex items-center space-x-4 mb-8">
                        <div className="flex items-center border border-gray-300 rounded-md">
                            <button
                                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                                className="px-3 py-2 hover:bg-gray-50 text-gray-600"
                            >
                                -
                            </button>
                            <span className="px-3 py-2 font-medium w-12 text-center">{quantity}</span>
                            <button
                                onClick={() => setQuantity(quantity + 1)}
                                className="px-3 py-2 hover:bg-gray-50 text-gray-600"
                            >
                                +
                            </button>
                        </div>
                        <motion.button
                            whileTap={{ scale: 0.95 }}
                            onClick={handleAddToCart}
                            className="flex-1 bg-primary-600 text-white px-6 py-3 rounded-md font-bold hover:bg-primary-700 flex items-center justify-center space-x-2"
                        >
                            <ShoppingCart className="h-5 w-5" />
                            <span>Add to Cart</span>
                        </motion.button>
                    </div>
                </div>
            </div>

            {/* Reviews Section */}
            <div className="border-t border-gray-100 p-8 bg-gray-50">
                <h2 className="text-2xl font-bold mb-6">Customer Reviews</h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                    <div className="space-y-6">
                        {product.reviews && product.reviews.length > 0 ? (
                            product.reviews.map(review => (
                                <div key={review.id} className="bg-white p-4 rounded-lg shadow-sm">
                                    <div className="flex items-center justify-between mb-2">
                                        <span className="font-semibold">{review.user}</span>
                                        <div className="flex text-yellow-400">
                                            {[...Array(5)].map((_, i) => (
                                                <Star key={i} className={`h-4 w-4 ${i < review.rating ? 'fill-current' : 'text-gray-300'}`} />
                                            ))}
                                        </div>
                                    </div>
                                    <p className="text-gray-600">{review.comment}</p>
                                </div>
                            ))
                        ) : (
                            <p className="text-gray-500">No reviews yet.</p>
                        )}
                    </div>

                    {isAuthenticated ? (
                        <div className="bg-white p-6 rounded-lg shadow-sm h-fit">
                            <h3 className="text-lg font-bold mb-4">Write a Review</h3>
                            <form onSubmit={submitReview}>
                                <div className="mb-4">
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Rating</label>
                                    <select
                                        value={reviewForm.rating}
                                        onChange={e => setReviewForm({ ...reviewForm, rating: parseInt(e.target.value) })}
                                        className="w-full border border-gray-300 rounded-md py-2 px-3"
                                    >
                                        <option value="5">5 Stars</option>
                                        <option value="4">4 Stars</option>
                                        <option value="3">3 Stars</option>
                                        <option value="2">2 Stars</option>
                                        <option value="1">1 Star</option>
                                    </select>
                                </div>
                                <div className="mb-4">
                                    <label className="block text-sm font-medium text-gray-700 mb-1">Comment</label>
                                    <textarea
                                        value={reviewForm.comment}
                                        onChange={e => setReviewForm({ ...reviewForm, comment: e.target.value })}
                                        className="w-full border border-gray-300 rounded-md py-2 px-3 h-24"
                                        required
                                    ></textarea>
                                </div>
                                <button type="submit" className="w-full bg-primary-600 text-white py-2 rounded-md hover:bg-primary-700 font-medium">
                                    Submit Review
                                </button>
                            </form>
                        </div>
                    ) : (
                        <div className="bg-white p-6 rounded-lg shadow-sm text-center">
                            <p>Please <a href="/login" className="text-primary-600 font-bold">login</a> to write a review.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ProductDetail;
