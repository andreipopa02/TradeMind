export interface TradeJournal {
    ticket: number;
    symbol?: string;
    volume?: number;
    price?: number;
    commission?: number;
    swap?: number;
    profit?: number;
    time?: string | number;
}
