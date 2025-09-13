import React from "react";
import Select from "react-select";

import {ui2Styles} from "../../../components/ThemeContext";



interface Strategy {
    id: number;
    name: string;
}

interface Props {
    strategyType: "public" | "personal";
    setStrategyType: (val: "public" | "personal") => void;
    strategy_id: string;
    setStrategy: (val: string) => void;
    availableStrategies: Strategy[];
    userStrategies: Strategy[];
    initial_balance: number;
    setInitialBalance: (val: number) => void;
    risk_per_trade: number;
    setRiskPerTrade: (val: number) => void;
    riskReward: number;
    setRiskReward: (val: number) => void;
    runBacktest: () => void;
    backtestError: string | null;
}

const BacktestParametersCard: React.FC<Props> = ({
                                                     strategyType, setStrategyType,
                                                     strategy_id, setStrategy,
                                                     availableStrategies, userStrategies,
                                                     initial_balance, setInitialBalance,
                                                     risk_per_trade, setRiskPerTrade,
                                                     riskReward, setRiskReward,
                                                     runBacktest, backtestError
                                                 }) => {

    const strategyTypeOptions = [
        { value: "public", label: "Public" },
        { value: "personal", label: "Personal" },
    ] as const;

    const strategyOptions = (strategyType === "public" ? availableStrategies : userStrategies)
        .map(s => ({ value: String(s.id), label: s.name }));

    const balanceOptions = [5, 10, 25, 50, 100, 200].map(k => ({
        value: k * 1000,
        label: `${k}k USD`,
    }));

    const rrOptions = [
        { value: 1, label: "1 : 1" },
        { value: 2, label: "1 : 2" },
        { value: 3, label: "1 : 3" },
    ];

    return (
        <div className="backtest-card">
            <h3>Select Backtest parameters</h3>

            <div className="backtest-info-item">
                <span>Strategy Type</span>
                <Select
                    styles={ui2Styles}
                    options={strategyTypeOptions as any}
                    value={strategyTypeOptions.find(o => o.value === strategyType) as any}
                    onChange={(opt: any) => {
                        setStrategyType(opt?.value ?? "public");
                        setStrategy("");
                    }}
                    placeholder="Choose type"
                    classNamePrefix="tmselect"
                    menuPortalTarget={document.body}
                    menuPosition="fixed"
                    menuShouldScrollIntoView={false}
                    maxMenuHeight={260}
                />
            </div>

            <div className="backtest-info-item">
                <span>Select Strategy</span>
                <Select
                    styles={ui2Styles}
                    options={strategyOptions}
                    value={strategy_id ? strategyOptions.find(o => o.value === strategy_id) ?? null : null}
                    onChange={(opt: any) => setStrategy(opt?.value ?? "")}
                    placeholder="-- Choose a strategy --"
                    isClearable
                    noOptionsMessage={() => "No strategies"}
                    classNamePrefix="tmselect"
                    menuPortalTarget={document.body}
                    menuPosition="fixed"
                    menuShouldScrollIntoView={false}
                    maxMenuHeight={260}
                />
            </div>

            <div className="backtest-info-item">
                <span>Initial Balance</span>
                <Select
                    styles={ui2Styles}
                    options={balanceOptions}
                    value={balanceOptions.find(o => o.value === initial_balance) ?? null}
                    onChange={(opt: any) => setInitialBalance(Number(opt?.value ?? initial_balance))}
                    placeholder="Select balance"
                    classNamePrefix="tmselect"
                    menuPortalTarget={document.body}
                    menuPosition="fixed"
                    menuShouldScrollIntoView={false}
                    maxMenuHeight={260}
                />

                <span>Risk per trade (%)</span>
                <input
                    type="number"
                    min={0.01}
                    max={10}
                    step={0.01}
                    value={risk_per_trade}
                    onChange={(e) => {
                        const val = parseFloat(e.target.value);
                        if (!isNaN(val)) {
                            const corrected = Math.min(Math.max(val, 0.01), 10);
                            setRiskPerTrade(corrected);
                        }
                    }}
                />

                <span>Risk / Reward</span>
                <Select
                    styles={ui2Styles}
                    options={rrOptions}
                    value={rrOptions.find(o => o.value === riskReward) ?? null}
                    onChange={(opt: any) => setRiskReward(Number(opt?.value ?? riskReward))}
                    placeholder="Select R:R"
                    classNamePrefix="tmselect"
                    menuPortalTarget={document.body}
                    menuPosition="fixed"
                    menuShouldScrollIntoView={false}
                    maxMenuHeight={260}

                />
            </div>

            <div className="backtest-actions">
                <button className="backtest-button" onClick={runBacktest}>
                    Run Backtest
                </button>
            </div>

            {backtestError && <div className="form-error">{backtestError}</div>}
        </div>
    );
};

export default BacktestParametersCard;
