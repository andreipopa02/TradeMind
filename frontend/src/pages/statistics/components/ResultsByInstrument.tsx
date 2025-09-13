import React from 'react';
import { PieChart } from 'lucide-react';
import { motion } from 'framer-motion';

import '../styles/ResultsByInstrument.css';



interface InstrumentResult {
    instrument: string;
    trades: number;
    profit: number;
}

interface ResultsByInstrumentProps {
    data: InstrumentResult[];
}

const InstrumentCard = ({ instrument, trades, profit }: InstrumentResult) => (
    <motion.div
        whileHover={{ scale: 1.03 }}
        className={`instrument-card redesigned ${profit >= 0 ? 'positive' : 'negative'}`}
    >
        <div className="icon-wrapper">
            <PieChart size={18} />
        </div>
        <span className="stat-label">{instrument}</span>
        <span className="stat-value">{trades} trades</span>
        <span className="stat-value">
            {profit >= 0 ? '+' : '-'}${Math.abs(profit).toFixed(2)}
        </span>
    </motion.div>
);

const ResultsByInstrument: React.FC<ResultsByInstrumentProps> = ({ data }) => {
    return (
        <div className="dashboard-section">
            <div className="instrument-grid">
                {data.map((row, index) => (
                    <InstrumentCard key={index} {...row} />
                ))}
            </div>
        </div>
    );
};

export default ResultsByInstrument;
