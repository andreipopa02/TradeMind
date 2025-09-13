import {useMemo} from "react";
import * as jwt_decode from "jwt-decode";
import { TokenPayload } from "../types/TokenPayload";

export function useAuth() {
    const token = localStorage.getItem("access_token");

    return useMemo(() => {
        if (!token) return null;
        try {
            const decoded = jwt_decode.jwtDecode<TokenPayload>(token);
            if (decoded.exp * 1000 < Date.now()) {
                return null;
            }
            return {
                email: decoded.sub,
                id: decoded.user_id,
                firstName: decoded.first_name,
            };
        } catch (e) {
            return null;
        }
    }, [token]);
}
