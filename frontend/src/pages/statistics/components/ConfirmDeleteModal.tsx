import React from "react";

import { Trade } from "../../../types/Trade";
import api from "../../../configuration/AxiosConfigurations";

import "../styles/ConfirmDeleteModal.css";



interface ConfirmDeleteModalProps {
    trade: Trade;
    onClose: () => void;
    onDeleted: () => void;
}

const ConfirmDeleteModal: React.FC<ConfirmDeleteModalProps> = ({ trade, onClose, onDeleted }) => {
    const handleDelete = async () => {
        try {
            console.log(trade)
            if (trade.source_type !== "user") {
                alert("Only trades with source type USER can be deleted.");
                return;
            }

            const response = await api.delete(`/api/trademind/trades/${trade.id}`);
            if (response.status !== 200 && response.status !== 204) {
                throw new Error("Failed to delete trade");
            }
            onDeleted();
        } catch (error) {
            console.error("Error deleting trade:", error);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h3>Confirm Delete</h3>
                <p>Are you sure you want to delete this trade?</p>
                <p><strong>{trade?.market ?? "Unknown Market"}</strong> from {trade?.open_date ?? "Unknown Date"} opened with {trade?.volume ?? "Unknown"} lots</p>

                <div className="modal-buttons">
                    <button className="delete-btn" onClick={handleDelete}>Delete</button>
                    <button className="cancel-btn" onClick={onClose}>Cancel</button>
                </div>
            </div>
        </div>
    );
};

export default ConfirmDeleteModal;
