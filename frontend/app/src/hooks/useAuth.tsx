import { useContext } from 'react';
import { AuthContext, AuthContextType } from "../context/AuthContext";


export function useAuth(): AuthContextType {
    return useContext(AuthContext);
}
