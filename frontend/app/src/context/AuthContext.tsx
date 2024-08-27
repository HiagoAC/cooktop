import { createContext, useState, ReactNode, useEffect, useMemo } from 'react';
import { getAxiosInstance } from '../utils/customAxios';
import { getTokens } from '../api/tokensApi';

const axios = getAxiosInstance();

export interface AuthContextType {
    accessToken: string | null;
    refreshToken: string | null;
    logIn: (
        email: string,
        password: string
        ) => Promise<void>;
    logOut: () => Promise<void>;
}

export const AuthContext: React.Context<AuthContextType> = createContext<AuthContextType>({
    accessToken: null,
    refreshToken: null,
    logIn: async (_e: string, _p: string) => {},
    logOut: async () => {},
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
            const response = await getTokens({
                email: email,
                password: password});
            setAccessToken(response.access_token);
            setRefreshToken(response.refresh_token);
    };

    const logOut = async (): Promise<void> => {
        setAccessToken(null);
        setRefreshToken(null);
        delete axios.defaults.headers.common["Authorization"];
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    }

    useEffect(() => {
        const updateTokens = async () => {
            try {
                if (accessToken && refreshToken) {
                    axios.defaults.headers.common["Authorization"] = "Bearer " + accessToken;
                    localStorage.setItem('accessToken', accessToken);
                    localStorage.setItem('refreshToken', refreshToken);
                } else {
                    logOut();
                }
            } finally {
                setLoading(false);
        }}
        updateTokens();

    }, [accessToken, refreshToken]);

    const contextValue = useMemo(
        () => ({
            accessToken: localStorage.getItem("accessToken"),
            refreshToken: localStorage.getItem("refreshToken"),
            logIn,
            logOut,
        }),
        [accessToken, refreshToken]
    );

    return (
        <AuthContext.Provider value={contextValue}>
            {loading? null : children}
        </AuthContext.Provider>
    );
}
