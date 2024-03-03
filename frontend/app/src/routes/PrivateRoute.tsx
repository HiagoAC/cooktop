import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";


export function PrivateRoute() {
    const { accessToken } = useAuth();
    console.log(accessToken);
    return accessToken ?
        <Outlet />
        : <Navigate to="/" />;
}
