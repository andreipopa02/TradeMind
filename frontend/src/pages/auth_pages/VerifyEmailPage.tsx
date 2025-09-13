import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import '../../styles/GlobalStyles.css';
import '../../styles/FormStyles.css';
import './AuthStyles.css';



const VerifyEmailPage = () => {
    const [status, setStatus] = useState<"pending" | "success" | "error">("pending");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        const verifyEmail = async () => {
            const params = new URLSearchParams(window.location.search);
            const token = params.get("token");

            if (!token) {
                setStatus("error");
                setMessage("No token provided.");
                return;
            }

            try {
                const res = await axios.get(
                    `http://localhost:8000/api/trademind/users/verify-email?token=${token}`
                );
                setStatus("success");
                setMessage(res.data.message || "Email verified successfully.");
            } catch (error: any) {
                setStatus("error");
                setMessage(error.response?.data?.detail || "Verification failed.");
            }
        };

        verifyEmail();
    }, []);

    const handleGoToLogin = () => {
        navigate("/login");
    };

    return (
        <div style={{ maxWidth: 500, margin: "100px auto", textAlign: "center" }}>
            <h1 className="page-title">Email Verification</h1>

            {status === "pending" && <p>Verifying...</p>}

            {status !== "pending" && (
                <>
                    <p style={{ color: status === "success" ? "green" : "red" }}>{message}</p>
                    {status === "success" && (
                        <button className='form-button' onClick={handleGoToLogin} >
                            Go to Login
                        </button>
                    )}
                </>
            )}
        </div>
    );
};

export default VerifyEmailPage;
