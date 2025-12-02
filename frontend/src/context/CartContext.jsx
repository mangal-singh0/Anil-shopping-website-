import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from './AuthContext';

const CartContext = createContext();

export const useCart = () => useContext(CartContext);

export const CartProvider = ({ children }) => {
    const { isAuthenticated } = useAuth();
    const [cart, setCart] = useState([]);
    const [total, setTotal] = useState(0);

    const fetchCart = async () => {
        if (!isAuthenticated) {
            setCart([]);
            setTotal(0);
            return;
        }
        try {
            const response = await axios.get('http://localhost:5000/api/cart');
            setCart(response.data.items);
            setTotal(response.data.total);
        } catch (error) {
            console.error('Failed to fetch cart', error);
        }
    };

    useEffect(() => {
        fetchCart();
    }, [isAuthenticated]);

    const addToCart = async (productId, quantity = 1) => {
        if (!isAuthenticated) {
            alert('Please login to add items to cart');
            return;
        }
        try {
            await axios.post('http://localhost:5000/api/cart', { product_id: productId, quantity });
            await fetchCart();
        } catch (error) {
            console.error('Failed to add to cart', error);
            throw error;
        }
    };

    const updateQuantity = async (itemId, quantity) => {
        try {
            await axios.put(`http://localhost:5000/api/cart/${itemId}`, { quantity });
            await fetchCart();
        } catch (error) {
            console.error('Failed to update cart', error);
        }
    };

    const removeFromCart = async (itemId) => {
        try {
            await axios.delete(`http://localhost:5000/api/cart/${itemId}`);
            await fetchCart();
        } catch (error) {
            console.error('Failed to remove from cart', error);
        }
    };

    const clearCart = () => {
        setCart([]);
        setTotal(0);
    };

    return (
        <CartContext.Provider value={{ cart, total, addToCart, updateQuantity, removeFromCart, clearCart, fetchCart }}>
            {children}
        </CartContext.Provider>
    );
};
