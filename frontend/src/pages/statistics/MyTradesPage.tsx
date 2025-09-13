import React, { useEffect, useState } from "react";
import {useAuth} from "../../configuration/UseAuth";
import { Trade } from "../../types/Trade";
import Select from "react-select";
import { uiStyles } from "../../components/ThemeContext";

import api from "../../configuration/AxiosConfigurations";
import TradeTable from "./components/TradeTabel"
import TradeFormModal from "./components/TradeFormModal";
import ConfirmDeleteModal from "./components/ConfirmDeleteModal";
import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";
import Footer from "../../components/footer/Footer";

import "../../styles/GlobalStyles.css"
import "./styles/MyTradesPage.css"



type Source = "personal" | "backtest";

const MyTradesPage = () => {
    const user = useAuth();
    const [trades, setTrades] = useState<Trade[]>([]);
    const [selectedTrade, setSelectedTrade] = useState<Trade | undefined>(undefined);
    const [showForm, setShowForm] = useState(false);
    const [showDelete, setShowDelete] = useState(false);
    const [sortField, setSortField] = useState<keyof Trade>("open_date");
    const [sortOrder, setSortOrder] = useState("asc");
    const [tradeSource, setTradeSource] = useState<Source>("personal");
    const [selectedBacktestId, setSelectedBacktestId] = useState<number | null>(null);
    const [backtests, setBacktests] = useState<{ id: number; name: string }[]>([]);
    const sourceOptions = [
        { value: "personal", label: "Personal" },
        { value: "backtest", label: "Backtest" },
    ] as const;

    const backtestOptions = backtests.map(bt => ({ value: bt.id, label: bt.name }));

    const fetchTrades = async () => {
        if (!user?.id) return;

        try {
            if (tradeSource === "personal") {
                const response = await api.get(`/api/trademind/trades/user/${user.id}`);
                setTrades(Array.isArray(response.data) ? response.data : []);
            } else if (tradeSource === "backtest" && selectedBacktestId) {
                const response = await api.get(`/api/trademind/trades/backtest/${selectedBacktestId}`);
                setTrades(Array.isArray(response.data) ? response.data : []);
            }
        } catch (err) {
            console.error("Error fetching trades:", err);
            setTrades([]);
        }
    };

    const fetchBacktests = async () => {
        if (!user?.id) return;
        try {
            const res = await api.get(`/api/trademind/backtests/user/${user.id}`);
            console.log("Backtests response:", res.data);

            setBacktests(res.data.map((bt: any) => ({
                id: bt.id,
                name: bt.name || `Unnamed (${bt.id})`
            })));
        } catch (err) {
            console.error("Error fetching backtests:", err);
        }
    };

    const sortedTrades = [...trades].sort((a, b) => {
        if (sortField === "profit") return sortOrder === "asc"
            ? (a.profit || 0) - (b.profit || 0)
            : (b.profit || 0) - (a.profit || 0);
        if (sortField === "market") return sortOrder === "asc"
            ? a.market.localeCompare(b.market)
            : b.market.localeCompare(a.market);
        if (sortField === "open_date") return sortOrder === "asc"
            ? new Date(a.open_date || "").getTime() - new Date(b.open_date || "").getTime()
            : new Date(b.open_date || "").getTime() - new Date(a.open_date || "").getTime();
        return 0;
    });

    useEffect(() => {
        fetchTrades();
        fetchBacktests();
    }, [user, tradeSource, selectedBacktestId]);



    return (
        <div className="app-container">
            <NavBar />

            <div className="main-content">
                <div className="side-menu">
                    <SideMenu />
                </div>

                <div className="page-content">
                    <h2 className="page-title">My Trades</h2>

                    <div className="pagination-controls">
                        <label>Source: </label>
                        <Select
                            styles={uiStyles}
                            options={sourceOptions}
                            value={sourceOptions.find(o => o.value === tradeSource) ?? null}
                            onChange={(opt) => setTradeSource(opt?.value ?? "personal")}
                            placeholder="Select source..."
                            menuPortalTarget={document.body}
                            menuPosition="fixed"
                        />

                        {tradeSource === "backtest" && (
                            <Select
                                styles={uiStyles}
                                options={backtestOptions}
                                value={selectedBacktestId ? backtestOptions.find(o => o.value === selectedBacktestId) ?? null : null}
                                onChange={(opt) => setSelectedBacktestId(opt ? opt.value : null)}
                                placeholder="-- Select a Backtest Session --"
                                isClearable
                                menuPortalTarget={document.body}
                                menuPosition="fixed"
                            />
                        )}

                    </div>

                    <TradeTable
                        trades={sortedTrades}
                        onEdit={(trade: Trade) => {
                            setSelectedTrade(trade);
                            setShowForm(true);
                        }}
                        onDelete={(trade: Trade) => {
                            setSelectedTrade(trade);
                            setShowDelete(true);
                        }}
                        onAddNew={() => {
                            setSelectedTrade(undefined);
                            setShowForm(true);
                        }}
                        onSortChange={(field: keyof Trade) => {
                            setSortOrder(sortOrder === "asc" ? "desc" : "asc");
                            setSortField(field);
                        }}
                    />


                    {showForm && (
                        <TradeFormModal
                            trade={selectedTrade}
                            onClose={() => setShowForm(false)}
                            onSuccess={() => {
                                fetchTrades();
                                setShowForm(false);
                            }}
                        />
                    )}

                    {showDelete && selectedTrade && (
                        <ConfirmDeleteModal
                            trade={selectedTrade}
                            onClose={() => setShowDelete(false)}
                            onDeleted={() => {
                                fetchTrades();
                                setShowDelete(false);
                            }}
                        />
                    )}

                    <Footer/>
                </div>
            </div>
        </div>
    );
};

export default MyTradesPage;
