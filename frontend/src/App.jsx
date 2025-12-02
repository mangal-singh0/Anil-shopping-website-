import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { CartProvider } from './context/CartContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ProductList from './pages/ProductList';
import ProductDetail from './pages/ProductDetail';
import Login from './pages/Login';
import Register from './pages/Register';
import Cart from './pages/Cart';
import Orders from './pages/Orders';
import AdminLayout from './components/layout/AdminLayout';
import AdminProducts from './pages/admin/AdminProducts';
import AddProduct from './pages/admin/AddProduct';
import EditProduct from './pages/admin/EditProduct';

function App() {
    return (
        <AuthProvider>
            <CartProvider>
                <Router>
                    <div className="min-h-screen bg-gray-50 flex flex-col">
                        <Navbar />
                        <main className="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-8">
                            <Routes>
                                <Route path="/" element={<Home />} />
                                <Route path="/products" element={<ProductList />} />
                                <Route path="/product/:id" element={<ProductDetail />} />
                                <Route path="/login" element={<Login />} />
                                <Route path="/register" element={<Register />} />
                                <Route path="/cart" element={<Cart />} />
                                <Route path="/orders" element={<Orders />} />
                                
                                {/* Admin Routes */}
                                <Route path="/admin" element={
                                    <ProtectedRoute>
                                        <AdminLayout />
                                    </ProtectedRoute>
                                }>
                                    <Route index element={<Navigate to="/admin/products" replace />} />
                                    <Route path="products" element={<AdminProducts />} />
                                    <Route path="products/add" element={<AddProduct />} />
                                    <Route path="products/edit/:id" element={<EditProduct />} />
                                    <Route path="orders" element={<div>Admin Orders</div>} />
                                    <Route path="users" element={<div>Users</div>} />
                                </Route>
                            </Routes>
                        </main>
                        <footer className="bg-white border-t border-gray-200 mt-auto">
                            <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                                <p className="text-center text-gray-500 text-sm">
                                    &copy; 2024 Anil Steel. All rights reserved.
                                </p>
                            </div>
                        </footer>
                    </div>
                </Router>
            </CartProvider>
        </AuthProvider>
    );
}

// Protected Route Component
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated, user } = useAuth();
    
    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }
    
    if (!user?.is_admin) {
        return <Navigate to="/" replace />;
    }
    
    return children;
};

export default App;
