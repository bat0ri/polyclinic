import axios from "axios";
import { error } from "console";
import { config } from "process";
import { AuthResponce } from "../models/response/AuthResponce";

export const API_URL = "http://127.0.0.1:8000"

const $api = axios.create({
    baseURL: API_URL,
    withCredentials: true,
});



$api.interceptors.request.use((config) => {
    config.headers.Authorization = `Bearer ${localStorage.getItem('access')}`
    return config
})


$api.interceptors.response.use((config) => {
    return config;
},async (error) => {
    const originalRequest = error.config;
    if (error.response.status == 403 && error.response.status == 401 && error.config && !error.config._isRetry) {
        originalRequest._isRetry = true;
        try {
            const response = await axios.get<AuthResponce>(`${API_URL}/auth/refresh_token`, {withCredentials: true})
            localStorage.setItem('access', response.data.access_token);
            return $api.request(originalRequest);
        } catch (e) {
            console.log('НЕ АВТОРИЗОВАН')
        }
    }
    throw error;
})

export default $api;