export interface TokenPayload {
    sub: string;
    user_id: number;
    first_name: string;
    last_name: string;
    exp: number;
    iat?: number;
}
