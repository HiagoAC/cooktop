import { createContext, useState, ReactNode, useEffect, useMemo } from 'react';
import axios from 'axios';
import { getTokens } from '../api/tokensApi';

export interface AuthContextType {
    accessToken: string | null;
    refreshToken: string | null;
    logIn: (
        email: string,
        password: string
        ) => Promise<void>;
}

export const AuthContext: React.Context<AuthContextType> = createContext<AuthContextType>({
    accessToken: null,
    refreshToken: null,
    logIn: async (_e: string, _p: string) => {},
});


interface Props {
    children: ReactNode;
}

export function AuthProvider({children}: Props) {
    const [accessToken, setAccessToken] = useState<string | null>(
        localStorage.getItem("accessToken"));
    const [refreshToken, setRefreshToken] = useState<string | null>(
        localStorage.getItem("refreshToken"));
    const [loading, setLoading] = useState<boolean>(false);

    const logIn = async (email: string, password: string): Promise<void> => {
            setLoading(true);
            axios.defaults.headers.common["Authorization"] = "";
            axios.defaults.headers.common["Authorization"] = "";
            const response = await getTokens({
                email: email,
                password: password});
            setAccessToken(response.access_token);
            setRefreshToken(response.refresh_token);
    };

    useEffect(() => {
        const updateTokens = async () => {
            try {
                if (accessToken && refreshToken) {
                    axios.defaults.headers.common["Authorization"] = "Bearer " + accessToken;
                    localStorage.setItem('accessToken', accessToken);
                    localStorage.setItem('refreshToken', refreshToken);
                } else {
                    delete axios.defaults.headers.common["Authorization"];
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                }
            } finally {
                setLoading(false);
        }}
        updateTokens();
    }, [accessToken, refreshToken]);

    const contextValue = useMemo(
        () => ({
          accessToken,
          refreshToken,
          logIn,
        }),
        [accessToken, refreshToken]
      );

    return (
        <AuthContext.Provider value={contextValue}>
            {loading? null : children}
        </AuthContext.Provider>
    );
}
