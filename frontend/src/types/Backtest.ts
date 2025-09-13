export interface Candle {
    time: number;
    open: number;
    high: number;
    low: number;
    close: number;
}

export interface ExecutedTrade {
    entry_id: number;
    exit_id: number;
    entry_action: string;
    exit_action: string;
    entry_price: number;
    exit_price: number;
    profit: number;
    open_timestamp: number;
    close_timestamp: number;

    sl_price?: number;
    tp_price?: number;
}
