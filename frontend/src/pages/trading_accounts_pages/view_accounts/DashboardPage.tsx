import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../../configuration/UseAuth";
import api from "../../../configuration/AxiosConfigurations";

import AccountInfoCard from "../components/AccountInfoCard";
import NavBar from "../../../components/nav_bar/NavBar";
import SideMenu from "../../../components/side_menu/SideMenu";
import Footer from "../../../components/footer/Footer";

import "../../../styles/GlobalStyles.css";
import "./DashboardStyles.css";



const DashboardPage: React.FC = () => {
    const user = useAuth();
    const [accounts, setAccounts] = useState<any[]>([]);
    const [errorMessage, setErrorMessage] = useState("");
    const [showPopup, setShowPopup] = useState(false);
    const navigate = useNavigate();


    useEffect(() => {
        if (!user?.id) {
            setErrorMessage("User not authenticated.");
            return;
        }

        const fetchAccounts = async () => {
            try {
                const response = await api.get(`/api/trademind/trading_accounts/accounts/${user.id}`);

                if (response.status === 404) {
                    setErrorMessage("No trading accounts found.");
                    setShowPopup(true);
                    return;
                }

                const data = response.data;
                if (Array.isArray(data)) {
                    setAccounts(data);
                    if (data.length === 0) {
                        setShowPopup(true);
                    }
                } else {
                    throw new Error("Unexpected response format.");
                }
            } catch (error) {
                setErrorMessage("Failed to load accounts.");
                setShowPopup(true);
            }
        };

        fetchAccounts();
    }, [user]);

    const reloadAccountData = async () => {
        if (!user?.id) return;
        try {
            const userAccounts = await api.get(`/api/trademind/trading_accounts/accounts/${user.id}`);
            const accountsData = await Promise.all(
                userAccounts.data.map(async (acc: any) => {
                    const reloadResp = await api.get(`/api/trademind/trading_accounts/${acc.account_id}/get_account_info/reload`);
                    return { ...acc, ...reloadResp.data };
                })
            );
            setAccounts(accountsData);
            setErrorMessage("");

            if (accountsData.length > 0) {
                setShowPopup(false);
            }

        } catch (error) {
            setErrorMessage("Failed to reload accounts.");
        }
    };


    const handleDeleteAccount = (deletedAccountId: number) => {
        setAccounts((prevAccounts) =>
            prevAccounts.filter((account) => Number(account.account_id) !== deletedAccountId)
        );
    };


    return (
        <div className="app-container">
            <NavBar />
            <div className="main-content">
                <div className="side-menu">
                    <SideMenu />
                </div>

                <div className="page-content">
                    <h2 className="page-title">Your Trading Accounts</h2>

                    {errorMessage && <p className="error-message">{errorMessage}</p>}

                    <div className="account-list">
                        {accounts.length > 0 ? (
                            accounts.map((account) => (
                                <AccountInfoCard
                                    key={account.account_id}
                                    account={account}
                                    onDelete={handleDeleteAccount}
                                />
                            ))
                        ) : (
                            <p>Loading accounts...</p>
                        )}
                        <button className="form-button reload-button" onClick={reloadAccountData}>
                            Reload accounts
                        </button>
                    </div>

                    <Footer/>
                </div>
            </div>

            {showPopup && (
                <div className="credentials-modal">
                    <div className="modal-content">
                        <p className="form-error">
                            You don't have any trading accounts added yet. Please add one to continue.
                        </p>
                        <button className="close-modal" onClick={() => setShowPopup(false)}>✖</button>

                        <div className="modal-buttons">
                            <button className="form-button" onClick={() => navigate("/accounts/add")}>
                                Add Account
                            </button>

                            <button className="form-button" onClick={reloadAccountData}>
                                Reload
                            </button>

                            <button className="form-button" onClick={() => navigate("/home")}>
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            )}


        </div>
    );
};

export default DashboardPage;



