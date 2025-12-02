import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { Package, ChevronDown, ChevronUp } from 'lucide-react';

const Orders = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const { isAuthenticated } = useAuth();
    const [expandedOrder, setExpandedOrder] = useState(null);
    const [orderDetails, setOrderDetails] = useState({});

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/orders');
                setOrders(response.data);
            } catch (error) {
                console.error('Failed to fetch orders', error);
            } finally {
                setLoading(false);
            }
        };

        if (isAuthenticated) {
            fetchOrders();
        }
    }, [isAuthenticated]);

    const toggleOrder = async (orderId) => {
        if (expandedOrder === orderId) {
            setExpandedOrder(null);
            return;
        }

        setExpandedOrder(orderId);
        if (!orderDetails[orderId]) {
            try {
                const response = await axios.get(`http://localhost:5000/api/orders/${orderId}`);
                setOrderDetails(prev => ({ ...prev, [orderId]: response.data }));
            } catch (error) {
                console.error('Failed to fetch order details', error);
            }
        }
    };

    if (!isAuthenticated) return <div className="text-center py-20">Please login to view orders</div>;
    if (loading) return <div className="text-center py-20">Loading...</div>;

    return (
        <div className="max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-8">My Orders</h1>

            {orders.length === 0 ? (
                <div className="text-center py-20 bg-white rounded-lg shadow-sm">
                    <Package className="h-16 w-16 mx-auto text-gray-300 mb-4" />
                    <p className="text-gray-500">You haven't placed any orders yet.</p>
                </div>
            ) : (
                <div className="space-y-4">
                    {orders.map(order => (
                        <div key={order.id} className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden">
                            <div
                                className="p-6 flex items-center justify-between cursor-pointer hover:bg-gray-50 transition-colors"
                                onClick={() => toggleOrder(order.id)}
                            >
                                <div className="flex items-center gap-4">
                                    <div className="bg-primary-100 p-3 rounded-full">
                                        <Package className="h-6 w-6 text-primary-600" />
                                    </div>
                                    <div>
                                        <p className="font-bold text-gray-900">Order #{order.id}</p>
                                        <p className="text-sm text-gray-500">{new Date(order.created_at).toLocaleDateString()}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-6">
                                    <span className={`px-3 py-1 rounded-full text-xs font-semibold
                    ${order.status === 'Delivered' ? 'bg-green-100 text-green-800' :
                                            order.status === 'Cancelled' ? 'bg-red-100 text-red-800' :
                                                'bg-blue-100 text-blue-800'}`}>
                                        {order.status}
                                    </span>
                                    <div className="text-right">
                                        <p className="font-bold">₹{order.total_amount}</p>
                                        <p className="text-xs text-gray-500">{order.item_count} items</p>
                                    </div>
                                    {expandedOrder === order.id ? <ChevronUp className="h-5 w-5 text-gray-400" /> : <ChevronDown className="h-5 w-5 text-gray-400" />}
                                </div>
                            </div>

                            {expandedOrder === order.id && orderDetails[order.id] && (
                                <div className="border-t border-gray-100 p-6 bg-gray-50">
                                    <div className="mb-4">
                                        <h4 className="font-semibold mb-2">Shipping Details</h4>
                                        <p className="text-sm text-gray-600">{orderDetails[order.id].shipping.name}</p>
                                        <p className="text-sm text-gray-600">{orderDetails[order.id].shipping.address}</p>
                                        <p className="text-sm text-gray-600">{orderDetails[order.id].shipping.phone}</p>
                                    </div>

                                    <h4 className="font-semibold mb-2">Items</h4>
                                    <div className="space-y-3">
                                        {orderDetails[order.id].items.map((item, idx) => (
                                            <div key={idx} className="flex items-center justify-between bg-white p-3 rounded border border-gray-200">
                                                <div className="flex items-center gap-3">
                                                    <img src={item.image_url || 'https://placehold.co/50x50'} alt={item.product_name} className="w-12 h-12 object-cover rounded" />
                                                    <div>
                                                        <p className="font-medium">{item.product_name}</p>
                                                        <p className="text-xs text-gray-500">Qty: {item.quantity}</p>
                                                    </div>
                                                </div>
                                                <p className="font-medium">₹{item.total}</p>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Orders;
