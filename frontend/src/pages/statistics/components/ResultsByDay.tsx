import React from 'react';
import { CalendarDays } from 'lucide-react';
import { motion } from 'framer-motion';

import '../styles/ResultsByDay.css';



interface DayStat {
    day: string;
    profit: number;
    trades: number;
}

interface ResultsByDayProps {
    data: DayStat[];
}

const DayCard = ({
                     day,
                     profit,
                     trades
                 }: {
    day: string;
    profit: number;
    trades: number;
}) => (
    <motion.div
        whileHover={{ scale: 1.03 }}
        className={`day-card redesigned ${profit >= 0 ? 'positive' : 'negative'}`}
    >
        <div className="icon-wrapper">
            <CalendarDays size={18} />
        </div>
        <span className="stat-label">{day}</span>
        <span className="stat-value">{trades} trades</span>
        <div className="profit-row">
            <span className="stat-value">${profit.toFixed(2)}</span>
        </div>
    </motion.div>
);

const ResultsByDay: React.FC<ResultsByDayProps> = ({ data }) => {
    return (
        <div className="dashboard-section">
            <div className="day-grid">
                {data.map((item, index) => (
                    <DayCard
                        key={index}
                        day={item.day}
                        trades={item.trades}
                        profit={item.profit}
                    />
                ))}
            </div>
        </div>
    );
};

export default ResultsByDay;
