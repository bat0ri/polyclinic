import $api from '../http'
import { AxiosResponse } from 'axios'
import { AuthResponce } from '../models/response/AuthResponce'
import { User } from '../models/User'

export default class UserService {
    static fetchUsers(): Promise<AxiosResponse<User[]>> {
        return $api.get<User[]>('/auth/protected')
    }
}

