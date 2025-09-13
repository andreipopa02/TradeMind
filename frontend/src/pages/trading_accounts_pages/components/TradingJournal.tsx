import React, { useMemo, useState } from "react";
import Select from "react-select";
import { uiStyles } from "../../../components/ThemeContext";
import { TradeJournal } from "../../../types/TradeProps";

import "../view_accounts/DashboardStyles.css";
import "./TradingJournal.css";



const TradingJournal: React.FC<{ trades: TradeJournal[] }> = ({ trades }) => {
    const [itemsPerPage, setItemsPerPage] = useState<number>(25);
    const [page, setPage] = useState<number>(1);

    const total = Array.isArray(trades) ? trades.length : 0;
    const totalPages = Math.max(1, Math.ceil(total / itemsPerPage));
    const currentPage = Math.min(page, totalPages);
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const pageSizeOptions = [
        { value: 10, label: "10 / page" },
        { value: 25, label: "25 / page" },
        { value: 50, label: "50 / page" },
        { value: 100, label: "100 / page" },
    ];

    const pageTrades = useMemo(() => {
        if (!Array.isArray(trades) || trades.length === 0) return [];
        return trades.slice(startIndex, endIndex);
    }, [trades, startIndex, endIndex]);

    const goFirst = () => setPage(1);
    const goPrev = () => setPage((p) => Math.max(1, p - 1));
    const goNext = () => setPage((p) => Math.min(totalPages, p + 1));
    const goLast = () => setPage(totalPages);

    return (
        <div className="trading-journal">
            <h2>Trading Journal</h2>

            <div className="pagination-controls">
                <label htmlFor="tj-page-size">Rows per page</label>
                <Select
                    instanceId="tj-page-size"
                    styles={uiStyles}
                    options={pageSizeOptions}
                    value={pageSizeOptions.find(o => o.value === itemsPerPage) || null}
                    onChange={(opt: any) => {
                        setItemsPerPage(opt?.value ?? 25);
                        setPage(1);
                    }}
                    placeholder="Rows per page"
                    isSearchable={false}
                />

                <span className="total-trades">Total trades: {total}</span>
            </div>

            <div className="table-wrapper">
                {total === 0 ? (
                    <p>No trade history available.</p>
                ) : (
                    <table>
                        <thead>
                        <tr>
                            <th>Ticket</th>
                            <th>Symbol</th>
                            <th>Volume</th>
                            <th>Price</th>
                            <th>Commission</th>
                            <th>Swap</th>
                            <th>Profit</th>
                            <th>Time</th>
                        </tr>
                        </thead>
                        <tbody>
                        {pageTrades.map((trade, index) => (
                            <tr key={`${trade.ticket ?? "row"}-${startIndex + index}`}>
                                <td>{trade.ticket ?? "N/A"}</td>
                                <td>{trade.symbol ?? "N/A"}</td>
                                <td>{trade.volume !== undefined ? trade.volume.toLocaleString() : "N/A"}</td>
                                <td>{trade.price !== undefined ? trade.price.toFixed(5) : "N/A"}</td>
                                <td>{trade.commission !== undefined ? trade.commission.toFixed(2) : "N/A"}</td>
                                <td>{trade.swap !== undefined ? trade.swap.toFixed(2) : "N/A"}</td>
                                <td
                                    style={{
                                        color: trade.profit !== undefined && trade.profit < 0 ? "red" : "green",
                                        fontWeight: "bold",
                                    }}
                                >
                                    {trade.profit !== undefined ? `${trade.profit.toFixed(2)} USD` : "N/A"}
                                </td>
                                <td>
                                    {trade.time
                                        ? new Date(
                                            typeof trade.time === "string" ? parseInt(trade.time) * 1000 : trade.time * 1000
                                        ).toLocaleString()
                                        : "N/A"}
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                )}
            </div>

            <div className="pagination-nav">
                <button onClick={goFirst} disabled={currentPage === 1}>« First</button>
                <button onClick={goPrev} disabled={currentPage === 1}>‹ Prev</button>
                <span>
          Page {currentPage} / {totalPages}
        </span>
                <button onClick={goNext} disabled={currentPage === totalPages}>Next ›</button>
                <button onClick={goLast} disabled={currentPage === totalPages}>Last »</button>
            </div>
        </div>
    );
};

export default TradingJournal;
