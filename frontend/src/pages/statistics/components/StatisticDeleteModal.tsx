import React from "react";

import "../styles/Modal.css"



interface Props {
    statisticName: string;
    onCancel: () => void;
    onConfirm: () => void;
}

const StatisticDeleteModal: React.FC<Props> = ({ statisticName, onCancel, onConfirm }) => {
    return (
        <div className="credentials-modal">
            <div className="modal-content">
                <h3>Delete Statistic</h3>
                <p>Are you sure you want to delete <strong>{statisticName}</strong>?</p>

                <button className="close-modal" onClick={onCancel}>✖</button>

                <div className="modal-buttons">
                    <button className="delete-confirm" onClick={onConfirm}>Yes, Delete</button>
                    <button className="delete-cancel" onClick={onCancel}>Cancel</button>
                </div>
            </div>
        </div>
    );
};

export default StatisticDeleteModal;
