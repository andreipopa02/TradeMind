import React, { useState } from 'react';
import Select from "react-select";
import { Link, useNavigate } from 'react-router-dom';
import api from '../../configuration/AxiosConfigurations';

import Footer from "../../components/footer/Footer";
import { uiStyles, genderOptions, countryOptions } from "../../components/ThemeContext";

import '../../styles/GlobalStyles.css';
import '../../styles/FormStyles.css';
import './AuthStyles.css';



const RegisterPage: React.FC = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        phone: '',
        gender: '',
        country: ''
    });
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();

    const isValidEmail = (email: string) =>
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    const isStrongPassword = (password: string) =>
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/.test(password);

    const isValidPhone = (phone: string) =>
        /^\+?\d{8,15}$/.test(phone);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData({
            ...formData,
            [e.target.id]: e.target.value
        });
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setErrorMessage('');
        setSuccessMessage('');

        if (!isValidEmail(formData.email)) {
            setErrorMessage("Invalid email format.");
            return;
        }

        if (!isStrongPassword(formData.password)) {
            setErrorMessage("Password must be at least 8 characters, contain uppercase, lowercase, digit and special character.");
            return;
        }

        if (!isValidPhone(formData.phone)) {
            setErrorMessage("Invalid phone number.");
            return;
        }

        if (formData.firstName.trim().length < 2 || formData.lastName.trim().length < 2) {
            setErrorMessage("First and last name must be at least 2 characters.");
            return;
        }

        if (!formData.gender || !formData.country) {
            setErrorMessage("Gender and country must be selected.");
            return;
        }

        try {
            const response = await api.post('/api/trademind/users/register', {
                first_name: formData.firstName,
                last_name: formData.lastName,
                email: formData.email,
                password: formData.password,
                phone: formData.phone,
                gender: formData.gender,
                country: formData.country
            });

            if (response.status === 200 || response.status === 201) {
                setSuccessMessage('User registered successfully!');
                setFormData({
                    firstName: '',
                    lastName: '',
                    email: '',
                    password: '',
                    phone: '',
                    gender: '',
                    country: ''
                });
                setTimeout(() => navigate('/login'), 1000);
            }
        } catch (error: any) {
            if (error.response?.data?.detail) {
                setErrorMessage(error.response.data.detail);
            } else {
                setErrorMessage('Failed to register user.');
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
                    <button className="btn inactive">Login</button>
                </Link>
                <Link to="/register">
                    <button className="btn active">Register</button>
                </Link>
            </div>

            <div className="form-container-div">
                <form onSubmit={handleSubmit} className="form-container register">
                    <h2 className="page-title">Register</h2>

                    {errorMessage && <p style={{color: 'red'}}>{errorMessage}</p>}
                    {successMessage && <p style={{color: 'green'}}>{successMessage}</p>}

                    <label htmlFor="firstName">First Name</label>
                    <input
                        type="text"
                        id="firstName"
                        placeholder="Enter your first name"
                        value={formData.firstName}
                        onChange={handleInputChange}
                        required
                    />

                    <label htmlFor="lastName">Last Name</label>
                    <input
                        type="text"
                        id="lastName"
                        placeholder="Enter your last name"
                        value={formData.lastName}
                        onChange={handleInputChange}
                        required
                    />

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
                    <label htmlFor="phone">Phone</label>
                    <input
                        type="tel"
                        id="phone"
                        placeholder="Enter your phone number"
                        value={formData.phone}
                        onChange={handleInputChange}
                        required
                    />

                    <label htmlFor="gender">Gender</label>
                    <Select
                        styles={uiStyles}
                        options={genderOptions}
                        value={formData.gender ? {value: formData.gender, label: formData.gender} : null}
                        onChange={(opt: any) => setFormData({...formData, gender: opt?.value ?? ""})}
                        placeholder="Select Gender"
                    />

                    <label htmlFor="country">Country</label>
                    <Select
                        styles={uiStyles}
                        options={countryOptions}
                        value={formData.country ? {value: formData.country, label: formData.country} : null}
                        onChange={(opt: any) => setFormData({...formData, country: opt?.value ?? ""})}
                        placeholder="Select Country"
                    />

                    <button type="submit" className="form-button">Register</button>
                </form>
            </div>

            <Footer/>
        </div>
    );
};

export default RegisterPage;
