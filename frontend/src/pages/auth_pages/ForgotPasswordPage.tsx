import { useState } from "react";
import axios from "axios";

import Footer from "../../components/footer/Footer";

import '../../styles/GlobalStyles.css';
import '../../styles/FormStyles.css';
import './AuthStyles.css';



const ForgotPasswordPage = () => {
    const [email, setEmail] = useState("");
    const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
    const [message, setMessage] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setStatus("idle");
        setMessage("");

        if (!email) {
            setMessage("Email is required.");
            setStatus("error");
            return;
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            setMessage("Invalid email format.");
            setStatus("error");
            return;
        }

        try {
            const res = await axios.post("http://localhost:8000/api/trademind/users/forgot-password", {
                email,
            });
            setStatus("success");
            setMessage(res.data.message || "If the email exists, a reset link has been sent.");
        } catch (error: any) {
            setStatus("error");
            setMessage(error.response?.data?.detail || "Failed to send reset link.");
        }
    };

    return (
        <div className="app-container auth-container">
            <h1 className="page-title">Forgot Password</h1>

            <form className="form-container" onSubmit={handleSubmit}>
                <label htmlFor="email">Your Email</label>
                <input
                    type="email"
                    id="email"
                    placeholder="Enter your email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />

                <button type="submit" className="form-button">
                    Send Reset Link
                </button>

                {status === "success" && <p className="form-success">{message}</p>}
                {status === "error" && <p className="form-error">{message}</p>}
            </form>

            <Footer/>
        </div>
    );
};

export default ForgotPasswordPage;
