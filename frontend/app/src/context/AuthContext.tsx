import { createContext, useState, ReactNode, useEffect, useMemo } from 'react';
import axios from 'axios';

export interface AuthContextType {
    accessToken: string | null;
    refreshToken: string | null;
    updateTokens: (
        newAccessToken: string,
        newRefreshToken: string
        ) => void;
}

export const AuthContext: React.Context<AuthContextType> = createContext<AuthContextType>({
    accessToken: null,
    refreshToken: null,
    updateTokens: (_a: string, _r: string) => {}
});


interface Props {
    children: ReactNode;
}

export function AuthProvider({children}: Props) {
    const [accessToken, setAccessToken] = useState<string | null>(
        localStorage.getItem("accessToken"));
    const [refreshToken, setRefreshToken] = useState<string | null>(
        localStorage.getItem("refreshToken"));

    const updateTokens = (
        newRefreshToken: string,
        newAccessToken: string)
        : void => {
            console.log(newAccessToken);
            console.log(newRefreshToken);
            setAccessToken(newAccessToken);
            setRefreshToken(newRefreshToken);
            console.log(accessToken);
            console.log(refreshToken);
      };

    useEffect(() => {
        if (accessToken && refreshToken) {
            axios.defaults.headers.common["Authorization"] = "Bearer " + accessToken;
            localStorage.setItem('accessToken', accessToken);
            localStorage.setItem('refreshToken', refreshToken);
        } else {
            delete axios.defaults.headers.common["Authorization"];
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
        }
    }, [accessToken, refreshToken]);

    const contextValue = useMemo(
        () => ({
          accessToken,
          refreshToken,
          updateTokens
        }),
        [accessToken, refreshToken]
      );

    return (
        <AuthContext.Provider value={contextValue}>
          {children}
        </AuthContext.Provider>
    );
}
