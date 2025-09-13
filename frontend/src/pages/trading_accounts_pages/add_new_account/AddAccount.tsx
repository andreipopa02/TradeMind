import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import {useAuth} from "../../../configuration/UseAuth";

import api from "../../../configuration/AxiosConfigurations";
import NavBar from "../../../components/nav_bar/NavBar";
import SideMenu from "../../../components/side_menu/SideMenu";
import Footer from "../../../components/footer/Footer";

import "../../../styles/GlobalStyles.css";
import '../../../styles/FormStyles.css';



const AddAccount: React.FC = () => {
    const user = useAuth();
    const [formData, setFormData] = useState({
        broker_name: "",
        account_id: "",
        server: "",
        password: "",
    });
    const [errorMessage, setErrorMessage] = useState("");
    const [successMessage, setSuccessMessage] = useState("");
    const [fieldErrors, setFieldErrors] = useState<{ [key: string]: string }>({});
    const navigate = useNavigate();


    useEffect(() => {
        if (!user?.id) {
            setErrorMessage("No authenticated user found.");
        }
    }, [user]);

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData({
            ...formData,
            [id]: value,
        });

        validateField(id, value);
    };

    const validateField = (field: string, value: string) => {
        let error = "";

        if (!value.trim()) {
            error = "This field is required.";
        } else {
            if (field === "account_id" && !/^\d+$/.test(value)) {
                error = "Account ID must contain only digits.";
            }
        }

        setFieldErrors((prevErrors) => ({
            ...prevErrors,
            [field]: error,
        }));
    };

    const validateForm = () => {
        const errors: { [key: string]: string } = {};

        Object.keys(formData).forEach((field) => {
            if (!formData[field as keyof typeof formData].trim()) {
                errors[field] = "This field is required.";
            }
        });

        if (formData.account_id && !/^\d+$/.test(formData.account_id)) {
            errors.account_id = "Account ID must contain only digits.";
        }

        setFieldErrors(errors);
        return Object.keys(errors).length === 0;
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage("");
        setSuccessMessage("");

        if (!validateForm() || !user?.id) {
            return;
        }

        const formDataToSend = {
            ...formData,
            user_id: user.id
        };

        try {
            const response = await api.post("/api/trademind/trading_accounts/add_account", formDataToSend);
            if (response.status === 200 || response.status === 201) {
                setSuccessMessage("Account successfully added!");
                setTimeout(() => navigate(`/accounts/dashboard/${formData.account_id}`), 2000);
            }
        } catch (error: any) {
            if (error.response?.data?.detail) {
                setErrorMessage(error.response.data.detail);
            } else {
                setErrorMessage("Invalid trading account credentials. Failed to add account.");
            }
        }
    };

    return (
        <div className="app-container">
            <NavBar />

            <div className="main-content">
                <div className="side-menu">
                    <SideMenu />
                </div>

                <div className="page-content">
                    <h2 className="page-title">Add New Trading Account</h2>

                    {errorMessage && <p className="form-error">{errorMessage}</p>}
                    {successMessage && <p className="form-success">{successMessage}</p>}

                    <form className="form-container wide-form" onSubmit={handleSubmit}>
                        <label htmlFor="broker">Broker:</label>
                        <input
                            type="text"
                            id="broker_name"
                            value={formData.broker_name}
                            onChange={handleInputChange}
                            placeholder="Enter broker name"
                            required
                        />
                        {fieldErrors.broker_name && <p className="form-error">{fieldErrors.broker_name}</p>}

                        <label htmlFor="accountId">Account ID:</label>
                        <input
                            type="text"
                            id="account_id"
                            value={formData.account_id}
                            onChange={handleInputChange}
                            placeholder="Enter account ID"
                            required
                        />
                        {fieldErrors.account_id && <p className="form-error">{fieldErrors.account_id}</p>}

                        <label htmlFor="password">Account Password:</label>
                        <input
                            type="password"
                            id="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            placeholder="Enter account password"
                            required
                        />
                        {fieldErrors.password && <p className="form-error">{fieldErrors.password}</p>}

                        <label htmlFor="server">Server:</label>
                        <input
                            type="text"
                            id="server"
                            value={formData.server}
                            onChange={handleInputChange}
                            placeholder="Enter server"
                            required
                        />
                        {fieldErrors.server && <p className="form-error">{fieldErrors.server}</p>}

                        <button type="submit" className="form-button">
                            Add Account
                        </button>
                    </form>

                    <Footer />
                </div>
            </div>
        </div>
    );
};

export default AddAccount;
