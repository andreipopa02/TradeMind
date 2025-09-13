import React from 'react';
import { Clock4 } from 'lucide-react';
import { motion } from 'framer-motion';

import '../styles/ResultsByDuration.css';



interface DurationStat {
    range: string;
    trades: number;
    profit: number;
}

interface ResultsByDurationProps {
    data: DurationStat[];
}

const DurationCard = ({ range, trades, profit }: DurationStat) => (
    <motion.div
        whileHover={{ scale: 1.03 }}
        className={`duration-card redesigned ${profit >= 0 ? 'positive' : 'negative'}`}
    >
        <div className="icon-wrapper">
            <Clock4 size={18} />
        </div>
        <span className="stat-label">{range}</span>
        <span className="stat-value">
            {trades} {trades === 1 ? 'trade' : 'trades'}
        </span> <span className="stat-value">
            {profit >= 0 ? '+' : '-'}${Math.abs(profit).toFixed(2)}
        </span>
    </motion.div>
);

const ResultsByDuration: React.FC<ResultsByDurationProps> = ({ data }) => {
    return (
        <div className="dashboard-section">
            <div className="duration-grid">
                {data.map((item, index) => (
                    <DurationCard key={index} {...item} />
                ))}
            </div>
        </div>
    );
};

export default ResultsByDuration;
