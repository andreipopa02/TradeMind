import React from "react";
import Select from "react-select";

import {ui2Styles} from "../../../components/ThemeContext";



interface Props {
    symbol: string;
    setSymbol: (s: string) => void;
    timeframe: string;
    setTimeframe: (tf: string) => void;
    startDate: string;
    setStartDate: (d: string) => void;
    endDate: string;
    setEndDate: (d: string) => void;
    updateWeek: (dir: "prev" | "next") => void;
    fetchChartData: () => void;
    chartError: string | null;
    symbolsByCategory: {
        crypto: string[];
        forex: string[];
        indices: string[];
    };
}

const timeframes = ["1m", "5m", "15m", "30m", "60m", "daily"];

const SymbolTimeframeCard: React.FC<Props> = ({
                                                  symbol, setSymbol,
                                                  timeframe, setTimeframe,
                                                  startDate, setStartDate,
                                                  endDate, setEndDate,
                                                  updateWeek, fetchChartData,
                                                  chartError, symbolsByCategory
                                              }) => {

    const groupedSymbolOptions = [
        {
            label: "Crypto",
            options: symbolsByCategory.crypto.map(s => ({ value: s, label: s })),
        },
        {
            label: "Forex",
            options: symbolsByCategory.forex.map(s => ({ value: s, label: s })),
        },
        {
            label: "Indices",
            options: symbolsByCategory.indices.map(s => ({ value: s, label: s })),
        },
    ];

    const timeframeOptions = timeframes.map(tf => ({ value: tf, label: tf }));

    return (
        <div className="backtest-card">
            <h3>Select symbol and time frame</h3>

            <div className="backtest-info-item">
                <span>Symbol</span>
                <Select
                    styles={ui2Styles}
                    options={groupedSymbolOptions as any}
                    value={{ value: symbol, label: symbol }}
                    onChange={(opt: any) => setSymbol(opt?.value ?? symbol)}
                    placeholder="Select symbol"
                    classNamePrefix="tmselect"
                    menuPortalTarget={document.body}
                    menuPosition="fixed"
                    menuShouldScrollIntoView={false}
                    maxMenuHeight={260}
                />
            </div>

            <div className="backtest-info-item">
                <span>Time Frame</span>
                <Select
                    styles={ui2Styles}
                    options={timeframeOptions}
                    value={timeframeOptions.find(o => o.value === timeframe) ?? null}
                    onChange={(opt: any) => setTimeframe(opt?.value ?? timeframe)}
                    placeholder="Select timeframe"
                    classNamePrefix="tmselect"
                    menuPortalTarget={document.body}
                    menuPosition="fixed"
                    menuShouldScrollIntoView={false}
                    maxMenuHeight={260}
                />
            </div>

            <div className="backtest-info-item">
                <span>Start Date</span>
                <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
                <span>End Date</span>
                <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </div>

            <div className="backtest-actions">
                <button className="backtest-button" onClick={() => updateWeek("prev")}>Previous Week</button>
                <button className="backtest-button" onClick={() => updateWeek("next")}>Next Week</button>
                <button className="backtest-button" onClick={fetchChartData}>Load Chart</button>
            </div>

            {chartError && <div className="form-error">{chartError}</div>}
        </div>
    );
};

export default SymbolTimeframeCard;
