import React from 'react'
import { User } from '../models/User'
import { makeAutoObservable } from 'mobx';
import AuthService from '../services/AuthService';
import axios from 'axios';
import { AuthResponce } from '../models/response/AuthResponce';
import { API_URL } from '../http';


export default class Store {
    user = {} as User;
    isAuth = false;

    isLoading = false;

    constructor() {
        makeAutoObservable(this);
    }

    setAuth(bool: boolean) {
        this.isAuth = bool;
    }

    setUser(user: User) {
        this.user = user;
    }
    setLoading(bool: boolean) {
        this.isLoading = bool;
    }

    async login(username: string, password: string) {
        try {
            const response = await AuthService.login(username, password);
            console.log(response)
            localStorage.setItem('access', response.data.access_token);
            this.setAuth(true);
            this.setUser(response.data.user);
        } catch (e: any) {
            if ('response' in e && e.response?.data?.message) {
                console.log(e.response.data.message);
            } else {
                console.log('An error occurred:', e);
            }
        }
    }

    async logout() {
        try {
            const response = await AuthService.logout();
            this.setAuth(false);
            this.setUser({} as User);
            localStorage.removeItem('access');
        } catch (e: any) {
            if ('response' in e && e.response?.data?.message) {
                console.log(e.response.data.message);
            } else {
                console.log('An error occurred:', e);
            }
        }
    }
    
    async registration(username: string, email: string, password: string) {
        try {
            const response = await AuthService.registration(username, email, password);
        } catch (e: any) {
            if ('response' in e && e.response?.data?.message) {
                console.log(e.response.data.message);
            } else {
                console.log('An error occurred:', e);
            }
        }
    }

    async checkAuth() {
        this.setLoading(true);
        try {
            const response = await axios.get<AuthResponce>(`${API_URL}/auth/refresh_token`, {withCredentials: true})
            console.log(response);
            localStorage.setItem('access', response.data.access_token);
            this.setAuth(true);
            this.setUser(response.data.user);
        } catch (e) {
            console.log(e);
        } finally {
            this.setLoading(false);
        }
    }

}
