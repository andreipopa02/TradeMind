import React, { useEffect, useState } from 'react';
import Select from "react-select";
import { uiStyles, genderOptions, countryOptions } from "../../components/ThemeContext";

import api from '../../configuration/AxiosConfigurations';
import {useAuth} from "../../configuration/UseAuth";

import NavBar from '../../components/nav_bar/NavBar';
import SideMenu from '../../components/side_menu/SideMenu';
import Footer from "../../components/footer/Footer";

import '../../styles/GlobalStyles.css';
import '../../styles/FormStyles.css';
import './SettingsPageStyles.css';



const SettingsPage: React.FC = () => {
    const user = useAuth();
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        gender: '',
        country: '',
    });
    const [success, setSuccess] = useState('');
    const [showPasswordFields, setShowPasswordFields] = useState(false);
    const [passwords, setPasswords] = useState({
        current: '',
        new: '',
        confirm: ''
    });
    const [passwordError, setPasswordError] = useState('');
    const [passwordSuccess, setPasswordSuccess] = useState('');

    useEffect(() => {
        if (user) {
            api.get(`/api/trademind/users/details/${user.id}`)
                .then((res) => {
                    setFormData({
                        first_name: res.data.first_name,
                        last_name: res.data.last_name,
                        email: res.data.email,
                        phone: res.data.phone || '',
                        gender: res.data.gender || '',
                        country: res.data.country || '',
                    });
                })
                .catch((err) => console.error(err));
        }
    }, []);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!user?.id) return;

        try {
            await api.put(`/api/trademind/users/${user.id}`, formData);
            setSuccess('Operation completed successfully.');
        } catch (err) {
            console.error(err);
        }
    };

    const handlePasswordChange = async () => {
        setPasswordError('');
        setPasswordSuccess('');

        if (passwords.new !== passwords.confirm) {
            setPasswordError("New passwords do not match.");
            return;
        }

        try {
            await api.put('/api/trademind/users/update-password', {
                email: formData.email,
                current_password: passwords.current,
                new_password: passwords.new
            });
            setPasswordSuccess("Password changed successfully.");
            setPasswords({ current: '', new: '', confirm: '' });
            setShowPasswordFields(false);
        } catch (err: any) {
            setPasswordError(err.response?.data?.detail || "Failed to change password.");
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
                    <h2 className="page-title">Your Control Panel️</h2>

                    <form className="form-container" onSubmit={handleSubmit}>
                        <label>
                            First Name:
                            <input
                                type="text"
                                name="first_name"
                                value={formData.first_name}
                                onChange={handleChange}
                                required/>
                        </label>

                        <label>
                            Last Name:
                            <input
                                type="text"
                                name="last_name"
                                value={formData.last_name}
                                onChange={handleChange}
                                required/>
                        </label>

                        <label>
                            Email (not editable):
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                readOnly/>
                        </label>

                        <label>
                            Phone:
                            <input
                                type="text"
                                name="phone"
                                value={formData.phone}
                                onChange={handleChange}
                                placeholder="+1..."/>
                        </label>

                        <label>
                            Country:
                            <Select
                                styles={uiStyles}
                                options={countryOptions}
                                value={formData.country ? {value: formData.country, label: formData.country} : null}
                                onChange={(opt: any) => setFormData({...formData, country: opt?.value ?? ""})}
                                placeholder="Select Country"
                            />
                        </label>

                        <label>
                            Gender:
                            <Select
                                styles={uiStyles}
                                options={genderOptions}
                                value={formData.gender ? {value: formData.gender, label: formData.gender} : null}
                                onChange={(opt: any) => setFormData({...formData, gender: opt?.value ?? ""})}
                                placeholder="Select Gender"
                            />
                        </label>

                        <button type="submit" className="form-button">Save Changes</button>
                    </form>

                    {success && <p className="form-success">{success}</p>}

                    <button
                        className="change-password-button"
                        onClick={() => setShowPasswordFields(!showPasswordFields)}>
                        {showPasswordFields ? 'Cancel' : 'Change password'}
                    </button>

                    {showPasswordFields && (
                        <form className="form-container change-pswd-container" onSubmit={(e) => {
                            e.preventDefault();
                            handlePasswordChange();
                        }}>
                            <label>
                                Current password:
                                <input
                                    type="password"
                                    value={passwords.current}
                                    onChange={(e) => setPasswords({...passwords, current: e.target.value})}
                                    required
                                />
                            </label>

                            <label>
                                New password:
                                <input
                                    type="password"
                                    value={passwords.new}
                                    onChange={(e) => setPasswords({...passwords, new: e.target.value})}
                                    required
                                />
                            </label>

                            <label>
                                Confirm new password:
                                <input
                                    type="password"
                                    value={passwords.confirm}
                                    onChange={(e) => setPasswords({...passwords, confirm: e.target.value})}
                                    required
                                />
                            </label>

                            <button type="submit" className="form-button">
                                Confirm change
                            </button>
                        </form>
                    )}

                    {passwordError && <p className="form-error">{passwordError}</p>}
                    {passwordSuccess && <p className="form-success">{passwordSuccess}</p>}

                    <Footer />
                </div>
            </div>


        </div>
    );
};

export default SettingsPage;
