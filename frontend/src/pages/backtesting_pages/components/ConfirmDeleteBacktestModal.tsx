import React from "react";
import api from "../../../configuration/AxiosConfigurations";

import "./ConfirmDeleteBacktestModal.css";



interface ConfirmDeleteBacktestModalProps {
    backtest: { id: number; name: string; created_at: string };
    onClose: () => void;
    onDeleted: () => void;
}

const ConfirmDeleteBacktestModal: React.FC<ConfirmDeleteBacktestModalProps> = ({ backtest, onClose, onDeleted }) => {
    const handleDelete = async () => {
        try {
            const response = await api.delete(`/api/trademind/backtests/${backtest.id}`);
            if (response.status !== 200 && response.status !== 204) {
                throw new Error("Failed to delete backtest");
            }
            onDeleted();
        } catch (error) {
            console.error("Error deleting backtest:", error);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h3>Confirm Delete</h3>

                <p>Are you sure you want to delete this backtest session?</p>
                <p>
                    <strong>{backtest.name}</strong> created on {new Date(backtest.created_at).toLocaleDateString()}
                </p>

                <div className="modal-buttons">
                    <button className="delete-btn" onClick={handleDelete}>Delete</button>
                    <button className="cancel-btn" onClick={onClose}>Cancel</button>
                </div>

            </div>
        </div>
    );
};

export default ConfirmDeleteBacktestModal;
