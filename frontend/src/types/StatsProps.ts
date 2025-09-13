export interface StatsProps {
    stats: {
        totalTrades?: number;
        winRate?: number;
        avgProfit?: number;
        avgLoss?: number;
        profitFactor?: number;
    } | null;
}