import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import api from "../../configuration/AxiosConfigurations";

import NavBar from "../../components/nav_bar/NavBar";
import SideMenu from "../../components/side_menu/SideMenu";
import Footer from "../../components/footer/Footer";
import GeneralStats from '../statistics/components/GeneralStats';
import BalanceCurveChart from '../statistics/components/BalanceCurveChart';
import LongVsShortStats from '../statistics/components/LongVsShortStats';
import ResultsByInstrument from '../statistics/components/ResultsByInstrument';
import ResultsByDay from '../statistics/components/ResultsByDay';
import ResultsByDuration from '../statistics/components/ResultsByDuration';
import StatExplanationBox from "./components/StatExplanationBox";
import StatBoxWrapper from "./components/StatBoxWrapper";

import './styles/MyStatisticDashboardPage.css';



const MyStatisticDashboardPage: React.FC = () => {
    const { statisticId } = useParams();
    const [result, setResult] = useState<any>(null);

    useEffect(() => {
        const fetchAndGenerate = async () => {
            try {
                const statRes = await api.get(`/api/trademind/statistics/${statisticId}`);
                const statData = statRes.data;
                console.log("send data", statData);
                const genRes = await api.post(`/api/trademind/statistics/generate`, statData);
                const genData = genRes.data;
                console.log("generated data", genData);

                setResult(genData);
            } catch (error) {
                console.error("Error loading statistics:", error);
            }
        };

        fetchAndGenerate();
    }, [statisticId]);

    if (!result) return <div className="dashboard-container">Loading dashboard...</div>;

    return (
        <div className="app-container">
            <NavBar />

            <div className="main-content">
                <div className="side-menu">
                    <SideMenu />
                </div>

                <div className="page-content">
                    <h2 className="page-title">{result.statistic_name}</h2>

                    <StatBoxWrapper title="Performance Overview">
                        <StatExplanationBox title="General Statistics Summary">
                            Summary of trade results, win rate, risk/reward, and profitability.
                        </StatExplanationBox>
                        <GeneralStats metrics={result.metrics} />
                        <BalanceCurveChart data={result?.metrics?.balance_curve || []} />
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

export default MyStatisticDashboardPage;
