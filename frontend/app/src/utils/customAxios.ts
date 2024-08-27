import axios from 'axios';
import { refreshTokens } from '../api/tokensApi';

const handleRefreshTokens = async (refreshToken: string) => {
    try {
        console.log('Refreshing token.......................');
        refreshTokens(refreshToken).then((res) => {
            axios.defaults.headers.common["Authorization"] = "Bearer " + res.access_token;
            localStorage.setItem('accessToken', res.access_token);
            localStorage.setItem('refreshToken', res.refresh_token);
        });

    } catch (error) {
        console.error('Failed to refresh token', error);
    }
};

export function getAxiosInstance () {
    const instance = axios.create({});
    console.log('Setting up interceptor');
    axios.interceptors.response.use(
        (response: any) => {
            console.log('Response Interceptor:', response);
            return response;
        },
        async (error: any) => {
            console.log('Interceptor error:', error);
            var originalRequest = error.config;
            if (error.response?.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true;
                if (localStorage.getItem("refreshToken")) {
                    const refreshToken: string = localStorage.getItem("refreshToken") || '';
                    await handleRefreshTokens(refreshToken);
                }
                return axios(error.config);
            }
            return Promise.reject(error);
    });
    return instance;
}
