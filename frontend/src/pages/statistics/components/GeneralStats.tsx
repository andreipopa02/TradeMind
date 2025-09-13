import React from 'react';
import { TrendingUp, TrendingDown, Percent, DollarSign, Scale, Trophy, XCircle } from 'lucide-react';
import { motion } from 'framer-motion';

import '../styles/GeneralStatsStyles.css';



interface GeneralStatsProps {
    metrics: any;
}

export const StatCard = ({
                      icon: Icon,
                      label,
                      value,
                      positive
                  }: {
    icon: any;
    label: string;
    value: string;
    positive?: boolean;
}) => (
    <motion.div
        whileHover={{ scale: 1.02 }}
        className={`stat-item redesigned ${positive ? 'positive' : !positive ? 'negative' : ''}`}
    >
        <div className="icon-wrapper">
            <Icon size={18} />
        </div>
        <div className="stat-content">
            <span className="stat-label">{label}</span>
            <span className="stat-value">{value}</span>
        </div>
    </motion.div>
);


const GeneralStats: React.FC<GeneralStatsProps> = ({ metrics }) => {
    if (!metrics) return null;

    return (
        <div className="dashboard-section">
            <div className="general-stats-grid">
                <StatCard icon={DollarSign} label="Result" value={`$${(metrics.total_result ?? 0).toFixed(2)}`} positive={true} />
                <StatCard icon={Percent} label="Win rate" value={`${metrics.winrate ?? 0}%`} />
                <StatCard icon={TrendingUp} label="Avg. Profit" value={`$${(metrics.avg_profit ?? 0).toFixed(2)}`} positive={true} />
                <StatCard icon={TrendingDown} label="Avg. Loss" value={`$${(metrics.avg_loss ?? 0).toFixed(2)}`} positive={false} />
                <StatCard icon={Scale} label="RRR" value={`${(metrics.avg_rr ?? 0).toFixed(2)}`} />
                <StatCard icon={Trophy} label="Max Profit" value={`$${(metrics.max_profit ?? 0).toFixed(2)}`} positive={true} />
                <StatCard icon={XCircle} label="Max Loss" value={`$${(metrics.max_loss ?? 0).toFixed(2)}`} positive={false} />
            </div>
        </div>
    );
};

export default GeneralStats;
