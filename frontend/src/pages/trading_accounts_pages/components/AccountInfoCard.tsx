import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../../configuration/AxiosConfigurations";
import {AccountProps} from "../../../types/AccountProps";
import "../view_accounts/DashboardStyles.css";

import "../../../styles/GlobalStyles.css";
import "../../../styles/FormStyles.css";
import "./AccountCard.css";


const AccountInfoCard: React.FC<AccountProps> = ({ account, onDelete }) => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const [showCredentials, setShowCredentials] = useState(false);
    const [passwordVisible, setPasswordVisible] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const accountCache = new Map();
    const [accountInfo, setAccountInfo] = useState<{
        balance: number | null;
        equity: number | null;
        active_positions: number | null;
        currency: string | null;
    }>({
        balance: null,
        equity: null,
        active_positions: null,
        currency: null
    });

    useEffect(() => {
        let isMounted = true;

        const fetchAccountInfo = async () => {
            if (accountCache.has(account.account_id)) {
                setAccountInfo(accountCache.get(account.account_id));
                setLoading(false);
                return;
            }

            try {
                const response = await api.get(`/api/trademind/trading_accounts/${account.account_id}/get_account_info`);
                const data = response.data;

                if (isMounted) {
                    const formattedData = {
                        balance: data.balance ?? null,
                        equity: data.equity ?? null,
                        active_positions: data.active_positions ?? null,
                        currency: data.currency ?? "USD"
                    };
                    accountCache.set(account.account_id, formattedData);
                    setAccountInfo(formattedData);
                    setLoading(false);
                }
            } catch (error) {
                console.error("Error fetching account info:", error);
                if (isMounted) {
                    setError("Failed to load account info");
                    setLoading(false);
                }
            }
        };

        fetchAccountInfo();

        return () => {
            isMounted = false;
        };
    }, [account.account_id]);

    const copyToClipboard = (text: string) => {
        navigator.clipboard.writeText(text);
    };

    const handleDelete = async () => {
        try {
            const { status } = await api.delete(`/api/trademind/trading_accounts/delete_account/${account.account_id}`);

            if (status !== 200 && status !== 204) {
                throw new Error("Failed to delete the trading account.");
            }

            onDelete(Number(account.account_id));
            setShowDeleteConfirm(false);
        } catch (error) {
            console.error("Error deleting account:", error);
            alert("An error occurred while deleting the account.");
        }
    };

    return (
        <div className="form-container account-info-card">
            <h2>{account.broker_name} {account.account_id}</h2>

            {loading ? (
                <p>Loading account data...</p>
            ) : error ? (
                <p className="form-error">{error}</p>
            ) : (
                <div className="info-grid">
                    <div><strong>Status:</strong> {account.status ?? "Active"}</div>
                    <div><strong>Platform:</strong> {account.platform ?? "MetaTrader5"}</div>
                    <div><strong>Balance:</strong> {accountInfo.balance !== null ? `${accountInfo.balance.toLocaleString()} ${accountInfo.currency}` : "N/A"}</div>
                    <div><strong>Equity:</strong> {accountInfo.equity !== null ? `${accountInfo.equity.toLocaleString()} ${accountInfo.currency}` : "N/A"}</div>
                    <div><strong>Active Trades:</strong> {accountInfo.active_positions !== null ? accountInfo.active_positions : "N/A"}</div>
                    <div><strong>Currency:</strong> {accountInfo.currency}</div>
                </div>
            )}

            {/*<div className="account-buttons">*/}

                {window.location.pathname.includes("dashboard/") ? (
                    <button className="form-button" onClick={() => setShowCredentials(true)}>Credentials</button>
                ) : (
                    <>
                        <button
                            className="form-button"
                            onClick={() => navigate(`/accounts/dashboard/${account.account_id}`)}>MetriX
                        </button>

                        <button
                            className="form-button" onClick={() => setShowCredentials(true)}>Credentials
                        </button>

                        <button
                            className="form-button" onClick={() => setShowDeleteConfirm(true)}>Delete
                        </button>
                    </>
                )}
            {/*</div>*/}

            {showCredentials && (
                <div className="credentials-modal">
                    <div className="modal-content">
                        <h3>Login Credentials</h3>
                        <button className="close-modal" onClick={() => setShowCredentials(false)}>✖</button>

                        <div className="credential-item">
                            <span>Login:</span>
                            <span>{account.account_id}</span>
                            <button onClick={() => copyToClipboard(account.account_id)}>📋 Copy</button>
                        </div>

                        <div className="credential-item">
                            <span>Password:</span>
                            <span>
                                {passwordVisible ? account.password : "********"}
                            </span>
                            <button onClick={() => setPasswordVisible(!passwordVisible)}>👁</button>
                            <button onClick={() => copyToClipboard(account.password!)}>📋 Copy</button>
                        </div>

                        <div className="credential-item">
                            <span>Server:</span>
                            <span>{account.server ?? "N/A"}</span>
                            <button onClick={() => copyToClipboard(account.server ?? "N/A")}>📋 Copy</button>
                        </div>
                    </div>
                </div>
            )}

            {showDeleteConfirm && (
                <div className="credentials-modal">
                    <div className="modal-content">
                        <h3>Confirm Delete</h3>
                        <p>Are you sure you want to delete this trading account?</p>
                        <button className="close-modal" onClick={() => setShowDeleteConfirm(false)}>✖</button>

                        <div className="modal-buttons">
                            <button className="delete-confirm" onClick={handleDelete}>Yes, Delete</button>
                            <button className="delete-cancel" onClick={() => setShowDeleteConfirm(false)}>Cancel</button>
                        </div>
                    </div>
                </div>
            )}

        </div>
    );
};

export default AccountInfoCard;
