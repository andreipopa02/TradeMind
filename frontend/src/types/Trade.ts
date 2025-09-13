export interface Trade {
    id: number;
    user_id: number;

    market: string;
    type: string;
    volume: number;

    open_date: string;
    open_time: string;
    close_date?: string;
    close_time?: string;
    session?: string;

    open_price: number;
    close_price?: number;
    sl_price?: number;
    tp_price?: number;

    swap?: number;
    commission?: number;
    profit?: number;
    pips?: number;

    link_photo?: string;

    source_type: string;
}
