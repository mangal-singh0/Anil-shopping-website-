import { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';

// Base URL for API requests
const API_BASE_URL = 'http://localhost:5001/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState(localStorage.getItem('token'));

    // Configure axios defaults
    useEffect(() => {
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            localStorage.setItem('token', token);
        } else {
            delete axios.defaults.headers.common['Authorization'];
            localStorage.removeItem('token');
        }
    }, [token]);

    useEffect(() => {
        const fetchUser = async () => {
            if (!token) {
                console.log('No token found, user not authenticated');
                setLoading(false);
                return;
            }
            try {
                console.log('Fetching user data...');
                const response = await axios.get(`${API_BASE_URL}/auth/me`);
                console.log('User data from /me:', response.data.user);
                setUser(response.data.user);
            } catch (error) {
                console.error('Failed to fetch user', error);
                setToken(null);
                setUser(null);
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, [token]);

    const login = async (email, password) => {
        console.log('Login attempt with:', email);
        const response = await axios.post(`${API_BASE_URL}/auth/login`, { email, password });
        console.log('Login response:', response.data);
        setToken(response.data.token);
        setUser(response.data.user);
        console.log('User after login:', response.data.user);
        return response;
    };

    const register = async (name, email, password, phone) => {
        const response = await axios.post(`${API_BASE_URL}/auth/register`, { name, email, password, phone });
        setToken(response.data.token);
        setUser(response.data.user);
        return response;
    };

    const logout = () => {
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, register, logout, loading, isAuthenticated: !!user }}>
            {children}
        </AuthContext.Provider>
    );
};
