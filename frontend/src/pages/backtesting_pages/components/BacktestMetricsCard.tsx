import React from "react";



interface Metrics {
    total_profit: number;
    drawdown_max: number;
    winrate: number;
    nr_trades: number;
    profit_factor: number | null;
    expectancy: number;
}

interface Props {
    metrics: Metrics;
    saveBacktest: () => void;
    saveStatus?: "success" | "error" | null;
    saveMessage?: string | null;
}

const BacktestMetricsCard: React.FC<Props> = ({ metrics, saveBacktest, saveStatus, saveMessage }) => (
    <div className="backtest-card backtest-metrics-card">
        <h3>Backtest Metrics</h3>

        <div className="backtest-info-grid">
            <div className="backtest-info-item"><span>Total Profit</span><p>{metrics.total_profit}</p></div>
            <div className="backtest-info-item"><span>Max Drawdown</span><p>{metrics.drawdown_max}</p></div>
            <div className="backtest-info-item"><span>Winrate</span><p>{metrics.winrate}%</p></div>
            <div className="backtest-info-item"><span>Trades</span><p>{metrics.nr_trades}</p></div>
            <div className="backtest-info-item"><span>Profit Factor</span><p>{metrics.profit_factor}</p></div>
            <div className="backtest-info-item"><span>Expectancy</span><p>{metrics.expectancy}</p></div>
        </div>

        <div className="backtest-actions">
            <button className="backtest-button" onClick={saveBacktest}>
                Save Backtest & Create Statistics
            </button>
        </div>

        {saveMessage && (
            <div className={saveStatus === "success" ? "form-success" : "form-error"}>
                {saveMessage}
            </div>
        )}
    </div>
);

export default BacktestMetricsCard;
