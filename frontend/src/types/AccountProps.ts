export interface AccountProps {
    account: {
        account_id: string;
        broker_name: string;
        status?: string;
        platform?: string;
        password?: string;
        server?: string;
        balance?: number | null;
        equity?: number | null;
        active_positions?: number | null;
        currency?: string | null;
    };
    onDelete: (accountId: number) => void;
}