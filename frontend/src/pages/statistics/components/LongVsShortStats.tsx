import React from 'react';

import '../styles/LongVsShortStats.css';



interface TradeTypeStatsProps {
    longStats: { count: number; profit: number; winrate: number };
    shortStats: { count: number; profit: number; winrate: number };
}

const LongVsShortStats: React.FC<TradeTypeStatsProps> = ({ longStats, shortStats }) => {
    return (
        <div className="dashboard-section">
            <div className="long-short-grid">

                <div className="trade-type-card">
                    <h4>Long</h4>
                    <p>Trades: {longStats.count}</p>
                    <p>Profit: ${longStats.profit.toFixed(2)}</p>
                    <p>Winrate: {longStats.winrate}%</p>
                </div>

                <div className="trade-type-card">
                    <h4>Short</h4>
                    <p>Trades: {shortStats.count}</p>
                    <p>Profit: ${shortStats.profit.toFixed(2)}</p>
                    <p>Winrate: {shortStats.winrate}%</p>
                </div>

            </div>
        </div>
    );
};

export default LongVsShortStats;