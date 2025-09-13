import React from 'react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid,
    Legend,
} from 'recharts';
import '../styles/BalanceCurveChart.css';



interface BalanceCurveChartProps {
    data: { trade: number; balance: number }[];
}

const BalanceCurveChart: React.FC<BalanceCurveChartProps> = ({ data }) => {
    if (!data || data.length === 0) return null;

    const balances = data.map(d => d.balance);
    const min = Math.min(...balances);
    const max = Math.max(...balances);
    const range = Math.max(1, max - min);
    const pad = Math.max(range * 0.05, 50);

    return (
        <div className="chart-section">
            <h3>📈 Balance Curve</h3>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="trade" />
                    <YAxis
                        domain={[min - pad, max + pad]}
                        tickCount={6}
                        width={80}
                        allowDecimals={false}
                        tickFormatter={(v: number) =>
                            v.toLocaleString('en-US', { maximumFractionDigits: 0 })
                        }
                    />
                    <Tooltip
                        formatter={(value: number) => value.toFixed(2)}
                        labelFormatter={(label) => `Trade: ${label}`}
                    />
                    <Legend />
                    <Line type="monotone" dataKey="balance" stroke="#00e676" strokeWidth={2} dot />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default BalanceCurveChart;
