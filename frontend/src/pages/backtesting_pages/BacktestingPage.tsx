import React, { useState, useEffect } from "react";
import api from "../../configuration/AxiosConfigurations";
import {useAuth} from "../../configuration/UseAuth";

import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";
import BacktestChart from "./components/BacktestChart";
import SymbolTimeframeCard from "./components/SymbolTimeframeCard";
import BacktestMetricsCard from "./components/BacktestMetricsCard";
import BacktestParametersCard from "./components/BacktestParametersCard";
import Footer from "../../components/footer/Footer";

import "../../styles/FormStyles.css";
import "./BacktestingPage.css";


const symbolsByCategory = {
    crypto: ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"],
    forex: ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"],
    indices: ["GER40", "US100", "US30", "UK100", "SP500"]
};

interface Candle {
    time: number;
    open: number;
    high: number;
    low: number;
    close: number;
}

interface PageExecutedTrade {
    entry_id: number;
    exit_id: number;
    entry_action: string;
    exit_action: string;
    entry_price: number;
    exit_price: number;
    profit: number;
    open_timestamp: number;
    close_timestamp: number;
    sl_price?: number;
    tp_price?: number;
}


const getLastMonday = (date: Date) => {
    const day = date.getDay();
    const diff = date.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(date.setDate(diff));
};

const getNextWeek = (date: Date) => {
    const next = new Date(date);
    next.setDate(date.getDate() + 7);
    return next;
};

const getPreviousWeek = (date: Date) => {
    const prev = new Date(date);
    prev.setDate(date.getDate() - 7);
    return prev;
};

const formatDate = (date: Date): string => date.toISOString().split("T")[0];

const getSource = (symbol: string): "crypto" | "forex" | "indices" => {
    if (symbolsByCategory.crypto.includes(symbol)) return "crypto";
    if (symbolsByCategory.forex.includes(symbol)) return "forex";
    return "indices";
};

