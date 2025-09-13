import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import Footer from "../../components/footer/Footer";

import '../../styles/GlobalStyles.css';
import '../../styles/FormStyles.css';
import './AuthStyles.css';



const ResetPasswordPage = () => {
    const navigate = useNavigate();
    const [token, setToken] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
    const [message, setMessage] = useState("");

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const t = params.get("token");
        if (t) {
            setToken(t);
        } else {
            setStatus("error");
            setMessage("Missing token in URL.");
        }
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!newPassword) {
            setMessage("Password is required.");
            setStatus("error");
            return;
        }

        if (!/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{8,}$/.test(newPassword)) {
            setMessage("Password must be at least 8 characters long, include uppercase, lowercase, digit and special character.");
            setStatus("error");
            return;
        }

        try {
            const response = await axios.put("http://localhost:8000/api/trademind/users/reset-password", {
                token,
                new_password: newPassword,
            });
            setStatus("success");
            setMessage(response.data.message || "Password reset successful.");
        } catch (error: any) {
            setStatus("error");
            setMessage(error.response?.data?.detail || "Failed to reset password.");
        }
    };

    return (
        <div className="app-container auth-container">
            <h1 className="page-title">Reset Password</h1>

            {status === "success" ? (
                <div className="form-container">
                    <p className="form-success">{message}</p>
                    <button className="form-button-secondary" onClick={() => navigate("/login")}>
                        Go to Login
                    </button>
                </div>
            ) : (
                <form className="form-container" onSubmit={handleSubmit}>
                    <label htmlFor="newPassword">New Password</label>
                    <input
                        type="password"
                        id="newPassword"
                        placeholder="Enter your new password"
                        value={newPassword}
                        onChange={(e) => setNewPassword(e.target.value)}
                        required
                    />
                    <button type="submit" className="form-button">
                        Reset Password
                    </button>
                    {status === "error" && <p className="form-error">{message}</p>}
                </form>
            )}

            <Footer/>
        </div>
    );
};

export default ResetPasswordPage;
