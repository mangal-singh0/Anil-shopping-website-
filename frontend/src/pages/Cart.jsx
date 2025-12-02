import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { Link, useNavigate } from 'react-router-dom';
import { Trash2, Plus, Minus } from 'lucide-react';
import axios from 'axios';
import { useState } from 'react';
import { useForm } from 'react-hook-form';

const Cart = () => {
    const { cart, total, updateQuantity, removeFromCart, clearCart } = useCart();
    const { isAuthenticated, user } = useAuth();
    const navigate = useNavigate();
    const [isCheckingOut, setIsCheckingOut] = useState(false);
    const { register, handleSubmit, formState: { errors } } = useForm();

    if (!isAuthenticated) {
        return (
            <div className="text-center py-20">
                <h2 className="text-2xl font-bold mb-4">Please login to view your cart</h2>
                <Link to="/login" className="text-primary-600 hover:underline">Login here</Link>
            </div>
        );
    }

    if (cart.length === 0) {
        return (
            <div className="text-center py-20">
                <h2 className="text-2xl font-bold mb-4">Your cart is empty</h2>
                <Link to="/products" className="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700">
                    Start Shopping
                </Link>
            </div>
        );
    }

    const onCheckout = async (data) => {
        try {
            await axios.post('http://localhost:5000/api/orders', {
                shipping: {
                    name: data.name,
                    phone: data.phone,
                    address: data.address
                }
            });
            clearCart();
            alert('Order placed successfully!');
            navigate('/orders');
        } catch (error) {
            alert('Failed to place order');
        }
    };

    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-8">Shopping Cart</h1>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 space-y-4">
                    {cart.map(item => (
                        <div key={item.id} className="bg-white p-4 rounded-lg shadow-sm flex gap-4 items-center">
                            <img
                                src={item.image_url || 'https://placehold.co/100x100'}
                                alt={item.product_name}
                                className="w-20 h-20 object-cover rounded-md"
                            />
                            <div className="flex-grow">
                                <h3 className="font-semibold text-lg">{item.product_name}</h3>
                                <p className="text-gray-600">₹{item.price}</p>
                            </div>
                            <div className="flex items-center gap-2">
                                <button
                                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                    className="p-1 hover:bg-gray-100 rounded"
                                >
                                    <Minus className="h-4 w-4" />
                                </button>
                                <span className="w-8 text-center">{item.quantity}</span>
                                <button
                                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                    className="p-1 hover:bg-gray-100 rounded"
                                >
                                    <Plus className="h-4 w-4" />
                                </button>
                            </div>
                            <button
                                onClick={() => removeFromCart(item.id)}
                                className="text-red-500 hover:text-red-700 p-2"
                            >
                                <Trash2 className="h-5 w-5" />
                            </button>
                        </div>
                    ))}
                </div>

                <div className="lg:col-span-1">
                    <div className="bg-white p-6 rounded-lg shadow-sm sticky top-24">
                        <h2 className="text-xl font-bold mb-4">Order Summary</h2>
                        <div className="flex justify-between mb-2">
                            <span>Subtotal</span>
                            <span>₹{total}</span>
                        </div>
                        <div className="flex justify-between mb-4">
                            <span>Shipping</span>
                            <span>Free</span>
                        </div>
                        <div className="border-t pt-4 mb-6">
                            <div className="flex justify-between font-bold text-lg">
                                <span>Total</span>
                                <span>₹{total}</span>
                            </div>
                        </div>

                        {!isCheckingOut ? (
                            <button
                                onClick={() => setIsCheckingOut(true)}
                                className="w-full bg-primary-600 text-white py-3 rounded-md font-bold hover:bg-primary-700"
                            >
                                Proceed to Checkout
                            </button>
                        ) : (
                            <form onSubmit={handleSubmit(onCheckout)} className="space-y-4 animate-fade-in">
                                <h3 className="font-semibold border-b pb-2">Shipping Details</h3>
                                <div>
                                    <input
                                        {...register('name', { required: true })}
                                        defaultValue={user?.name}
                                        placeholder="Full Name"
                                        className="w-full border rounded-md p-2 text-sm"
                                    />
                                    {errors.name && <span className="text-red-500 text-xs">Required</span>}
                                </div>
                                <div>
                                    <input
                                        {...register('phone', { required: true })}
                                        defaultValue={user?.phone}
                                        placeholder="Phone Number"
                                        className="w-full border rounded-md p-2 text-sm"
                                    />
                                    {errors.phone && <span className="text-red-500 text-xs">Required</span>}
                                </div>
                                <div>
                                    <textarea
                                        {...register('address', { required: true })}
                                        placeholder="Shipping Address"
                                        className="w-full border rounded-md p-2 text-sm h-20"
                                    ></textarea>
                                    {errors.address && <span className="text-red-500 text-xs">Required</span>}
                                </div>
                                <div className="flex gap-2">
                                    <button
                                        type="button"
                                        onClick={() => setIsCheckingOut(false)}
                                        className="flex-1 border border-gray-300 py-2 rounded-md hover:bg-gray-50"
                                    >
                                        Cancel
                                    </button>
                                    <button
                                        type="submit"
                                        className="flex-1 bg-green-600 text-white py-2 rounded-md hover:bg-green-700"
                                    >
                                        Place Order
                                    </button>
                                </div>
                            </form>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Cart;
