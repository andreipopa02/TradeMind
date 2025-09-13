import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from "../../configuration/UseAuth";
import api from "../../configuration/AxiosConfigurations";

import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";
import Footer from "../../components/footer/Footer";
import ConfirmDeleteBacktestModal from "./components/ConfirmDeleteBacktestModal";

import "./MyBacktestsPage.css";



interface Backtest {
    id: number;
    name: string;
    created_at: string;
    total_profit: number;
    nr_trades: number;
}

const MyBacktestsPage: React.FC = () => {
    const [backtests, setBacktests] = useState<Backtest[]>([]);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [selectedBacktest, setSelectedBacktest] = useState<Backtest | null>(null);

    const navigate = useNavigate();
    const user = useAuth();


    const openDeleteModal = (backtest: Backtest) => {
        setSelectedBacktest(backtest);
        setShowDeleteModal(true);
    };

    const closeDeleteModal = () => {
        setSelectedBacktest(null);
        setShowDeleteModal(false);
    };

    const handleDeletedBacktest = () => {
        if (selectedBacktest) {
            setBacktests(prev => prev.filter(bt => bt.id !== selectedBacktest.id));
        }
        closeDeleteModal();
    };

    const handleCardClick = (backtestId: number) => {
        navigate(`/backtesting/my_backtests/${backtestId}`);
    };

    useEffect(() => {
        const fetchUserBacktests = async () => {
            if (!user?.id) return;
            try {
                const response = await api.get(`/api/trademind/backtests/user/${user.id}`);
                setBacktests(response.data);
            } catch (err) {
                console.error("Failed to fetch backtests", err);
            }
        };
        fetchUserBacktests();
    }, [user]);


    return (
        <div className="app-container">
            <NavBar />
            <div className="main-content">
                <div className="side-menu">
                    <SideMenu/>
                </div>

                <div className="page-content">
                    <h2 className="page-title">My Backtests</h2>

                    <div className="mybt-grid">
                        {backtests.map((bt) => (
                            <div key={bt.id} className="mybt-card">
                                <h3>{bt.name}</h3>

                                <div className="mybt-info-grid">
                                    <div className="mybt-info-item">
                                        <span>Created</span>
                                        <p>{new Date(bt.created_at).toLocaleDateString()}</p>
                                    </div>
                                    <div className="mybt-info-item">
                                        <span>Total Profit</span>
                                        <p>{bt.total_profit}</p>
                                    </div>
                                    <div className="mybt-info-item">
                                        <span>Trades</span>
                                        <p>{bt.nr_trades}</p>
                                    </div>
                                </div>

                                <div className="mybt-actions">
                                    <button className="view-button" onClick={() => handleCardClick(bt.id)}>View</button>
                                    <button className="delete-button" onClick={() => openDeleteModal(bt)}>Delete
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>

                    {showDeleteModal && selectedBacktest && (
                        <ConfirmDeleteBacktestModal
                            backtest={selectedBacktest}
                            onClose={closeDeleteModal}
                            onDeleted={handleDeletedBacktest}
                        />
                    )}

                    <Footer/>
                </div>
            </div>
        </div>
    );
};

export default MyBacktestsPage;
