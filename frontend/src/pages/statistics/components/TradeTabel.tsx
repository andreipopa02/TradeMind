import React, { useState } from "react";
import Select from "react-select";

import { Trade } from "../../../types/Trade";
import { uiStyles } from "../../../components/ThemeContext";
import TradeRow from "./TradeRow";

import "../styles/TradeTable.css";



interface TradeTableProps {
    trades: Trade[];
    onEdit: (trade: Trade) => void;
    onDelete: (trade: Trade) => void;
    onAddNew: () => void;
    onSortChange: (field: keyof Trade) => void;

    hideAddButton?: boolean;
}

const TradeTable: React.FC<TradeTableProps> = ({
                 trades,  onEdit, onDelete, onAddNew, onSortChange, hideAddButton = false,}) => {
    const [currentPage, setCurrentPage] = useState(1);
    const [tradesPerPage, setTradesPerPage] = useState(10);

    const totalPages = Math.ceil(trades.length / tradesPerPage);
    const indexOfLastTrade = currentPage * tradesPerPage;
    const indexOfFirstTrade = indexOfLastTrade - tradesPerPage;
    const currentTrades = trades.slice(indexOfFirstTrade, indexOfLastTrade);
    const pageSizeOptions = [
        { value: 10, label: "10 / page" },
        { value: 25, label: "25 / page" },
        { value: 50, label: "50 / page" },
    ];
    const handlePageChange = (newPage: number) => {
        if (newPage >= 1 && newPage <= totalPages) {
            setCurrentPage(newPage);
        }
    };

    return (
        <div className="trade-table-container">
            <div className="pagination-controls">
                <label>Show: </label>
                <Select
                    instanceId="trade-table-page-size"
                    styles={uiStyles}
                    options={pageSizeOptions}
                    value={pageSizeOptions.find((o) => o.value === tradesPerPage) || null}
                    onChange={(opt: any) => {
                        setTradesPerPage(opt?.value ?? 10);
                        setCurrentPage(1);
                    }}
                    placeholder="Rows per page"
                    isSearchable={false}
                    menuPortalTarget={document.body}
                    menuPosition="fixed"
                    menuShouldScrollIntoView={false}
                />

                <span className="total-trades">Total Trades: {trades.length}</span>

                {!hideAddButton && (
                    <button className="add-trade-btn" onClick={onAddNew}>
                        Add New Trade
                    </button>
                )}
            </div>

            <div className="table-wrapper">
                <table className="trade-table">
                    <thead>
                    <tr>
                        <th onClick={() => onSortChange("market")}>Market ⬍</th>
                        <th>Volume</th>
                        <th>Type</th>
                        <th onClick={() => onSortChange("open_date")}>Open Date ⬍</th>
                        <th>Open Time</th>
                        <th>Close Date</th>
                        <th>Close Time</th>
                        <th>Session</th>
                        <th>Open Price</th>
                        <th>TP Price</th>
                        <th>SL Price</th>
                        <th>Close Price</th>
                        <th onClick={() => onSortChange("profit")}>Profit ⬍</th>
                        <th>Swap</th>
                        <th>Commission</th>
                        <th>Pips</th>
                        <th>Photo Link</th>
                    </tr>
                    </thead>
                    <tbody>
                    {currentTrades.map((trade) => (
                        <TradeRow key={trade.id} trade={trade} onEdit={onEdit} onDelete={onDelete} />
                    ))}
                    </tbody>
                </table>
            </div>

            <div className="pagination-nav">
                <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
                    ◀ Prev
                </button>
                <span>
          Page {currentPage} of {totalPages}
        </span>
                <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
                    Next ▶
                </button>
            </div>
        </div>
    );
};

export default TradeTable;
