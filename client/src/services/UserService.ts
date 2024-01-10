import $api from '../http'
import { AxiosResponse } from 'axios'
import { AuthResponce } from '../models/response/AuthResponce'
import { User } from '../models/User'
import { Meet } from '../models/Meet'

export default class UserService {
    static fetchDoctors(): Promise<AxiosResponse<User[]>> {
        return $api.get<User[]>('/auth/protected')
    }

    static async makeMeet(meet_date: string, doctor_id: string, doctor_username: string | null): Promise<AxiosResponse<Meet>> {
        return $api.post<Meet>('/meeting/create', {
            meet_date,
            doctor_id,
            doctor_username
        });
    }

    static fetchMeets(): Promise<AxiosResponse<Meet[]>> {
        return $api.get<Meet[]>('/meeting/list');
    }

    static fetchMeetsDoctor(): Promise<AxiosResponse<Meet[]>> {
        return $api.get<Meet[]>('/meeting/list/doctor');
    }
    
}

