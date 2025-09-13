import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from "../../configuration/AxiosConfigurations";
import {useAuth} from "../../configuration/UseAuth";
import {Clock, DollarSign, Percent, Scale, TrendingDown, TrendingUp, Trophy} from "lucide-react";

import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";
import Footer from "../../components/footer/Footer";
import { Trade } from "../../types/Trade";
import TradeTable from "../statistics/components/TradeTabel";
import BalanceCurveChart from '../statistics/components/BalanceCurveChart';
import LongVsShortStats from '../statistics/components/LongVsShortStats';
import ResultsByInstrument from '../statistics/components/ResultsByInstrument';
import ResultsByDay from '../statistics/components/ResultsByDay';
import ResultsByDuration from '../statistics/components/ResultsByDuration';
import { StatCard } from '../statistics/components/GeneralStats';
import StatExplanationBox from "../statistics/components/StatExplanationBox";
import StatBoxWrapper from "../statistics/components/StatBoxWrapper";

import '../statistics/styles/GeneralStatsStyles.css';



interface BacktestDetails {
    id: number;
    name: string;
    created_at: string;
    total_profit: number;
    drawdown_max: number;
    winrate: number;
    nr_trades: number;
    profit_factor: number | null;
    expectancy: number;
    balance_curve?: { trade: number; balance: number }[];
}

const BacktestDetailsPage: React.FC = () => {
    const user = useAuth();
    const { backtestId } = useParams<{ backtestId: string }>();
    const [backtest, setBacktest] = useState<BacktestDetails | null>(null);
    const [trades, setTrades] = useState<Trade[]>([]);
    const [loading, setLoading] = useState(true);
    const [result, setResult] = useState<any>(null);


    useEffect(() => {
        const fetchBacktestData = async () => {
            if (!user?.id) return;
            try {
                const [backtestRes, tradesRes] = await Promise.all([
                    api.get(`/api/trademind/backtests/${backtestId}`),
                    api.get(`/api/trademind/trades/backtest/${backtestId}`),
                ]);

                setBacktest(backtestRes.data);
                setTrades(tradesRes.data);


                const payload = {
                    user_id: user.id,
                    name: `Backtest ${backtestRes.data?.name || backtestId}`,
                    params: {
                        source_type: "BACKTEST",
                        backtest_id: Number(backtestId),
                    },
                };

                const genRes = await api.post(`/api/trademind/statistics/generate`, payload);

                setResult(genRes.data);

            } catch (err) {
                console.error("Failed to fetch backtest details", err);
            } finally {
                setLoading(false);
            }
        };
        fetchBacktestData();
    }, [user?.id, backtestId]);

    if (loading) return <p>Loading...</p>;
    if (!backtest) return <p>No backtest data found.</p>;

    return (
        <div className="app-container">
            <NavBar />
            <div className="main-content">
                <div className="side-menu">
                    <SideMenu />
                </div>

                <div className="page-content">
                    <h2 className="page-title">{backtest.name}</h2>

                    <StatBoxWrapper title="Performance Overview">
                        <StatExplanationBox title="General Statistics Summary">
                            Summary of trade results, win rate, risk/reward, and profitability.
                        </StatExplanationBox>
                        <div className="general-stats-grid">
                        <StatCard icon={DollarSign} label="Total Profit"
                                  value={`$${(backtest.total_profit ?? 0).toFixed(2)}`}
                                  positive={backtest.total_profit >= 0}
                        />
                        <StatCard icon={TrendingDown} label="Max Drawdown"
                                  value={`$${(backtest.drawdown_max ?? 0).toFixed(2)}`}
                                  positive={false}
                        />
                        <StatCard icon={Percent} label="Winrate"
                                  value={`${(backtest.winrate ?? 0).toFixed(2)}%`}
                                  positive={backtest.winrate >= 50}
                        />
                        <StatCard icon={TrendingUp} label="Trades"
                                  value={`${backtest.nr_trades ?? 0}`}
                                  positive={backtest.nr_trades > 0}
                        />
                        <StatCard icon={Scale} label="Profit Factor"
                                  value={`${(backtest.profit_factor ?? 0).toFixed(2)}`}
                        />
                        <StatCard icon={Trophy} label="Expectancy"
                                  value={`$${(backtest.expectancy ?? 0).toFixed(2)}`}
                                  positive={backtest.expectancy >= 0}
                        />
                        <StatCard icon={Clock} label="Created At"
                                  value={new Date(backtest.created_at).toLocaleDateString()}
                        />
                    </div>

                        <BalanceCurveChart data={backtest?.balance_curve || []} />
                    </StatBoxWrapper>

                    <StatBoxWrapper title="Trades">
                        <TradeTable
                            trades={trades}
                            onEdit={() => {}}
                            onDelete={() => {}}
                            onAddNew={() => {}}
                            onSortChange={() => {}}
                            hideAddButton
                        />
                    </StatBoxWrapper>

                    <StatBoxWrapper title="Long vs Short Comparison">
                        <StatExplanationBox title="">
                            You've executed <strong>{result.metrics.long_stats.count}</strong> long
                            trades and <strong>{result.metrics.short_stats.count}</strong> short
                            trades. Long trades resulted in a total profit
                            of <strong>${result.metrics.long_stats.profit}</strong> and a winrate
                            of <strong>{result.metrics.long_stats.winrate}%</strong>.
                            Meanwhile, short trades
                            accumulated <strong>${result.metrics.short_stats.profit}</strong> with a winrate
                            of <strong>{result.metrics.short_stats.winrate}%</strong>.
                            This breakdown reveals which direction performed better.
                        </StatExplanationBox>


                        <LongVsShortStats
                            longStats={result.metrics?.long_stats || {count: 0, profit: 0, winrate: 0}}
                            shortStats={result.metrics?.short_stats || {count: 0, profit: 0, winrate: 0}}
                        />
                    </StatBoxWrapper>

                    <StatBoxWrapper title="Performance by Instrument">
                        <StatExplanationBox title="">
                            This section analyzes your trading performance across different instruments.
                            You traded a total of <strong>{result.metrics.by_instrument.length}</strong> markets.
                            Each market displays its number of trades and total profit/loss, offering insights into
                            which instruments contributed
                            most to your overall performance.
                        </StatExplanationBox>

                        <ResultsByInstrument data={result.metrics?.by_instrument || []}/>
                    </StatBoxWrapper>

                    <StatBoxWrapper title="Performance by Day">
                        <StatExplanationBox title="">
                            This breakdown shows how trades performed based on the day they were opened.
                            Identifying profitable days can help you spot weekly behavioral or volatility patterns
                            in your strategy.
                        </StatExplanationBox>

                        <ResultsByDay data={result.metrics?.by_day || []}/>
                    </StatBoxWrapper>

                    <StatBoxWrapper title="Performance by Trade Duration">
                        <StatExplanationBox title="">
                            The table below segments your trades by duration. Each range reflects how long trades
                            were held and the
                            associated results. This is particularly useful to understand whether your strategy
                            benefits from short-term
                            or long-term setups.
                        </StatExplanationBox>

                        <ResultsByDuration data={result.metrics?.by_duration || []}/>

                    </StatBoxWrapper>

                    <br/>

                    <Footer />
                </div>
            </div>
        </div>
    );
};

export default BacktestDetailsPage;
