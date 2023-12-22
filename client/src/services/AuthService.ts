import $api from '../http'
import { AxiosResponse } from 'axios'
import { AuthResponce } from '../models/response/AuthResponce'

export default class AuthService {
    static async login(username: string, password: string): Promise<AxiosResponse<AuthResponce>> {
        return $api.post<AuthResponce>('/auth/login', {username, password},)
    }

    static async registration(username: string, email: string, password: string): Promise<AxiosResponse<AuthResponce>> {
        const defaultValues = {
          phone_number: 'default_phone_number',
          first_name: 'default_first_name',
          last_name: 'default_last_name',
          roles: 'ROLE_PACIENT'
        };
        return $api.post<AuthResponce>('/auth/registration', { username, email, password, ...defaultValues });
      }
      

    static async logout(): Promise<void> {
        return $api.post('/auth/logout')
    }
}

