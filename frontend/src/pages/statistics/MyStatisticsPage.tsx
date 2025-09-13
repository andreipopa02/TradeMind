import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {useAuth} from "../../configuration/UseAuth";
import {Statistic} from "../../types/StatisticProps";

import api from "../../configuration/AxiosConfigurations";
import StatisticDeleteModal from "./components/StatisticDeleteModal";
import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";
import Footer from "../../components/footer/Footer";

import './styles/MyStatistics.css';



const MyStatisticsPage: React.FC = () => {
    const user = useAuth();
    const [statistics, setStatistics] = useState<Statistic[]>([]);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [statToDelete, setStatToDelete] = useState<Statistic | null>(null);
    const navigate = useNavigate();


    useEffect(() => {
        const fetchUserStatistics = async () => {
            if (!user?.id) return;
            try {
                const response = await api.get(`/api/trademind/statistics/user/${user.id}`);
                setStatistics(response.data);
            } catch (err) {
                console.error("Failed to fetch statistics", err);
            }
        };

        fetchUserStatistics();
    }, [user]);

    const handleCardClick = (statisticId: number) => {
        navigate(`/statistics/my_statistics/${statisticId}`);
    };

    const openDeleteModal = (stat: Statistic) => {
        setStatToDelete(stat);
        setShowDeleteModal(true);
    };

    const handleConfirmDelete = async () => {
        if (!statToDelete) return;

        try {
            await api.delete(`/api/trademind/statistics/${statToDelete.id}`);
            setStatistics((prev) => prev.filter((s) => s.id !== statToDelete.id));
        } catch (err) {
            console.error("Error deleting statistic:", err);
        } finally {
            setShowDeleteModal(false);
            setStatToDelete(null);
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
                    <h2 className="page-title">My Statistics</h2>

                    <div style={{textAlign: 'center', marginBottom: '20px'}}>
                        <button
                            onClick={() => navigate("/statistics/new_statistic")}
                            className="form-button"
                        >
                            Add New Statistic
                        </button>
                    </div>
                    
                    <div className="statistics-grid">
                        {statistics.map((stat) => (
                            <div key={stat.id} className="stat-card">
                                <h3>{stat.name}</h3>
                                <div className="stat-info-grid">
                                    <div className="stat-info-item">
                                        <span>Created</span>
                                        <p>{new Date(stat.created_at).toLocaleDateString()}</p>
                                    </div>
                                    <div className="stat-info-item">
                                        <span>Status</span>
                                        <p>{stat.is_active ? 'Active' : 'Inactive'}</p>
                                    </div>
                                </div>
                                <div className="stat-actions">
                                    <button className="view-button"
                                            onClick={() => handleCardClick(stat.id)}>View
                                    </button>
                                    <button className="delete-button" onClick={() => openDeleteModal(stat)}>Delete
                                    </button>

                                </div>
                            </div>
                        ))}
                    </div>

                    {showDeleteModal && statToDelete && (
                        <StatisticDeleteModal
                            statisticName={statToDelete.name}
                            onCancel={() => setShowDeleteModal(false)}
                            onConfirm={handleConfirmDelete}
                        />
                    )}

                    <Footer />
                </div>
            </div>
        </div>
    );
};

export default MyStatisticsPage;
