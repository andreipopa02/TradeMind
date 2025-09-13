import React, { useState } from 'react';
import {Link, useNavigate} from 'react-router-dom';
import * as jwt_decode from "jwt-decode";

import Footer from "../../components/footer/Footer";
import { TokenPayload } from "../../types/TokenPayload";
import api from "../../configuration/AxiosConfigurations";

import '../../styles/GlobalStyles.css';
import '../../styles/FormStyles.css';
import './AuthStyles.css';



const LoginPage: React.FC = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({
            ...formData,
            [e.target.id]: e.target.value,
        });
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setErrorMessage('');
        setSuccessMessage('');

        if (!formData.email || !formData.password) {
            setErrorMessage("Email and password are required.");
            return;
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
            setErrorMessage("Invalid email format.");
            return;
        }

        try {
            const response = await api.post("/api/trademind/users/login", {
                email: formData.email,
                password: formData.password,
            });

            const { access_token } = response.data;
            localStorage.setItem("access_token", access_token);

            const decoded = jwt_decode.jwtDecode<TokenPayload>(access_token);

            setSuccessMessage(`Welcome back, ${decoded.first_name}!`);
            setTimeout(() => navigate('/home'), 2000);

        } catch (error: any) {
            if (error.response?.data?.detail) {
                setErrorMessage(error.response.data.detail);
            } else {
                setErrorMessage('Login failed. Please try again.');
            }
        }
    };

    return (
        <div className="app-container auth-container">

            <div className="title-container">
                <h1 className="page-title">TradeMind</h1>
            </div>

            <div className="button-container">
                <Link to="/login">
                    <button className="btn active">Login</button>
                </Link>

                <Link to="/register">
                    <button className="btn inactive">Register</button>
                </Link>
            </div>

            <div className="form-container-div">

                <form onSubmit={handleSubmit} className="form-container login">
                    <h2 className="page-title">Login</h2>

                    {errorMessage && <p style={{color: 'red'}}>{errorMessage}</p>}
                    {successMessage && <p style={{color: 'green'}}>{successMessage}</p>}

                    <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        placeholder="Enter your email"
                        value={formData.email}
                        onChange={handleInputChange}
                        required
                    />

                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        placeholder="Enter your password"
                        value={formData.password}
                        onChange={handleInputChange}
                        required
                    />
                    <div className="forgot-password" >
                        <Link to="/forgot-password">
                            Forgot your password?
                        </Link>
                    </div>

                    <button type="submit" className="form-button">Login</button>
                </form>
            </div>

            <Footer/>
        </div>
    );
};

export default LoginPage;
