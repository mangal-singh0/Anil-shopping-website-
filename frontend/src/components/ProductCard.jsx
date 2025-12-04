import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useCart } from '../context/CartContext';
import { ShoppingCart, Star } from 'lucide-react';

const ProductCard = ({ product }) => {
    const { addToCart } = useCart();

    const handleAddToCart = (e) => {
        e.preventDefault();
        addToCart(product.id);
    };

    return (
        <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100 flex flex-col h-full"
        >
            <Link to={`/product/${product.id}`} className="block relative pt-[75%]">
                <img
                    src={product.image_url ? (product.image_url.startsWith('http') ? product.image_url : `http://localhost:5001${product.image_url}`) : 'https://placehold.co/600x400?text=No+Image'}
                    alt={product.name}
                    className="absolute top-0 left-0 w-full h-full object-cover"
                />
            </Link>
            <div className="p-4 flex flex-col flex-grow">
                <div className="mb-2">
                    <span className="text-xs font-semibold text-primary-600 uppercase tracking-wider">
                        {product.category}
                    </span>
                </div>
                <Link to={`/product/${product.id}`}>
                    <h3 className="text-lg font-semibold text-gray-900 mb-1 hover:text-primary-600 line-clamp-2">
                        {product.name}
                    </h3>
                </Link>
                <div className="flex items-center mb-2">
                    <Star className="h-4 w-4 text-yellow-400 fill-current" />
                    <span className="ml-1 text-sm text-gray-600">{product.rating || '4.5'}</span>
                </div>
                <div className="mt-auto flex items-center justify-between">
                    <span className="text-xl font-bold text-gray-900">₹{product.price}</span>
                    <motion.button
                        whileTap={{ scale: 0.95 }}
                        onClick={handleAddToCart}
                        className="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                        <ShoppingCart className="h-4 w-4 mr-1" />
                        Add
                    </motion.button>
                </div>
            </div>
        </motion.div>
    );
};

export default ProductCard;