const BacktestingPage: React.FC = () => {
    const today = new Date();
    const lastMonday = getLastMonday(new Date(today));
    const lastSunday = new Date(lastMonday);
    lastSunday.setDate(lastMonday.getDate() + 6);

    const user = useAuth();
    const [symbol, setSymbol] = useState("BTCUSDT");
    const [startDate, setStartDate] = useState(formatDate(new Date()));
    const [endDate, setEndDate] = useState(formatDate(new Date()));
    const [timeframe, setTimeframe] = useState("1m");
    const [strategy_id, setStrategy] = useState("");
    const [initial_balance, setInitialBalance] = useState(100000);
    const [risk_per_trade, setRiskPerTrade] = useState(1.0);
    const [riskReward, setRiskReward] = useState(1);
    const [candles, setCandles] = useState<Candle[]>([]);
    const [trades, setTrades] = useState<PageExecutedTrade[]>([]);
    const [metrics, setMetrics] = useState<any>(null);
    const [availableStrategies, setAvailableStrategies] = useState<{ id: number; name: string }[]>([]);
    const [strategyType, setStrategyType] = useState<"public" | "personal">("public");
    const [userStrategies, setUserStrategies] = useState<{ id: number; name: string }[]>([]);
    const [chartError, setChartError] = useState<string | null>(null);
    const [backtestError, setBacktestError] = useState<string | null>(null);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [saveStatus, setSaveStatus] = useState<"success" | "error" | null>(null);
    const [saveMessage, setSaveMessage] = useState<string | null>(null);



    const fetchStrategies = async () => {
        try {
            const resPublic = await api.get("/api/trademind/strategies/public");
            const publicList = resPublic.data.map((strategy: any) => ({
                id: strategy.id,
                name: strategy.name
            }));

            let userList: { id: number; name: string }[] = [];

            if (user) {
                const resUser = await api.get(`/api/trademind/strategies/user/${user.id}`);
                userList = resUser.data.map((strategy: any) => ({
                    id: strategy.id,
                    name: strategy.name
                }));
            }

            setAvailableStrategies(publicList);
            setUserStrategies(userList);
        } catch (err) {
            console.error("Failed to fetch strategies:", err);
        }
    };

    const runBacktest = async () => {
        setBacktestError(null);
        if (!strategy_id || !user?.id) {
            setBacktestError("Please select a strategy before running the backtest.");
            return;
        }

        const payload = {
            user_id: user.id,
            strategy_id: parseInt(strategy_id),
            symbol,
            time_frame: timeframe,
            start_date: startDate,
            end_date: endDate,
            initial_balance,
            risk_per_trade,
            risk_reward_ratio: riskReward
        };

        try {
            const res = await api.post("/api/trademind/backtests/preview", payload);
            setTrades(res.data.executed_trades);
            setMetrics(res.data.metrics);
            console.log(res.data);
        } catch (err) {
            console.error("Error running backtest:", err);
            setBacktestError("Backtest failed. Please check your inputs and try again.");
        }
    };

    useEffect(() => {
        document.body.classList.toggle("chart-fullscreen", isFullscreen);
        return () => document.body.classList.remove("chart-fullscreen");
    }, [isFullscreen]);

    const fetchChartData = () => {
        setTrades([]);
        setMetrics(null);
        setCandles([]);

        setChartError(null);
        if (!validateInputs()) return;

        const todayStr = formatDate(new Date());
        if (startDate === todayStr && endDate === todayStr) {
            setChartError("Start date and End date cannot both be today.");
            return;
        }

        if (startDate === endDate) {
            setChartError("Start date and End date cannot be the same.");
            return;
        }


        api.post("/api/trademind/chart-data", {
            symbol,
            source: getSource(symbol),
            time_frame: timeframe,
            start_date: startDate,
            end_date: endDate
        }).then(res => {
            setCandles(res.data.candles);
        }).catch(err => {
            console.error("Error fetching chart data:", err);
            setChartError("Something went wrong. Please check your inputs.");
        }).finally(() => {

        });
    };

    const updateWeek = (direction: "prev" | "next") => {
        const currentStart = new Date(startDate);
        const newStart = direction === "prev" ? getPreviousWeek(currentStart) : getNextWeek(currentStart);
        const newEnd = new Date(newStart);
        newEnd.setDate(newStart.getDate() + 6);
        setStartDate(formatDate(newStart));
        setEndDate(formatDate(newEnd));
    };

    const validateInputs = (): boolean => {
        const todayStr = formatDate(new Date());
        const source = getSource(symbol);

        if (endDate > todayStr) {
            setChartError("End date cannot be in the future.");
            return false;
        }
        if (source === "crypto" && ["60m", "daily"].includes(timeframe)) {
            setChartError("Crypto does not support intervals higher than 1 hour.");
            return false;
        }
        if (source === "forex" && timeframe === "1m") {
            setChartError("Forex pairs does not support 1-minute data.");
            return false;
        }
        return true;
    };

    const saveBacktest = async () => {
        if (!user?.id) {
            setSaveStatus("error");
            setSaveMessage("User not authenticated.");
            return;
        }

        try {
            const payload = {
                user_id: user.id,
                strategy_id: parseInt(strategy_id),
                symbol,
                time_frame: timeframe,
                start_date: startDate,
                end_date: endDate,
                initial_balance,
                risk_per_trade,
                risk_reward_ratio: riskReward,
                metrics,
                executed_trades: trades
            };

            const res = await api.post("/api/trademind/backtests/save", payload);
            console.log("Saved backtest:", res.data);
            setSaveStatus("success");
            setSaveMessage("Backtest saved successfully!");
        } catch (err) {
            console.error("Error saving backtest:", err);
            setSaveStatus("error");
            setSaveMessage("Failed to save backtest.");
        }
    };

    useEffect(() => {
        fetchStrategies();
    }, []);


    return (
        <div className="app-container">
            <NavBar />
            <div className="main-content">
                <div className="side-menu"><SideMenu /></div>

                <div className="page-content">
                    <h2 className="page-title">Backtesting</h2>

                    <div className="backtesting-grid">
                        <SymbolTimeframeCard
                            symbol={symbol} setSymbol={setSymbol}
                            timeframe={timeframe} setTimeframe={setTimeframe}
                            startDate={startDate} setStartDate={setStartDate}
                            endDate={endDate} setEndDate={setEndDate}
                            updateWeek={updateWeek} fetchChartData={fetchChartData}
                            chartError={chartError}
                            symbolsByCategory={symbolsByCategory}
                        />

                        <BacktestParametersCard
                            strategyType={strategyType} setStrategyType={setStrategyType}
                            strategy_id={strategy_id} setStrategy={setStrategy}
                            availableStrategies={availableStrategies}
                            userStrategies={userStrategies}
                            initial_balance={initial_balance} setInitialBalance={setInitialBalance}
                            risk_per_trade={risk_per_trade} setRiskPerTrade={setRiskPerTrade}
                            riskReward={riskReward} setRiskReward={setRiskReward}
                            runBacktest={runBacktest} backtestError={backtestError}
                        />

                        {metrics && (
                            <BacktestMetricsCard
                                metrics={metrics}
                                saveBacktest={saveBacktest}
                                saveStatus={saveStatus}
                                saveMessage={saveMessage}
                            />
                        )}

                    </div>

                    <div className="backtesting-grid">
                        <div className={`backtest-card chart-wide ${isFullscreen ? "fullscreen" : ""}`}>
                            <div className="chart-controls">
                                {!isFullscreen ? (
                                    <button onClick={() => setIsFullscreen(true)}>Full Screen</button>
                                ) : (
                                    <button onClick={() => setIsFullscreen(false)}>Exit Full Screen</button>
                                )}
                            </div>

                            <BacktestChart candles={candles} trades={trades}/>
                        </div>
                    </div>

                    <Footer/>
                </div>
            </div>
        </div>
    );
};

export default BacktestingPage;
